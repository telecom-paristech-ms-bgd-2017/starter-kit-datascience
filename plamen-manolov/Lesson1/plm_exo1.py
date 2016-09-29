import sys
def main():
	print ("Hello")
	print (" sys.argv : " , sys.argv)
	Hello(sys.argv[1])

def Hello(name):
	if name == 'Alice':
		print("Alert: Alice mode")
		name = name + " ?????"
	else:
		print("Else")
	name = name + "!!!!!"
	print ("Hello" , sys.argv[0] , name)


main()
