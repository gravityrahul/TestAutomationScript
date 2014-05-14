#!/usr/bin/env python
import Queue
import threading
from cmdLaunch import LaunchCommands
import time
import sys


LaunchInstance = None
StepName = None

queue = Queue.Queue()

cmds = ["./integration/testStepSQLTest01.py", 
        "./integration/testStepSQLTest02.py", 
        "./integration/testStepSQLTest03.py"]


queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

exitFlag = 0

class RunThread (threading.Thread):
	def __init__(self, threadID, q):
           threading.Thread.__init__(self)
           self.threadID = threadID
           self.q = q
	def run(self):
           self.runCmd(self.q)



	def runCmd(self, q):
            global LaunchInstance, StepName, TestName
            while not exitFlag:
		queueLock.acquire()
                #print "processing Thread - %s" %name
		if not workQueue.empty():
                    #print "%s processing %s" % (name, cmd)		
                    cmd = q.get()
		    print "Processing Command ---> %s" % (cmd)
                    LaunchInstance.Launch(cmd, StepName, TestName, isTask=True)
                    queueLock.release()
		else:
                    queueLock.release()


global_start = time.clock()
now = global_start

class GenerateThreadRun(object):

    def __init__(self, stepname, cmds, testName, fileHandle):
	global threadID, workQueue, queueLock, threads, exitFlag, LaunchInstance, StepName, TestName
	self.cmds = cmds
	LaunchInstance = LaunchCommands(fileHandle)
	StepName = stepname
        TestName = testName
 
	# Create new threads
	for i in range(len(cmds)):
	   # tName =i 
	    self.thread = RunThread(threadID, workQueue)
	    self.thread.start()
	    threads.append(self.thread)
	    threadID += 1
	self.runthreads()

    def runthreads(self):
   
	global exitFlag
	# Fill the queue
	queueLock.acquire()

	# Put the commands
	for cmd in cmds:
    	    workQueue.put(cmd)
	queueLock.release()

	# Wait for queue to empty
	while not workQueue.empty():
    	    pass

	# Notify threads it's time to exit
	exitFlag = 1

	# Wait for all threads to complete
	for t in threads:
    		t.join()
         
	
	print "Exiting Main Thread"
	global_te = time.clock() - global_start
	print "Time Elapsed in Total: %f" % global_te



#if __name__=="__main__":
#	stepname = "Test Step02"
#	fileHL = open('summary.txt','w')
#	GenerateThreadRun(stepname, cmds, fileHL)

