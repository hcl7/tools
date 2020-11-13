import hashlib
import sys
import string
import time
import os

Black = '\x1b[30m'
Red = '\x1b[31m'
Green = '\x1b[32m'
Yellow = '\x1b[33m'
Blue = '\x1b[34m'
Magenta = '\x1b[35m'
Cyan = '\x1b[36m'
White = '\x1b[37m'
Default = '\x1b[39m'
LightGray = '\x1b[90m'
LightRed = '\x1b[91m'
LightGreen = '\x1b[92m'
LightYellow = '\x1b[93m'
LightBlue = '\x1b[94m'
LightMagenta = '\x1b[95m'
LightCyan = '\x1b[96m'
LightWhite = '\x1b[97m'

def clear():
  return os.system('cls' if os.name == 'nt' else 'clear')

def logo():
  clear()
  print (LightBlue + "   ___  _____   _____ _ __  " + Default)
  print (LightBlue + "  / __|/ _ \ \ / / _ \ |_ \ " + Default)
  print (LightBlue + "  \__ \  __/\ V /  __/ | | |" + Default)
  print (LightBlue + "  |___/\___| \_/ \___|_| |_|" + Default)
  print (LightBlue + "                            " + Default)

logo()

def rainbow(n):
  x=1
  allstr = "aA@bB9cC(dDeE3#fF7gG6hHiI1!jJ2kKlLmMnNoO0pPqQ8rR4sS5$tT)uUvVwWxXyYzZ9%&*.=?[]^{}~/\|"
  strlen = len(allstr)
  #allstr = string.letters + string.digits + string.punctuation
  for x in range(x):
    for i in range(strlen):
      if n >= 1:
        a=allstr[i+x]
        yield a
        for i in range(strlen):
          if n >= 2:
            b=allstr[i+x]
            yield a+b
            for i in range(strlen):
              if n >= 3:
                c=allstr[i+x]
                yield a+b+c
                for i in range(strlen):
                  if n >= 4:
                    d=allstr[i+x]
                    yield a+b+c+d
                    for i in range(strlen):
                      if n >= 5:
                        e=allstr[i+x]
                        yield a+b+c+d+e
                        for i in range(strlen):
                          if n >= 6:
                            f=allstr[i+x]
                            yield a+b+c+d+e+f
                            for i in range(strlen):
                              if n >= 7:
                                g=allstr[i+x]
                                yield a+b+c+d+e+f+g
                                for i in range(strlen):
                                  if n >= 8:
                                    h=allstr[i+x]
                                    yield a+b+c+d+e+f+g+h
                                    for i in range(strlen):
                                      if n >= 9:
                                        j=allstr[i+x]
                                        yield a+b+c+d+e+f+g+h+j
                                        for i in range(strlen):
                                          if n >= 10:
                                            k=allstr[i+x]
                                            yield a+b+c+d+e+f+g+h+j+k
                                            for i in range(strlen):
                                              if n >= 11:
                                                l=allstr[i+x]
                                                yield a+b+c+d+e+f+g+h+j+k+l
                                                for i in range(strlen):
                                                  if n >= 12:
                                                    m=allstr[i+x]
                                                    yield a+b+c+d+e+f+g+h+j+k+l+m
                    
def timer():
  now = time.localtime(time.time())
  return time.asctime(now)

def Crack(passwd):
  with open(crackfile, "r") as f:
    for h4sh in f:
      h4sh = h4sh.translate(None, "\n")
      h4shrainbow = hashlib.md5(passwd).hexdigest()
      if h4sh in h4shrainbow:
        print Yellow+"["+h4sh+"]"+Default+"->"+Blue+"["+passwd+"]"+Default
        sys.exit()
      else:
        print Yellow+"["+h4shrainbow+"]"+Default+"->"+Red+"["+passwd+"]"+Default

if len(sys.argv) < 3:
  print LightGreen+"usage: ",sys.argv[0]," <hashfile><pass length>"+Default
else:
  try:
    crackfile = sys.argv[1]
    for rain in rainbow(int(sys.argv[2])):
      Crack(rain)
  except:
    pass

