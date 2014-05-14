from subprocess import Popen
import sys
import time


class LaunchCommands(object):

    def __init__(self, fileHandle):
        self.fileHandle = fileHandle


    def Launch(self, cmd, stepName, testName, timeout_secs=30, no_timeout=False, isTask=False):


        ptfstdout = sys.stdout
        ptfstderr = sys.stderr
        ptfstdin = sys.stdin

        self.executable = cmd

        self.fileHandle.write("------------------------------------------------\n")
        self.fileHandle.write(" Test Name [%s]\n" % testName)
        self.fileHandle.write("------------------------------------------------\n")

        if isTask:
            self.fileHandle.write("------------------------------------------------\n")
            self.fileHandle.write(" Test Step [%s] Test Task : %s \n\n" % (stepName, self.executable))
            self.fileHandle.write("------------------------------------------------\n")

        else:
            self.fileHandle.write("------------------------------------------------\n")
            self.fileHandle.write(" Test Step [%s] \n\n" % stepName)
            self.fileHandle.write("------------------------------------------------\n")

        self.cmd = "python {0}".format(cmd)

        process = Popen(self.cmd, stdout=ptfstdout, stderr=ptfstderr, stdin=ptfstdin, shell=True)

        start = time.time()
        now = start
	self.fileHandle.write("START TIME seconds [%s] \n" % time.ctime())
        time_out = start + timeout_secs
        while process.returncode is None:
            if not no_timeout and now >= time_out:
                break
            time.sleep(0.001)   # avoid 100% cpu utilization
            process.poll()
            now = time.time()
        if process.returncode is not None:
            retval = process.returncode
            self.fileHandle.write("%f seconds remained \n" % (time_out - now))
        else:
            self.fileHandle.write("%s --> timed out after %f seconds\n" % (self.executable, now - start))
            process.terminate()
            retval = None
            self.fileHandle.write("stdout=[%s] stderr=[%s]\n" % process.communicate())
        if 0 == retval:
		self.fileHandle.write("END TIME seconds [%s] \n" % time.ctime())
                self.fileHandle.write("%s --> succeeded after %f second \n" % (self.executable, now - start))
                self.fileHandle.write(" RESULT: PASS\n")
                self.fileHandle.write("------------------------------------------------\n")
                self.fileHandle.write("------------------------------------------------\n")
        else:
            self.fileHandle.write("'%s' RESULT: FAILED \n" % self.executable)
            self.fileHandle.write("'%s' ==== ERROR =====\n" % self.executable)
            self.fileHandle.write("stdout=[%s] stderr=[%s]\n" % process.communicate())
            self.fileHandle.write("------------------------------------------------\n")
            self.fileHandle.write("------------------------------------------------\n")
        return retval
