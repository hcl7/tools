import xml.etree.ElementTree as ET
import argparse

class SplitXmlByTag:
    def __init__(self, fn):
        self.fn = fn

    def Split(self):
        head = '<?xml version="1.0" encoding="utf-8"?><WIDECAST_DVB>'
        foot = '</WIDECAST_DVB>'
        print('[+] Reading ' + self.fn + ' file!...\n')
        context = ET.iterparse(self.fn, events=('start','end', ))
        for event, item in context:
            if item.tag == 'channel':
                title = item.attrib['name']
                elem = ET.tostring(item, "utf-8")
                filename = format(title + ".xml")
                print('[+] Splitting into ' + filename + ' !...')
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(head)
                    f.write(elem.decode('utf-8'))
                    f.write(foot)
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