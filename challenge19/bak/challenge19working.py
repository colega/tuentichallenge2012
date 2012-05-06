import sys;
import fileinput;
from base64 import b64decode,b64encode;
import binascii

def str2bin(s):
	b = '';
	for c in s:
		b+=bin(ord(c))[2:].zfill(8);
	return b;

def bin2str(b):
	s = '';
	for i in xrange(len(b)/8):
		s+=chr(int(b[i*8:(i+1)*8],2));
	return s;


def main():
	inputs = '';
	for line in sys.stdin:
		inputs+=line.strip();
	outputs = '';
	for line in fileinput.input('sample_output'):
		outputs+=line.strip();
	outputs+='==';
	print "";
		
	ihex = b64decode(inputs);
	istr = binascii.unhexlify(ihex);
	ibin = str2bin(istr);
	
	ohex = b64decode(outputs);
	ostr = binascii.unhexlify(ohex);
	obin = str2bin(ostr);
	
	print ibin;
	
	numbers = [int('0'+v.strip(),2) for v in ibin.replace('10111100011110011111000', ' ').split(' ')][1:];
	
	
	ibinc = ibin.replace('10111100011110011111000', ' ');
	obinc = obin.replace('110111100011110011111000', '\n1\033[90m10111100011110011111000\033[0m');

	result = dict();
	obinclines = obinc.split('\n')[1:];
	obincparsed = '';
	fix = '1\033[90m10111100011110011111000\033[0m';
	for line in obinclines:
		p = '   ';
		l = line.replace('1\033[90m10111100011110011111000\033[0m', '');
		num = l[:9];
		result[num]=[num];
		l = l[9:];
		i = 0;
		while (i < (len(l)/6)):
			result[num]+=[l[i*6:(i+1)*6]];
			i+=1;
		if (l[(i)*6:]):
			result[num] += [l[(i)*6:]];
	
	
	
	lastnum = 0;
	processednumbers = {0:['100000011']};
	for i in range(len(numbers)-1):
		if (abs(numbers[i]-numbers[i+1]) > int('10000', 2) or -int('10000',2) == numbers[i]-numbers[i+1]):
			lastnum +=1;
			processednumbers[lastnum]=[bin(numbers[i+1])[2:].zfill(9)];
		else:
			processednumbers[lastnum]+=[bin(numbers[i+1])[2:].zfill(9)];
			
	output = '';
	for num in processednumbers:		
		output += '\033[94m';
		for i,enigma in enumerate(result[processednumbers[num][0]]):
			output += enigma+' ';
		output+= '\033[0m\n';
		for i in range(len(processednumbers[num])-1):
			intrest =int(processednumbers[num][i],2)-int(processednumbers[num][i+1],2);
			rest = bin(intrest)[2:] if intrest > 0 else '-'+bin(intrest)[3:]
			output += '\033[91m'+processednumbers[num][i] + '\033[0m -> ' + rest + ' -> \033[91m';
		output += processednumbers[num][len(processednumbers[num])-1];
		output += '\033[0m\n';
		output += '\n';
	
#	print output;	
	
	final = '';
	bin10000 = int('10000',2);
	for num in processednumbers:
		# Its not a continuation
		final += '1';
		# Fixed part
		final += '10111100011110011111000';
		final += processednumbers[num][0];
		i = 1;
		while i<len(processednumbers[num]):
			intDiff =int(processednumbers[num][i-1],2)-int(processednumbers[num][i],2);
			if (intDiff<=0):
				diff = bin(abs(intDiff))[2:];
				# 0 stands for "continue"
				# 0 stands for negative difference
				diffString = '00'+diff.zfill(4);
				final+=diffString;
				if (num == '100001010'):
					print "intdiff:",intDiff, diffString;
			else:
				diff = bin(bin10000-intDiff)[2:];
				# 0 stands for "continue";
				# 1 stands for positive difference
				diffString = '01'+diff.zfill(4);
				final+=diffString;
			i+=1;
#	print final;
	ok = '';
	for i,c in enumerate(final):
		if (final[i]==obin[i]):
			ok+=c;
		else:
			print "error at ",i,"that is ",final[i]," and must be ",obin[i];
			break;
#	print ok.replace('10111100011110011111000', '\033[90m10111100011110011111000\033[0m');
#	print final;
	finalhex = binascii.hexlify(bin2str(final));
	finalb64 = b64encode(finalhex);
#	print finalb64;
			
			
			
if __name__ == '__main__':
	main();
