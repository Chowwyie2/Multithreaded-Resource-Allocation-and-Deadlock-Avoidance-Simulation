# Lab 4 - Multithreaded Resource Allocation and Deadlock Avoidance Simulation 

# Summary

This project is a implementation of the Resource Allocation and Deadlock Concepts. This project is a mutithreaded simiulation of how a Banker's Algorithm (https://en.wikipedia.org/wiki/Banker%27s_algorithm) could be implemented in an OS. One thread is the designated "Resource Allocator", in charge of assigning resources and checking the safety of the system resource state. The other threads are "Resource Users", each requiring a certain amount of different resources before completion. These Resource Users will make requests to the Resource Allocator for resources, which the "Resource Allocator" will field and evaluate.

This was a fun project, I hope you enjoy.

# Table of Contents

- Overview
- Running the Program
- Expected Inputs
- Understanding the Output
- Main Data Structures
- Code Guide

# Overview

## Project Notes

An easy optimization could be made by running the safety algorithm at the initial state, but the point of the program is to be a simulate interactions between an allocator and users.

Additionally, instead of backtracking from the highest request possible and recursively going down, each resource user could only request resources one-at-a-time and not need to make larger requests. While this would absolutely work, I wanted to demonstrate the ResourceAllocator class capability.

## Programming Constructs Used

- Threads
- Shared Memory
- Mutex
- Message Passing

The threads all need to pass information to each other, namely, between each Resource User thread and the Resource Allocator thread. This is achieved with shared common data structures that are protected with mutexes when a critical section occurs that might cause a race condition.

## Main OS Concepts Used

- Deadlocks
- Resource Allocation

At the core of the Resource Allocator is the algorithm used to determine if the system is in a safe state. This algorithm, known as a Deadlock Detection algorithm is used to determine if any given request will leave the system in a safe state. That algorithm as a whole is the Banker's Algorithm discussed in class. Once this algorithm is used for a outstanding request, resources are then allocated to the requesting process if approved.

The pseudo-code shown in the Deadlocks slide 38 was referenced to implement the _safe method in the ResourceAllocator class.

