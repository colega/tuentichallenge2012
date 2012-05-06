import sys;
from Hamming import Hamming;
def bit(data,i):
	return int(data[i]);

def hamming(data):
	b = [int(v) for v in list(data)]
	p1 = b[1]^b[2]^b[4]^b[6]
	p2 = b[2]^b[5]^b[6]
	p3 = b[4]^b[5]^b[6]
#	print p1,p2,p3
#	if (p1+p2+p3 == 1):
#		print p1,p2,p3,"  ";
	if (p1 and p2 and not p2):
		b[2] = 1-b[2];
	elif (p1 and not p2 and p3):
		b[4] = 1-b[4];
	elif (not p1 and p2 and p3):	
		b[5] = 1-b[5];
	elif (p1 and p2 and p3):
		b[6] = 1-b[6];
	s = [str(v) for v in b]
	return int(s[2]+s[4]+s[5]+s[6],2)

def main():		
	s = 0;
	for line in sys.stdin:
		d = line.strip();
		
		for i in range(len(d)/7):
			if (i % 2 == 0):
				b = hamming(d[i*7:(i+1)*7]);
			else:
				b = b << 4 | hamming (d[i*7:(i+1)*7]);
				print chr(b),
#				print bin(b);
		print len(d);
	
if __name__ == '__main__':
	main();
