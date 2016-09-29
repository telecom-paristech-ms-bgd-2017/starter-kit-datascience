import numpy as np
import sys


def sum(a, b=1):
    """Sum two numbers
    """
    return a+b

sum1 = sum(1, 2)  # Add 1 and 2
sum2 = sum(1)  # Add 1 and 1

if len(sys.argv) > 2:
    sum3 = sum(int(sys.argv[1]), int(sys.argv[2]))
else:
    print("You may provide sum arguments")

print("1 + 2 = " + str(sum1))
print("1 + 1 = " + str(sum2))
print(sys.argv[1] + " + " + sys.argv[2] + " = " + str(sum3))

print("""\
Usage: thingy [OPTIONS]
     -h                        Display this usage message
     -H hostname               Hostname to connect to\
""")
