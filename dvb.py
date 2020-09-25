import xlrd as x
import sys
import xlrd as x
import sys

__author__ = 'Elvin Mucaj'
start_time = []
stime = []
duration = []
category = []
short = []
long = []

xml_start = '<?xml version="1.0" encoding="ISO-8859-1"?><WIDECAST_DVB><channel name="Family Channel HD">'
xml_end = '</channel></WIDECAST_DVB>'

xml_inside = '''<event id="{0}" start_time="{1}" duration="{2}">
				<short_event_descriptor lang="alb" name="{3}">{4}</short_event_descriptor>
				<extended_event_descriptor lang="alb"><text>{5}</text></extended_event_descriptor>
			</event>'''

def readExcelGenerateXml(file):
	wf = open("dvb.xml", "w+")
	wf.write(xml_start+'\n')
	wb = x.open_workbook(file) 
	print("[+] Reading Excel File!!!")
	sheet = wb.sheet_by_index(0)
	for i in range(sheet.nrows):
		start_time.append(sheet.cell_value(i, 1))
		stime.append(sheet.cell_value(i, 2))
		duration.append(sheet.cell_value(i, 4))
		category.append(sheet.cell_value(i, 5))
		short.append(sheet.cell_value(i, 6))
		long.append(sheet.cell_value(i, 7))
		
	start_time.pop(0)
	stime.pop(0)
	duration.pop(0)
	category.pop(0)
	short.pop(0)
	long.pop(0)
		
	print("[+] Generating XML File!!!")
	for p in range(len(start_time)):
		if(duration[p] != ""):
			wf.write(xml_inside.format(p, start_time[p]+" "+stime[p], int((duration[p]*60)), short[p], category[p], long[p])+'\n')
	wf.write(xml_end+'\n')
	wf.close()
	print("[+] Done!!!")
	
if len(sys.argv) < 2:
	print("[+] Usage: python", sys.argv[0], "<excelfile>")
else:
	print("By "+ __author__ )
	readExcelGenerateXml(sys.argv[1])
	
