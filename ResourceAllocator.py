import vectors
from threading import Thread

class ResourceAllocator(Thread):
    def __init__(self, lock, allocation, available, max, requestQueue, allocationResponse, processFinish, detailedOutput=False):
        Thread.__init__(self)
        self.lock = lock
        self.allocation = allocation
        self.available = available
        self.max = max
        self.requestQueue = requestQueue
        self.allocationResponse = allocationResponse
        self.processFinish = processFinish
        self.detailedOutput = detailedOutput

    # @staticmethod
    def _safe(max: list[list[int]], allocation: list[list[int]], available: list[int]) -> bool:
        """Checks if the given resource system is in a safe state.

        Implements resource safety algorithm. 

        Parameters:
            max: matrix representing the maximum resources that each process needs to complete.
            allocation: matrix representing the allocated resources that each process currently holds.
            available: vector representing the currently available resources.

        Returns:
            bool: A bool indicating if system is in safe state
        """
        need = vectors.subtractMatrix(max, allocation, inplace=False)
        finish = [False for process in allocation]
        resourceAllocated = True

        while resourceAllocated:
            resourceAllocated = False
            for processNum, (processNeed, processFinish) in enumerate(zip(need, finish)):
                # if the process is not finished and enough available resources
                if not processFinish and vectors.lessThanEqual(processNeed, available):
                    vectors.addVector(available, allocation[processNum])
                    finish[processNum] = True
                    resourceAllocated = True
                    break
        return all(finish)

    def _checkRequest(self, processNum: int, request: list[int]) -> bool:
        """Checks if a resource request made by a process will result in a system safe state

        Implements the Banker's Algorithm: https://en.wikipedia.org/wiki/Banker%27s_algorithm

        Parameters:
            processNum: the processNum of the process that made the request
            request: a vector representing the request the process made

        Returns:
            bool: A bool indicating if approving the request keeps the system in a safe state
        """
        need = vectors.subtractVector(self.max[processNum], self.allocation[processNum], inplace=False)
        # checks if process request is less/equal to the amount the process needs
        if not vectors.lessThanEqual(request, need):
            return False
        # checks if process request is less/equal to resources available
        if not vectors.lessThanEqual(request, self.available):
            return False
        # create new state (not modifying current state) with request fufilled
        newAllocation = [row[:] for row in self.allocation]
        vectors.addVector(newAllocation[processNum], request)
        # checks if that state is safe
        return ResourceAllocator._safe(max=self.max, allocation=newAllocation, available=vectors.subtractVector(self.available,request, inplace=False))

    def _processApprovedRequest(self, processNum: int, currentRequest: list[int]):
        """Processes an approved request.

        Updates all data structures to allocate the resources to processNum and inform processNum that the resource has been allocated.
        Prints output statement.

        Parameters: 
            processNum: the processNum of the process that made the request
            currentRequest: a vector representing the approved request the process made
        """
        self.lock.acquire()
        # response to processNum is True
        self.allocationResponse[processNum] = True
        # Updates allocation and available resources
        vectors.addVector(self.allocation[processNum], currentRequest)
        vectors.subtractVector(self.available, currentRequest)
        print(f'\nRequest {currentRequest} for process {processNum} approved.\nMax Vector: {self.max} \nAllocation Vector: {self.allocation} \nAvailable Vector: {self.available}\nProcess Finish Vector: {self.processFinish}\n')
        self.lock.release()
        
    def _processDeniedRequest(self, processNum: int, currentRequest: list[int]):
        """Processes an denied request.

        Updates data structures to inform processNum that the request had been denied.
        Prints output statement.

        Parameters: 
            processNum: the processNum of the process that made the request
            currentRequest: a vector representing the denied request the process made
        """
        self.lock.acquire()
        # response to processNum is False
        self.allocationResponse[processNum] = False
        if self.detailedOutput:
            print(f'Request {currentRequest} from process {processNum} denied due to putting system in unsafe state')
        self.lock.release()

    def _getNextOutstandingRequest(self) -> tuple[int, list[int]]:
        """Gets the next outstanding request in the requestQueue

        Returns: 
            tuple: 
                tuple[0] is the processNum that made the request
                tuple[1] is a vector representing the request
        """
        self.lock.acquire()
        # gets (processNum, currentRequest) from the first outstanding request in the queue
        processNum, currentRequest = self.requestQueue.pop()
        self.lock.release()
        return processNum, currentRequest

    def run(self):
        """While processes haven't completed, processes requests made in request queue and approves/denies them and processes them.

        Runs while processFinish vector is not fully populated. 
        Updates allocation and available vector when approved requests are made. 
        Overrides threading.Thread run() function. 
        """
        while True:
            # busy waits when there are no requests
            while(not len(self.requestQueue)):
                # if all processes are finished process completes.
                if all(self.processFinish):
                    return
                continue
            processNum, currentRequest = self._getNextOutstandingRequest()
            if self._checkRequest(processNum, currentRequest):
                self._processApprovedRequest(processNum, currentRequest)
            else:
                self._processDeniedRequest(processNum, currentRequest)