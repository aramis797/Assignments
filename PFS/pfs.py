import os
from random import randrange
import time

'''
	Some Global constants and variables are defined so that they can be used anywhere in the program

'''

PFS_PATH = "/home/nsm/Desktop/OS_pro/" # Project Path Change accordingly if you want to run
BLOCK_SIZE = 256 #block size as per project
FILE_SIZE = 10240 #filesize as mentioned in project description
BIT_MAP = [0]*40 #used as bit map to find next empty position in disk 0->Free, 1-> allotted(10240/256 = 40 blocks)

global outFile  # output file Pointer "PSFFile"
global directory  # Directory Object


'''
	@desc - Checks if the disk is full by checking with the above BIT_MAP array
	@params void - (uses global variable BIT_MAP)
	@returns bool - checks if all are filled and returns accordingly
'''
def isVolumeFull():
	return BIT_MAP.count(0) == 0


'''
	@desc - Gives an index to an empty block in disk
	@params void - (uses global variable BIT_MAP)
	@returns bool - Returns a randomly picked empty block in disk
'''
def getEmptyBlock():
	while(True):
		rand_index = randrange(0,40)
		if(BIT_MAP[rand_index] == 0):
			return rand_index 


'''
	@desc - Class to represent a block in disk
	@field blockId - unique blockid in disk(0-39) as our scenario contains 40 blocks only
	@field data - data of a file which is at most 256bytes in size
	@field next - pointer to next block if file spans in multiple blocks
'''
class FileBlock():
	def __init__(self,blockId,data,next=None):
		self.blockId = blockId
		self.data = data
		self.next = next
	def __str__(self):
		return "\n" "<=== "+ str(self.blockId) + "||" +  self.data +" || "+ str(self.next) + " ===>"

'''
	@desc - Directory Structure for our PFS
	@field dirFiles - container for FCB(File Control Block) Objects
	@method addFCB(fcb) - takes a FCB and appends it to the dirFiles list
'''
class Directory():
	def __init__(self):
		self.dirFiles = []
	def addFCB(self,fcb):
		self.dirFiles.append(fcb)


'''
	@desc - Represents a FCB(File Control Block)
	@field name - name of the file
	@field size - size of the file
	@filed createTimeAndDate - date and time of creation of that particular file
	@field startingBlockID - block Id from which this file is started in disk
	@field endingBlockID - block Id with which this file will end
	@method __str__ - overload method to utilize in dir command
'''
class FCB():
	def __init__(self,name,size,createTimeAndDate,startingBlockID,endingBlockID,remarks):
		self.name = name
		self.size = size
		self.createTimeAndDate = createTimeAndDate
		self.startingBlockID = startingBlockID
		self.endingBlockID = endingBlockID
		self.remarks = remarks
	def __str__(self):
		return "%10s %10s Bytes %10s %20s"%(self.name ,str(self.size),self.createTimeAndDate,self.remarks)



def putr(command):
	global directory
	fileName = command.split()[1]
	rem = command.split()[2]
	for fcb in directory.dirFiles:
		if(fcb.name == fileName):
			fcb.remarks = rem
			return
	print "INFO: File " + fileName + "Not Found"

'''
	@desc - open command implementation,
			checks if PFSFile present 
				if present opens it in append mode
				else creates, and then opens it in append mode
	@params command - open
'''
def openCommand(command):
	global outFile
	if(not os.path.isfile('PFSFile')):
		f = open('PFSFile','w')
		f.close()
	outFile = open('PFSFile','a')


'''
	@desc - put command implementation
			takes file and allocates memory in disk(i.e PSFFile) in linked allocation manner
	@params command - contains path corresponds to file which is to be put in PSFFile
	@returns bool - checks if all are filled and returns accordingly
'''
def put(command):
	global outFile,directory
	filePath = command.split()[1] # to get file path
	fileStat = os.stat(filePath) # get file properties using os.stat fuctions(i.e datetime,size)
	inpFile = open(filePath) # open file
	fileData = inpFile.read() # read file
	if(isVolumeFull()): # if there are no space in disk
		print "INFO: Sorry Disk Full"
		return
	else:
		startingBlockID = getEmptyBlock() #get an empty block
		previousBlockId = startingBlockID
		BIT_MAP[startingBlockID] = 1 #change status of block to occupied
		blockData = fileData[0:BLOCK_SIZE] # read first 256bytes of data
		remainingDataLength = len(fileData)-BLOCK_SIZE # calculating remaining size of data to be place in PSFFile
		if(remainingDataLength <= 0): #as there is data write to PSFFile by linked allocation method
			outFile.write(str(FileBlock(previousBlockId,blockData,None))) 
		while(not isVolumeFull() and remainingDataLength > 0 ):
			if(isVolumeFull()):# check if volume is full
				print "INFO: Sorry Volume Full"
				return
			else: 
				if(remainingDataLength > 0): # get 256bytes ofdata every time and append it to the PSFFile.
					nextBlockId = getEmptyBlock()
					outFile.write(str(FileBlock(previousBlockId,blockData,nextBlockId)))
					BIT_MAP[nextBlockId] = 1 #change status of the PSFFile
					blockData = fileData[len(fileData)-remainingDataLength:len(fileData)-remainingDataLength+256]
					remainingDataLength -= 256 # decreaseremaining Data
					previousBlockId = nextBlockId
				else:
					outFile.write(str(FileBlock(previousBlockId,blockData,None)))
	#Add that FCB to directory
	directory.addFCB(FCB(filePath.split('/')[-1],fileStat.st_size,time.ctime(fileStat.st_atime),startingBlockID,previousBlockId,""))
	inpFile.close()


def get(command):
	pfsFileName = command.split()[1]
	destinationFile = command.split()[2]
	os.system("cp " + PFS_PATH+pfsFileName +" "+ destinationFile)


'''
	@desc - dir command implementation
	@params command - dir
	@returns void - prints list of files with their name,size,createTimeAndDate
'''
def listdir(command):
	global directory
	print "%10s %15s %10s %20s"%("Name","Size","CreateTimeAndDate","Remarks")
	for fcb in directory.dirFiles:
		print fcb


'''
	@desc - kill command implementation
	@params void - 
	@returns viud - Deletes PFSFile 
'''
def kill():
	directory.dirFiles = []
	os.system("rm " + PFS_PATH+"PFSFile") # os command to remove given file
	print "INFO: PFSFile Removed Successfully!"


'''
	@desc - Driver method to start the file system operation
			Gives "PFS>" prompt and takes commands as long as exit is given
	@params void 
	@returns void
'''
def main():
	global outFile,directory
	directory = Directory()
	while(True):
		print "PFS>\t",
		command = raw_input()
		if(command == "exit"):
			outFile.close()
			print "Shutting Down!"
			break
		elif(command.startswith('open')):
			openCommand(command)
		elif(command.startswith('kill')):
			kill()
		elif(command.startswith('putr')):
			putr(command)
		elif(command.startswith('put')):
			put(command)
		elif(command.startswith('get')):
			get(command)
		elif(command.startswith('dir')):
			listdir(command)
		else:
			print "INFO: Available Commands[open,kill,put,dir]"
if __name__ == '__main__':
	main()