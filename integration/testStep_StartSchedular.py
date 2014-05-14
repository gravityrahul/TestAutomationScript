# This is a basic Testcase SchedularTest
# This test will make sure all the environment for the entire test case has
# correct information.
import sys
import time


def function():

    print "Hello World !! Running Schedular Test"
    print "You gotta wait till I am Done"
    time.sleep(1.5)
    print "Done"


if __name__ == "__main__":
    function()
