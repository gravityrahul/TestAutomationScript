import subprocess

logfile = open("ps_ef.log","w")

def getpsefStatus(logFileName):
    #psef = subprocess.Popen(['ps', '-ef'], stdout=logfile).communicate()[0]
    psef = subprocess.Popen(['ps', '-ef'], stdout=logFileName)
    ret_code = psef.wait()
    logfile.flush()
    return ret_code	 
    #for proc in processes:
#	print proc
#    return True

if __name__=="__main__":
   	getpsefStatus(logfile)
