from ResourceAllocator import ResourceAllocator
from ResourceUser import ResourceUser
from threading import Lock

# **********Modify these**********
allocation = [[5,2,0,0,5],[1,1,0,0,5],[0,0,0,4,3],[0,0,1,1,1],[3,0,0,3,1]]
max = [[5,4,2,2,5],[4,4,2,8,5],[4,4,2,8,5],[4,4,2,4,2],[4,4,1,3,1]]
available = [1,4,1,1,0]
detailedOutput = True
# ********************************

numberOfResourceUsers = len(allocation)
processFinish = [False] * numberOfResourceUsers 
requestQueue = [] 
allocationResponse = [0] * numberOfResourceUsers 
processFinishOrder = []
lock = Lock()


if __name__ =="__main__":
    print(f'**************************************************\nInitial State:\nMax Vector: {max}\nAllocation Vector: {allocation}\nAvailable Vector: {available}\nProcess Finish Vector: {processFinish}\nProcess Completion Order: {processFinishOrder}\n**************************************************\n')
    manager = ResourceAllocator(lock=lock,allocation=allocation,max=max, available=available,requestQueue=requestQueue, allocationResponse=allocationResponse, processFinish=processFinish, detailedOutput=detailedOutput)
    manager.start()
    threadArray = []
    for i in range(numberOfResourceUsers):
        thread = ResourceUser(processId=i,lock=lock,processAllocation=allocation[i],processMax=max[i], available=available,requestQueue=requestQueue, allocationResponse=allocationResponse, processFinish=processFinish, processFinishOrder=processFinishOrder)
        thread.start()
        threadArray.append(thread)
    for thread in threadArray:
        thread.join()
    manager.join()
    print(f'**************************************************\nFinal State:\nMax Vector: {max}\nAllocation Vector: {allocation}\nAvailable Vector: {available}\nProcess Finish Vector: {processFinish}\nProcess Completion Order: {processFinishOrder}\n**************************************************\n')
    print('Program Complete!')