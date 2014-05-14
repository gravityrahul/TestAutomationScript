#!/usr/bin/env/python
"""
author: Rahul Biswas
date: 05/12/14

"""

import os
import sys
from optparse import OptionParser
from lib import cmdLaunch, threadLaunch, readTestObject
import subprocess
from contextlib import contextmanager
from Queue import Queue
from multiprocessing import Process
import time
import commands	

try:
   from matplotlib import pylab
except ImportError:
   print >> sys.stderr, "Couldn't import matplotlib, Please install matplotlib"
   print >> sys.stderr, ""	
   sys.exit(1)


try:
   import numpy as np
except ImportError:
   print >> sys.stderr, "Couldn't import numpy, Please install Numpy"
   print >> sys.stderr, ""	
   sys.exit(1)

parser = OptionParser()
parser.add_option("-f", "--file", default = './test_definition.tdf', help="Test definition file for running the tests", metavar="FILE")
parser.add_option("-t", "--testfolder", default = './integration', help="Test Folder", metavar="TEST FOLDER")

(options, args) = parser.parse_args() 

fileHandle = None
cmdLaunchInstance = None


class Run(object):

        """
        The run module which will actually schedule the runs for a given test case.  The 
        run will actually identify each test steps inside  a given test case and queue it to run.
        """

	def __init__(self, tdfFile, testFolder):
            """
            params: testdefinition file tdfFile
            """
            global fileHandle, cmdLaunchInstance, Status

            self.testfolder = testFolder
            self.tdfFile = os.path.join(testFolder, tdfFile)
            summaryFile = filenamewithTimeStamp('summary.txt', testFolder)
            self.testCaseObj =  readTestObject.parseTestFiletoDict(self.tdfFile)
            fileHandle = open(summaryFile, 'w')
            cmdLaunchInstance = cmdLaunch.LaunchCommands(fileHandle)

	def StartRun(self):
          
	    #time.sleep(5.0)	
            print "======================================================================\n"
            print "===             STARTING TEST EXECUTION ==============================\n"
            print "======================================================================\n"
            print "Running ps -ef command before the execution"
	    time.sleep(5.0)
            end_filename =  filenamewithTimeStamp('psBefore.txt', self.testfolder)
            getpsefStatus(end_filename)
	    self.ScheduleRunPerTestCase()


	def StopRun(self):

	    #global Status	
            print "======================================================================\n"
            print "===      END OF TEST EXECUTION ==============================\n"
            print "======================================================================\n"
	    print "Running ps -ef command after the execution"
            end_filename =  filenamewithTimeStamp('psAfter.txt', self.testfolder)
            getpsefStatus(end_filename)
	    #Status = False			


	def ScheduleRunPerTestCase(self):
            """
            Puts test cases in the queue
            params:  None
            """
            testCaseKeys = self.testCaseObj.keys()
            testCaseKeys.sort()
            for testCaseKey in testCaseKeys:
                self.ScheduleRunPerTestStep(testCaseKey)


        def ScheduleRunPerTestStep(self, testcasekey):
            """
            Schedule run per test steps in a test case
            """
            global cmdLaunchInstance

            qcID = self.testCaseObj.get(testcasekey).get('qcId').encode()
            tcID =  self.testCaseObj.get(testcasekey).get('tcID').encode()
            tcName =  self.testCaseObj.get(testcasekey).get('tcName').encode()
            testStepsKeys =  self.testCaseObj.get(testcasekey).get('testSteps').keys()
            # Sort the Keys
            testStepsKeys.sort()

            print "======================================================================\n"
            print "Executing Test Case : %s " %tcName
            print "               qcId : %s " %qcID
            print "               tcId : %s " %tcID
            print "======================================================================\n"

            for testStepKey in testStepsKeys:
                testStepName = self.testCaseObj.get(testcasekey).get('testSteps').get(testStepKey)
                if not isinstance(testStepName, list):
                    cmd = testStepName.encode()
                    print "--------------------------------------------------------------\n"
                    print "Executing Test Step %s: %s " %(testStepKey, cmd)
                    print "--------------------------------------------------------------\n"
                    cmdLaunchInstance.Launch(cmd, testStepKey, tcName)
                else:
                    print "--------------------------------------------------------------\n"
                    print "Executing Test Step: %s "% testStepKey
                    print "Test Step has more than one Tasks: exectuting Test Step: ", testStepName
                    print "--------------------------------------------------------------\n"
                    testName = testStepKey
                    cmds = testStepName
                    threadLaunch.GenerateThreadRun(testStepKey, cmds, tcName, fileHandle)
                    print "--------------------------------------------------------------\n"


def filenamewithTimeStamp(filename, folder):
    t = time.localtime()
    filename = '%s-%d-%d-%d-%d:%d:%d' %(filename, t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)   
    filename = os.path.join(folder, filename)
    return filename


def getpsefStatus(logFileName):
    logfile = open(logFileName, 'w')
    psef = subprocess.Popen(['ps', '-ef'], stdout=logfile)
    ret_code = psef.wait()
    logfile.flush()
    logfile.close()	
    return 0



if __name__=="__main__":
       
        Status = True

	tdfFile =options.file
        testfolder = options.testfolder 

	def runnerFunction():
	   	
	    RunObject = Run(tdfFile, testfolder)	
	    RunObject.StartRun()	
	    RunObject.StopRun()	
	    		

 
	def RunMemoryTracker():
	    """
	    Context manager class to run Memory Usage from start to end
	    """
            print "<<<  ===== Tracking Memory Started ====== >>>"
	    timeArray=[]	
	    memFreeArray=[]	
            for i in range(20):
		t = time.clock()
		timeArray.append(t)	
            	time.sleep(1)
	   	
              	output = commands.getoutput('vmstat -S M')
                lines = output.split('\n') 
		freeMem = lines[2].split()[3]
		memFreeArray.append(freeMem)
	 
	    print "<<<  ===== Tracking Memory Ended ====== >>>"	

    	    timeNpArray = np.asarray(timeArray)
	    memFreeNpArray = np.asarray(memFreeArray)	
            print "Generating Plot of Time vs Free Memory"
		
	    pylab.plot(timeNpArray, memFreeNpArray)
	    pylab.xlabel('Clock Time (sec)')
	    pylab.ylabel('Free Memory (MB)')
	    pylab.grid(True)
            pylab.show()
            pylab.savefig('memory_performance.png')
	  					   
	    return 	
	     


	proc = []
	fns = [runnerFunction, RunMemoryTracker]
        pids = []
  	for fn in fns:
    	   p = Process(target=fn)
    	   p.start()
    	   proc.append(p)
	   pids.append(p.pid)	 	

  	for p in proc:
    	   p.join()
	
	
      

