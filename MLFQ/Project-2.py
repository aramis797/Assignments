"""Project.py: Implementation of Multilevel Feedback Queue Implementation."""

__author__      = "Aramis"
__copyright__   = "Copyright 2016, Bridgeport University"
__licence__     = "GPL"
__version__     = "1.0.1"
__email__       = "justganesh12321@gmail.com"


# Queue is a class which works as a general queue(FIFO) with an extra method
# push to insert at other end of the queue
class Queue:
	def __init__(self):
		self.items = []

	#returns true if queue is empty
	def empty(self):
		return self.items == []

	#pushes element at the end of the queue
	def push(self, item):
		self.items.insert(len(self.items),item)

	#puts element at the starting of the queue
	def put(self, item):
		self.items.insert(0,item)

	#removes and returns the end element from the queue
	def get(self):
		return self.items.pop()


#This is the process class which contains all proccess data. we can assume is as a PCB of a process
class Process:
	def __init__(self,process_id,arrival_time,service_time,queue_number=0,turnaround_time=0,response_time=0,waiting_time=0):
		self.process_id = process_id
		self.arrival_time = arrival_time
		self.service_time = service_time
		self.remaining_time = service_time
		self.turnaround_time = turnaround_time
		self.response_time = response_time
		self.waiting_time = waiting_time
		self.queue_time = 4

	#simple print class for printing purpose
	def __str__(self):
		return (str(self.process_id)+":-("+str(self.arrival_time)+","+str(self.service_time)+")")

# Taking queues for our MLFQ
# Queues separately donot posses any special properties.
# everything is configured in the execution only.
Q0 = Queue()
Q1 = Queue()
Q2 = Queue()
Q = Queue()

#our processes
A = Process("P0",0,12)
B = Process("P1",8,25)
C = Process("P2",21,33)
D = Process("P3",30,2)
E = Process("P4",7,12)
F = Process("P5",0,21)
G = Process("P6",12,8)
H = Process("P7",8,19)
I = Process("P8",5,15)
J = Process("P9",19,13)
K = Process("P10",9,19)
L = Process("P11",11,11)
M = Process("P12",30,9)
N = Process("P13",0,1)
O = Process("P14",1,23)
P = Process("P15",39,32)
Q = Process("P16",61,2)
R = Process("P17",12,16)
S = Process("P18",39,18)
T = Process("P19",17,17)

