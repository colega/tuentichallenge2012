import sys;
import md5;
import time;
from itertools import groupby;
from multiprocessing import Process, Queue, Event;
from operator import itemgetter;

def feedProcessor(s,qout,nextFinished):
	i = 0;
	lasti = 0;
	while (i < len(s)):
		while(qout.qsize()>1024*1024):
			pass;
		qout.put(s[i]);
		i = i+1;
		f = open('outs','a');
		f.write(str(i)+ ' '+time.ctime(time.time())+' '+str(time.time())+'\n');
		f.close();
	nextFinished.set();
		

def stageProcessor(qin, qout, adj, finished,nextFinished):
	while (not finished.is_set() or qin.qsize() > 0):
		while (qout.qsize() > 1024*1024):
			pass;
		data = qin.get()
		for c in data:
			try:
				qout.put(adj[c]);
			except:
				qout.put(c);
	nextFinished.set();

def hashProcessor(qin,finished):	
	hasher = md5.new();
	count = 0;
	lastcount = 0;
	lasttime = time.time();
	lastc = 0;
	while (not finished.is_set() or qin.qsize() > 0):
		try:
			e = qin.get(True,1);
			hasher.update(e);
			count += len(e);
			if (count / 100000 > lastc):
				lastc = count/100000;
				f = open('out','a');
				newtime = time.time();
				speed = (count-lastcount)/(newtime-lasttime);
				f.write(str(count)+time.ctime(newtime)+' Speed:'+str(speed)+'\n');
				lasttime = newtime;
				lastcount = count;
				f.close();
		except:
			pass;
	print hasher.hexdigest();

def main():
	maxProcesses = 8;
	
	queueString = sys.stdin.next().strip();
	queueLength = len(queueString);
	#queueList = [queueString[i*maxQueueStringSize:min(queueLength,(i+1)*maxQueueStringSize)] for i in range(queueLength/maxQueueStringSize+1)];
#	print "queue:",queueString;
	adjustments = [];
	for line in sys.stdin:
		parsed = line.strip().split(',');
		transformations = dict();
		for transformation in parsed:
			splitted = transformation.split('=>');
			transformations[splitted[0]] = splitted[1];
		adjustments.append(transformations);
	
	hasher = md5.new();
	s = [queueString]+['']*len(adjustments);
	
	q = [];
	e = [];
	p = [];
	for i in range(len(adjustments)+1):
		q.append(Queue());
		e.append(Event());
		
	feeder = Process(target=feedProcessor, args=(queueString, q[0], e[0]));
	feeder.start();
	for i in range(len(adjustments)):
		process = Process(target=stageProcessor, args=(q[i],q[i+1],adjustments[i],e[i],e[i+1]));
		process.start();
		p.append(process);
	hasher = Process(target=hashProcessor, args=(q[len(adjustments)],e[len(adjustments)]));
	hasher.start();
		
if __name__ == '__main__':
	main();
