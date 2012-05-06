import sys;
import md5;
from itertools import groupby;
from multiprocessing import Process, Queue;
from operator import itemgetter;
import time;

def processWithQueues(h,q,a,level):
	la = len(a);
	while level < len(a):
		nq = '';
		if (len(q) > 1024):
			for c in q:
#				print "calling processWithQueues(",h,c,"a",level,")";
				processWithQueues(h,c,a,level);
			break;
		else:
			for c in q:
				try:
					nq+=a[level][c]
				except:
					nq+=c;
#			print "q = nq",q,"=",nq
			q = nq;
			level+=1;
			if (level==la):
#				print "hashing",q
				h.update(q);
				
			

def main():
	maxQueueStringSize = 1024*1024;
	maxProcesses = 8;
	
	queueString = sys.stdin.next().strip();
	queueLength = len(queueString);
	queueList = [queueString[i*maxQueueStringSize:min(queueLength,(i+1)*maxQueueStringSize)] for i in range(queueLength/maxQueueStringSize+1)];

	adjustments = [];
	for line in sys.stdin:
		parsed = line.strip().split(',');
		transformations = dict();
		for transformation in parsed:
			splitted = transformation.split('=>');
			transformations[splitted[0]] = splitted[1];
		adjustments.append(transformations);
	

	hasher = md5.new();
	oldtime = time.time();
	for i,c in enumerate(queueString):
		processWithQueues(hasher,c,adjustments,0);
#		if (i % 255 == 0):
#			newtime = time.time();
#			speed = 255/(newtime-oldtime);
#			print "Processed ",i,speed
#			oldtime = newtime;
#			f = open('speed','a');
#			f.write('i=%d,speed=%5.2f \n'%(i,speed));
#			f.close();
	print time.time()-oldtime;
	print hasher.hexdigest();
		
		
if __name__ == '__main__':
	main();
