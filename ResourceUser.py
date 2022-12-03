import vectors
from time import sleep
from threading import Thread

class ResourceUser(Thread):
    FAILED_ATTEMPTS_ALLOWED = 3
    COOLDOWN = 0.5
    UNWRITTEN_RESPONSE_FLAG = -1

    def __init__(self, processId, lock, processAllocation, available, processMax, requestQueue, allocationResponse, processFinish, processFinishOrder):
        Thread.__init__(self)
        self.processId = processId
        self.lock = lock
        self.processAllocation = processAllocation
        self.available = available
        self.processMax = processMax
        self.requestQueue = requestQueue
        self.allocationResponse = allocationResponse
        self.processFinish = processFinish
        self.processFinishOrder = processFinishOrder  

    def _makeResourceRequest(self, request: list) -> bool:
        """Makes a resource request and busy waits until ResourceAllocator returns a response. Checks if request was granted.

        Parameters: 
            request: vector representing the resource vector that the process is requesting.

        Returns:
            bool: A bool indicating if the resource request was granted
        """
        self.lock.acquire()
        # sets the allocation response to UNWRITTEN_RESPONSE_FLAG
        self.allocationResponse[self.processId] = ResourceUser.UNWRITTEN_RESPONSE_FLAG
        # appends (processId,request) to the queue
        self.requestQueue.append((self.processId, request))
        self.lock.release()
        # Busy wait while allocator hasn't responded
        while(self.allocationResponse[self.processId] == ResourceUser.UNWRITTEN_RESPONSE_FLAG):
            continue
        return self.allocationResponse[self.processId]

    # recursively goes through all possible requests. Returns [resources] if a request is fufilled.
    def _sendAllResourceRequests(self, need: list[int], request: list[int]) -> bool:
        """Makes all resource requests below the process need vector. If any of these requests are approved, immediately returns.

        Parameters: 
            need: Vector representing the process resource need 
            request: Current request vector. Recursively builds the request vector.

        Returns:
            bool: A bool indicating if a resource request was granted
        """
        # if the all the needed resources in the need vector are accounted for
        if len(need) == 0:
            # Makes request if the request is not all zeros
            if not vectors.zeros(request):
                return self._makeResourceRequest(request)
            else:
                return False
        # Iterates through all possible request values for the first needed resource in the need vector. Iterates from largest request to smallest request (need[0] to 0, decrementing)
        for i in range(need[0],-1,-1):
            # Recursively builds the request for all combinations.
            requestApproved = self._sendAllResourceRequests(need[1:], request + [i])
            # If a request is approved return
            if requestApproved:
                return requestApproved
        return False
    
    def _sendAllResourceRequestsWithRetry(self, need: list[int]) -> bool:
        """Makes all resource requests below the process need vector with retries and cooldowns.

        This method is necessary because of the behavior of concurrent threads. It is possible that on all resource request sends in a given time interval none of them are approved, but the process could complete in the future if a resource user returns resources to the system. For systems that require longer processing time, more retries/longer cooldowns may be necessary. If cooldowns are all used without a sucessful request, the process times out.

        Parameters: 
            need: Vector representing the process resource need.

        Returns:
            bool: A bool indicating if a resource request was granted
        """
        numberOfFailedAttempts = 0
        while numberOfFailedAttempts < ResourceUser.FAILED_ATTEMPTS_ALLOWED:
            requestApproved = self._sendAllResourceRequests(need, [])
            # once a request is approved, returns.
            if requestApproved:
                return True
            else:
                # if all requests fail, cooldown before sending all requests again.
                sleep(ResourceUser.COOLDOWN)
                numberOfFailedAttempts += 1
        return False      

    def _processResourceUserFailure(self, need):
        """Processes the resource user failure event.

        Updates all data structures to inform resource allocator of resource user failure. Prints output statement.

        Parameters: 
            need: Vector representing the process resource need.
        """
        self.lock.acquire()
        # Upon finish, adds "Not Completed" to the processFinish vector to give finish status
        self.processFinish[self.processId] = "Not Completed"
        print(f'\n--------------------------------------------------\nResource user {self.processId} timed out and failed to get resources.\nProcess needed {need} more resources to complete.\nProcess will die with {self.processAllocation} resources.\nAvailable vector: {self.available}\nProcess Finish Vector: {self.processFinish}\n--------------------------------------------------\n')
        self.lock.release()

    def _processResourceUserSuccess(self):
        """Processes the resource user success event.

        Updates all data structures to inform resource allocator of resource user sucess. Returns all resources to the system. Prints output statement.
        """
        self.lock.acquire()
        # Returns resources to system
        vectors.addVector(self.available, self.processAllocation)
        # Sets clears own allocation vector 
        vectors.subtractVector(self.processAllocation, self.processAllocation)
        # Adds "Completed" to the processFinish vector to give finish status
        self.processFinish[self.processId] = "Completed"
        # Adds itself to the processFinishOrder queue
        self.processFinishOrder.append(self.processId)
        print(f'\n--------------------------------------------------\nResource user {self.processId} completed and released their resources.\nAvailable Vector: {self.available}\nProcess Finish Vector: {self.processFinish}\nProcess Completion Order: {self.processFinishOrder}\n--------------------------------------------------\n')
        self.lock.release()
    
    def run(self):
        """While the process needs resources to complete, makes resource requests until a timeout or process completion.

        Runs while timeout hasn't occurred for a process state or process has recieved all needed resources

        Overrides threading.Thread run() function. 
        """
        need = vectors.subtractVector(self.processMax, self.processAllocation, inplace = False)
        # while needs haven't been met
        while not vectors.zeros(need):
            # sends all requests with cooldown retries
            requestApproved = self._sendAllResourceRequestsWithRetry(need)
            if requestApproved:
                # updates need vector
                need = vectors.subtractVector(self.processMax, self.processAllocation, inplace = False)
            else:
                self._processResourceUserFailure(need)
                return
        self._processResourceUserSuccess()