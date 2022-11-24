import xml.etree.ElementTree as ET
import argparse

class SplitXmlByTag:
    def __init__(self, fn):
        self.fn = fn

    def WriteHeadToXml(self, fn, item):
        head = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE tv>\n<tv generator-info-name="my listings generator">\n'
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(head)
            f.write(item)

    def WriteBodyToXml(self, fn, item):
        with open(fn, 'a+', encoding='utf-8') as f:
            f.write(item)

    def WriteEndToXml(self, fn):
        foot = '</tv>'
        with open(fn, 'a+', encoding='utf-8') as f:
            f.write(foot)

    def Split(self):
        id = []
        title = []
        print('[+] Reading ' + self.fn + ' file!...\n')
        context = ET.iterparse(self.fn, events=('start',))
        for event, item in context:
            if item.tag == 'channel':
                ids = item.attrib['id']
                id.append(ids)
                titles = item.find('display-name').text
                title.append(titles)
                cnts = ET.tostring(item, "utf-8")
                filename = format(titles + ".xml")
                self.WriteHeadToXml(filename, cnts.decode('utf-8'))
            for i in range(len(id)):
                if item.tag == 'programme':
                    if id[i] == item.attrib['channel']:
                        cnt = ET.tostring(item, "utf-8")
                        self.WriteBodyToXml(title[i] + '.xml', cnt.decode('utf-8'))
        for j in range(len(id)):
            self.WriteEndToXml(title[j]  + '.xml')
        print('[+] Done!...\n')

parser = argparse.ArgumentParser(description='SplitXmlByTag class arguments:')
parser.version = '1.0'
parser.add_argument('--fn', help='xmlFile', action='store', type=str, required=True)
args = parser.parse_args()

def main():
    ob = SplitXmlByTag(args.fn)
    ob.Split()

if __name__ == '__main__':
    main()