# A list to store all processes
plist = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T]
N = len(plist)
# To sort all proccess according to arrival times.
plist.sort(key=lambda x: x.arrival_time)
#a variable to keep track of completed processes
completed_processes = 0
# to set clock as the first process arrival time.
clock = plist[0].arrival_time
# this loop stops when all processes are completed.
responseOut = []
tatOut = []
waitingOut = []
while completed_processes < N:
	# to get all processes which are arrived in clock time
	arrived = [x for x in plist if x.arrival_time <= clock]
	# To put all arrived processes in to the queue.
	for i in arrived:
		Q0.put(i)
		plist.remove(i)
	#if there is atleast one processes in Q0, below 4 in checking represents its RR quantum
	if not Q0.empty():
		temp = Q0.get() #get processes from Q0
		responseOut.append((temp.process_id,clock-temp.arrival_time))
		print temp.arrival_time,"ms ->",temp.process_id,"is Created.",temp.process_id,"enters Q0.",temp.process_id,"is selected."
		# if its execution time is <=4 the complete its execution and change variables accordingly
		if temp.remaining_time <= 4:
			completed_processes += 1
			temp.turnaround_time += temp.remaining_time
			clock += temp.remaining_time
			tatOut.append((temp.process_id,clock-temp.arrival_time,temp.service_time))
			print clock,"ms ->",temp.process_id,"is Completed"
		#otherwise reduce its remaining time and move the process into the Q1 with queue_time as 8. 
		else:
			temp.remaining_time -= 4
			clock += 4
			print clock,"ms ->",temp.process_id,"is Aged.",temp.process_id,"moves to Q1."
			temp.queue_time = 8
			Q1.put(temp)
	# if there is atleast one process in Q1(but not in Q0)
	elif not Q1.empty():
		temp = Q1.get()
		#print temp.remaining_time,temp.queue_time,clock
		print clock,"ms ->",temp.process_id,"is selected in Q1."
		#this try block is used to check if any new process arrives before a process 8 unit of time then that is placed into Q0
		# and current process is preemptied
		try:
			nextArrTime =  plist[0].arrival_time - clock
			if nextArrTime < temp.queue_time:
				clock += nextArrTime
				temp.queue_time = temp.queue_time - nextArrTime
				temp.remaining_time = temp.remaining_time - nextArrTime
				# print temp.remaining_time,temp.queue_time,clock
				Q1.push(temp)
				Q0.put(plist[0])
				plist.remove(plist[0])
				continue
		# above is put in try block because of plist array (if it is empty.)
		# if nothing is arriving before its 8 units of time then execute it and move that process into Q2
		except:
			temp.remaining_time -= temp.queue_time
			clock += temp.queue_time
			if temp.remaining_time > 0:
				print clock,"ms ->",temp.process_id,"is Aged.",temp.process_id,"moves to Q2."
				temp.queue_time = 12
				Q2.put(temp)
			else:
				completed_processes += 1
				tatOut.append((temp.process_id,clock-temp.arrival_time,temp.service_time))
				print clock,"ms ->",temp.process_id,"is Completed"
		else:
			temp.remaining_time -= temp.queue_time
			clock += temp.queue_time
			if temp.remaining_time > 0:
				print clock,"ms ->",temp.process_id,"is Aged.",temp.process_id,"moves to Q2."
				temp.queue_time = 12
				Q2.put(temp)
			else:
				completed_processes += 1
				tatOut.append((temp.process_id,clock-temp.arrival_time,temp.service_time))
				print clock,"ms ->",temp.process_id,"is Completed"
	# if there is process in Q2(but not in above two queues)
	elif not Q2.empty():
		temp = Q2.get()
		print clock,"ms ->",temp.process_id,"is selected in Q2."
		#same as above for checking early arrival of new processes
		try:
			var = plist[0].arrival_time - clock;
			if var < 12 :
				clock += var
				temp.queue_time -= var
				temp.remaining_time -= var
				Q2.push(temp)
				Q0.put(plist[0])
				plist.remove(plist[0])
				continue
		# if process burst time is <= 12 then execute it completely else make RR12 in Q2
		except:
			if temp.remaining_time <= 12:
				clock += temp.remaining_time
				completed_processes += 1
				tatOut.append((temp.process_id,clock-temp.arrival_time,temp.service_time))
				print clock,"ms ->",temp.process_id,"is completed"
				continue
			temp.remaining_time -= temp.queue_time
			clock += temp.queue_time
			if temp.remaining_time > 0:
				print clock,"ms ->",temp.process_id,"is Aged.",temp.process_id,"moves to Q2."
				temp.queue_time = 12
				Q2.put(temp)
			else:
				completed_processes += 1
				tatOut.append((temp.process_id,clock-temp.arrival_time,temp.service_time))
				print clock,"ms ->",temp.process_id,"is Completed"
		else:
			temp.remaining_time -= temp.queue_time
			clock += temp.queue_time
			if temp.remaining_time > 0:
				print clock,"ms ->",temp.process_id,"is Aged.",temp.process_id,"moves to Q2."
				temp.queue_time = 12
				Q2.put(temp)
			else:
				completed_processes += 1
				tatOut.append((temp.process_id,clock-temp.arrival_time,temp.service_time))
				print clock,"ms ->",temp.process_id,"is Completed"
# print responseOut
# print tatOut
for p in tatOut:
	waitingOut.append((p[0],p[1]-p[2]))
# print waitingOut
avgWait = 0
avgTat = 0
avgResponse = 0
for i,j,k in zip(waitingOut,tatOut,responseOut):
	avgWait += i[1]
	avgTat += j[1]
	avgResponse += k[1]
print "_____________________________"
print "Average Waiting Time:- %s \nAverage TurnAround Time:- %s \nAverage Response Time:- %s\n"%(avgWait/float(N),avgTat/float(N),avgResponse/float(N))
