import sys;
import fileinput;
import binascii
from multiprocessing import Process, Queue, Event
from Crypto.Cipher import DES,AES
from time import time

# Checking if it's an ASCII string with characters under 128
def isCorrect(s):
	for c in s[:20]:
		if (ord(c) > 127):
			return False;
	return True;

# Remove padding as in RFC 1423 (thanks for the tip, but it just made me the things more difficult)
def removePadding(ts):
	i = 0;
	ns = '';
	while i < len(ts):
		if (ord(ts[i])>=32):
			ns+=ts[i];
			i+=1;
		else:
			i+=ord(ts[i]);
	return ns;

# Function for processes. Makes brute force over DES with "weak" keys
# By the way, "weak" keys has a special meaning
def keysFinder(message, games, queue, found):
	binmessage = binascii.unhexlify(message);
	chars = range(48, 58, 2)  + range(97, 123,2);
	charsCount = len(chars);
	gamesCount = len(games);
	g = 0;
	boolFound = False;
	while (g < gamesCount and not found.is_set()):
		# if ((g << 5) & 1 > 0):
		# boolFound = ;
		bingame = binascii.unhexlify(games[g]);
		i = 0;
		gameDecrypted = False;
		while (i < charsCount and not gameDecrypted):
			j = 0;
			while (j < charsCount and not gameDecrypted):
				k = 0;
				while (k < charsCount and not gameDecrypted):
					l = 0;
					while (l < charsCount and not gameDecrypted):
						key = chr(chars[i])+chr(chars[j])+chr(chars[k])+chr(chars[l]);
						x = DES.new(key+'0000');
						dec = x.decrypt(bingame);
						# If it starts with Key= search for Puzzle
						if (dec[:4] == 'Key='):
							if (dec.count('Puzzle')>0):
								gameDecrypted = True;
								# Try this key to decrypt the message, if it decrpyts, stop all other threads
								puzzlekey = dec.split(' & ')[0].split('=')[1];
								x = AES.new(puzzlekey);
								dec = x.decrypt(binmessage);
								if (isCorrect(dec)):
									found.set();
									queue.put(removePadding(dec.strip()));
						l += 1;
					k += 1;
				j += 1;
			i += 1;
		g += 1;

def main():
	# Threads we will use, don't change this because each thread calculates keys for 100 games exactly
	# (You can change this if you know how, I'm too euphoric now to do more flexibility)
	start = time();
	threads = 10;
	for line in sys.stdin:
		# Parsing the stdin
		encryptedMessage,encryptedGames = line.strip().split(':');
		encryptedGames = encryptedGames.split('~');
		# Queue with decrpyted message
		q = Queue();
		found = Event();
		# Threads
		for i in range(10):
			p = Process(target=keysFinder, args=(encryptedMessage, encryptedGames[i*100:(i+1)*100],q, found));
			p.start();
		message = q.get();
		found.set();
		print message;

	if (sys.argv[1] == 'benchmark'):
		print "Time elapsed: ",time()-start;
		
				
if __name__ == '__main__':
	main();
