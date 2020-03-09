#read files path from xml file
from xml.dom import minidom
import sys

def readTab(filename, tag):
   wf = open("databoxAll.txt", "w+")
   print "[+] reading xml!"
   xml = minidom.parse(filename)
   stream = xml.getElementsByTagName(tag)
   print "[+] Writing to file!!!"
   for st in stream:
      fn = st.getAttribute("FileName")
      print fn
      wf.write(fn+'\n')
   wf.close()

if len(sys.argv) < 2:
   print "[+] Usage: python",sys.argv[0]," <file.xml> <tag|stream>"
else:
   readTab(sys.argv[1], sys.argv[2])
