import time


def function():

    print "Hello There, I am gonna do some Math"
    time.sleep(0.5)
    sumRange(20)
    time.sleep(0.5)
    print "Hello There, I am Done, Good Bye "


def sumRange(n):
    summ = 0
    for i in range(1, n):
        summ += i
    print "The sum of %d first numbers = %d" %(i, summ)

if __name__ == "__main__":
    function()