The pseudo-code shown in the Deadlocks slide 38 was referenced to implement the _checkRequest method (Banker's Algorithm) in the ResourceAllocator class.

## Famous Problems Used

- Producer-Consumer Problem 
- Data-level parallelism

Each Resource User thread operates the same tasks with a different set of data, thus implementing data-level parallelism. The Producer-Consumer Problem is also used in the implementation of the requestQueue, which is the queue that oncoming requests to the Resource Allocator are sent to. Resource Users, the Producer, make requests that are pushed onto the requestQueue. The Resource Allocator, the Consumer, will take these requests off the queue for processing.

# Running the Program

This lab was designed with no dependancies other than built-in libraries, simply running:

'''
python3 runner.py
'''

will produce output.

# Expected inputs

The user should modify allocation, max, available, detailedOutput within runner.py. 

allocation: The allocation matrix the system starts with. Read section in main data structures for more information

max: The matrix that contains information about the number of resources needed by each Resource User for completion. Read section in main data structures for more information

available: Vector representing number of available resources. Read section in main data structures for more information

detailedOutput: If request messages are wanted, set this to True, otherwise it disabled denied request messages.

## Input Constraints

Try to keep the system in a smaller state, espcially if there is no win condition. This is because there is no timed timeout, rather the process will backtrack through all possible requests (it will still work if you are willing to wait).

Since it is assummed that all resources that are allocated are done so by the Resource Allocator, which never allocates more than the process needs, in no input should the initial allocation matrix have an quantity of resources that is greater than the corresponding one in the max matrix

Each vector in allocation must have length n, where n is the number of resources.

Each vector in max must have length n, where n is the number of resources.

Available must have length n, where n is the number of resources.

The length of allocation, which is the number of Resource Users must equal the length of max.

## Sample Inputs

To illustrate the program's behavior, here are some sample cases.

Case 1: 

allocation = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
max = [[1,1,1,1],[1,1,1,1],[1,1,1,1],[1,1,1,1]]
available = [1,4,1,1]
detailedOutput = False

Since Resource Users run concurrently, run it with this input a few times! You will notice the order of the process completion may change.

Case 2:

allocation = [[5,0,0,0,5],[1,1,0,0,5],[0,0,0,4,3],[0,0,1,1,1],[3,0,0,3,1]]
max = [[10,5,2,8,15],[5,5,2,8,10],[4,4,2,8,5],[4,4,2,4,2],[4,4,1,3,1]]
available = [1,4,1,1,0]
detailedOutput = True

This is an example of a larger system - a 5 resource user system with 5 resources. More importantly, this system only has one possible win condition. The Resource Allocator must allocate resources to users 4, 3, 2, 1 in that order to keep the system in a safe state the whole time.

Case 3:

allocation = [[1,1,0],[0,0,0],[0,0,1],[3,0,0]]
max = [[4,5,2],[4,4,2],[4,4,2],[4,4,2]]
available = [1,4,1]
detailedOutput = True

This is a fun one that shows the amount of processing that happens behind the scenes - despite being a smaller system (4 users, 3 resources to manage), running this will show the number of requests being processesed. 

This system starts in an unsafe state and no users will complete.

# Understanding the output

## Detailed Output

The boolean detailedOutput in runner.py can be set to True to display Optional Request Denial Messages. These are set to optional because they may clutter the output if the user is not interested in seeing all requests that were made. However, they illustrate the use of concurrency in the project well - without seeing these, the user may think that the Resource Users are operating sequentially. 

## Messages

### Resource User Completion

#### Message styling: --- (dashed line above and below)

Upon each resource user termination, sucessful or not, an output message containing helpful information will be printed, containing the success of the resource user, the available resources vector after returning resources, a vector containing the end state of each resource user, indexed by resource user ID, and the process completion order, which displays the resource users that completed successfully in order from left-to-right. 

Example:
--------------------------------------------------
Resource user 0 completed and released their resources.
Available Vector: [4, 4, 2, 12]
Process Finish Vector: ['Completed', 'Completed', 'Completed', 'Completed']
Process Completion Order: [3, 2, 1, 0]
--------------------------------------------------

### State messages

#### Message styling: *** (asterisk line above and below)

Two of these messages will be printed, one before the threads start running and one after. This message contains all relavent state information, like the Max Vector, Allocation Vector, Available Vector, Process Finish Vector, and Process Completion Order.

Example:
**************************************************
Final State:
Max Vector: [[4, 4, 1, 3], [4, 4, 1, 4], [4, 4, 1, 1], [4, 4, 1, 3]]
Allocation Vector: [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
Available Vector: [4, 4, 2, 12]
Process Finish Vector: ['Completed', 'Completed', 'Completed', 'Completed']
Process Completion Order: [3, 2, 1, 0]
**************************************************

### Request Aproval Messages

#### Message styling: none

Upon request completion, a block is printed with state information and the request information. This message includes: the approved request and the resource user that made the request, Max Vector, Allocation Vector, Available Vector, Process Finish Vector

Example:
Request [0, 4, 0, 0] for process 0 approved.
Max Vector: [[4, 4, 1, 3], [4, 4, 1, 4], [4, 4, 1, 1], [4, 4, 1, 3]] 
Allocation Vector: [[4, 4, 1, 3], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] 
Available Vector: [0, 0, 1, 9]
Process Finish Vector: [False, 'Completed', 'Completed', 'Completed']

### Optional Request Denial Messages

#### Message styling: none

Upon request denial, this optional brief message is printed showing the process that made the request and the denied request.

Example:
Request [4, 2, 0, 0] from process 2 denied due to putting system in unsafe state

# Main Data Structures

There can be n resources, where 1 <= n. n will be used in this section to represent the number of resources.

## Allocation Matrix

This matrix represents the currently allocated resources to each Resource User. Indexed by the Resource User ID, each element is a list of length n, with each element representing a resource. The example below shows how to read this matrix. 

                A  B  C  D
process 0 has: [4, 3, 1, 3], 
process 1 has: [0, 0, 0, 4], 
process 2 has: [0, 0, 1, 1], 
process 3 has: [0, 0, 0, 0]

As an example, reading process 0's allocated resources we have: process 0 has 4 of resource A, 3 of resource B, 1 of resource C, 3 of resource D.

## Max Matrix

This matrix represents the resources each Resource User needs to have to complete. Indexed by the Resource User ID, each element is a list of length n, with each element representing a resource. The example below shows how to read this matrix. 

                                      A  B  C  D
process 0 needs to have to complete: [4, 3, 1, 3], 
process 1 needs to have to complete: [0, 0, 0, 4], 
process 2 needs to have to complete: [0, 0, 1, 1], 
process 3 needs to have to complete: [0, 0, 0, 0]

## Available Vector

This vector represents the resources that the Resource Allocator has not allocated yet. The example below shows how to read this vector. 

                             A  B  C  D
The Resource Allocator has: [0, 1, 0, 4]

Reading this out loud we have: The Resource Allocator has 0 of resource A, 1 of resource B, 0 of resource C, 4 of resource D.

## Process Finish Vector

This vector, indexed by Resource User ID, contains the status of the completion of process at that index. There are 3 values: 
- False: Process has not completed
- "Completed": Process recieved all needed resources and completed.
- "Not Completed": Process did not recieve all needed resources and timed out.

Example:
 Process 0     Process 1  Process 2  Process 3
['Completed', 'Completed',  False,  'Completed']

Here, Process 0 completed with needed resources, while Process 2 is still in-progress.

## Process Finish Order

List, read from left-to-right of the order of Users that completed with all needed resources. Example:

[3, 1, 0, 2]

Process 3 completed with all needed resources first, then process 1, then process 0, then process 2.

## Request Queue

The queue that oncoming requests to the Resource Allocator are sent to. Resource Users make requests that are pushed onto the requestQueue. The Resource Allocator will take these requests off the queue for processing. A request in the queue is represented as a tuple.

Example:
[(0, [1,1,2]),(1,[2,1,3])]

In this queue, there are two outstanding requests. The one in the front of the queue is (0, [1,1,2]). This means process 0 is requesting 1 of resource A, 1 of resource B, and 2 of resource C.

## Allocation Response 

This list is an array indexed with the user ID, which the Resource Allocator sends information to each Resource User through. There are 3 values each index can hold.

- True: the last request that the resource user made was granted
- False: the last request that the resource user made was denied
- UNWRITTEN_RESPONSE_FLAG: this is an integer defined in the ResourceUser class. This means that the last request from the ResourceUser has not been processed yet.

Example:
[-1, False, True] where UNWRITTEN_RESPONSE_FLAG = -1

There are three processes. Process 0 is awaiting a response that it has sent to the allocator. Process 1's last request was denied. Process 2's last request was approved.

# Code Guide

ResourceAllocator.py contains the class ResourceAllocator which extends the thread class. Instances of this class are threads that manage resources and processes requests made for resources.

ResourceUser.py contains the class ResourceUser which extends the thread class. Instances of this class are threads that need resources to complete and make requests for resources.

vectors.py contains utility methods to manipulate vectors and matricies.