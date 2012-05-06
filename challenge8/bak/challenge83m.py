import sys;
import md5;
from itertools import groupby;
from multiprocessing import Process, Queue;
from operator import itemgetter;
import time;


class Transformation:
	def __init__(self,s):
		self.l = []
		for c in s:
			self.l += [[c,1]]

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
	
	
	lengths = [max([len(v) for v in a.values()]) for i,a in enumerate(adjustments)];
	better = True;
	while better:
#		print lengths;
		better = False;
		if (len(adjustments)>1):
			cl = sorted([(i,lengths[i]*lengths[i+1]) for i in range(len(lengths)-1)], key=itemgetter(1));
#			print cl;
			if (cl[0][1] < pow(2,16)):
				i = cl[0][0];
#				print "let's remove",i,i+1;
				na = adjustments[:i];
				nadj = adjustments[i];
				adj = adjustments[i+1];
				for t in adj:
					for a in nadj:
						nadj[a] = nadj[a].replace(t,adj[t]);
					if t not in nadj.keys():
						nadj[t] = adj[t];
				better = True;
				na.append(nadj);
				try:
					na += adjustments[i+2:];
				except:
					pass;
				adjustments = na;
	
		lengths = [max([len(v) for v in a.values()]) for i,a in enumerate(adjustments)];
		lf = open('lengths', 'a');
		lf.write(str(lengths)+"\n");
		lf.close();
	
#	na = [];
#	j = 0;
#	if (len(adjustments) % 2 == 1):
#		na.append(adjustments[0]);
#		j=j+1;
#	while (j<len(adjustments)):
#		nadj = adjustments[j];
#		adj = adjustments[j+1];
#		for t in adj:
#			for a in nadj:
#				nadj[a] = nadj[a].replace(t,adj[t]);
#			if t not in nadj.keys():
#				nadj[t] = adj[t];
#		j+=2;
#		na.append(nadj);
#	
#	adjustments = na;
#
#	lengths = [max([len(v) for v in a.values()]) for i,a in enumerate(adjustments)];
#	lf = open('lengths', 'w');
#	lf.write(str(lengths));
#	lf.close();
		
	
	hasher = md5.new();
	s = [queueString]+['']*len(adjustments);
				
	i = 0;
	count = 0;
	lastc = 0;
	lastcount = 0;
	lasttime = time.time();
	adjustmentsLength = len(adjustments);
	while True:		
		if (len(s[i]) == 0):
#			print "no more chars on line",i
			i=i+1;
		else:
			# If there are no more adjustments,process the char
			if (i>=adjustmentsLength):
#				print s,s[i][0],type(s[i][0]);
				hasher.update(s[i]);
				count += len(s[i]);
				if (count / 10000000 > lastc):
					lastc = count/10000000;
					f = open('out','a');
					newtime = time.time();
					speed = (count-lastcount)/(newtime-lasttime);
					f.write(str(count)+" "+str(len(s[0]))+" "+str(sum([len(v) for v in s]))+time.ctime(time.time())+' Speed:'+str(speed)+'\n');
					lasttime = newtime;
					lastcount = count;
					f.close();
				s[i] = '';
				if (not s[0]):
					if (sum([len(v) for v in s]) == 0):
						break;
				while not s[i]:
					i-=1;
			# There are more levels
			else:
				# If there are characters on the next line, we don't need to add more
				# We don't even want to have two characters, because it would need the concatenation operation
				if(s[i+1]):
#					print "No more chars needed on the line ",i+1;
					i=i+1;
				else:
					# We need more chars, this is the case if there's a rule for it
					try:
						s[i+1] = adjustments[i][s[i][0]];
					# There is no rule for it
					except:
						s[i+1] = s[i][0];
					s[i] = s[i][1:];
					i=i+1;
			
	print hasher.hexdigest();
		
		
		
if __name__ == '__main__':
	main();
