#!/usr/bin/env python
import sys
import getopt
import operator

class ProgressiveCipher:

	def __init__(self, mode, msg):
		self.msg = msg
		if mode == '-e':
			self.l = self.str2num()
			#print self.l
			self.c = self.penc(self.l)
			self.cipher = ' '.join(self.c)
			#print "encrypted!"
		if mode == '-d':
			self.c = self.pdec(self.msg)
			self.cipher = self.num2str(self.c)
			#print "decrypted!"
	
	def xgcd(self, a, b):
		if a == 0:
			return b, 0, 1
		else:
			g, y, x = self.xgcd(b % a, a)
        	return g, x - (b // a) * y, y
		
	def str2num(self):
		return [ ord(chars) for chars in self.msg ]

	def num2str(self, l):
		return ''.join(map(chr, l))
	
	def penc(self, m):
		n = len(m)
		c = []
		for i in range(n):
			k = self.xgcd(i+n, 255)[1]%255
			y = (m[i]+(k*(1+i)))%255
			c.append(self.dec2hex(y))
		return c
	
	def pdec(self, c):
		c = c.split()
		n = len(c)
		m = []
		for i in range(n):
			dec = self.hex2dec(c[i])
			k = self.xgcd(i+n, 255)[1]%255
			y = (dec-(k*(1+i)))%255
			m.append(y)
		return m

	def dec2hex(self, dec):
		return hex(dec).split('x')[-1]

	def hex2dec(self, hex):
		return int(hex, 16)
	
	def getcipher(self):
		return self.cipher

if len(sys.argv) < 3:
	print sys.argv[0], '<-e|-d> <message>'
else:
	a = ProgressiveCipher(sys.argv[1], sys.argv[2])
	print a.getcipher()

