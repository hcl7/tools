from xml.etree import ElementTree
import argparse

class XmlEncode:
    def __init__(self, sFile):
        self.sFile = sFile + '.xml'
        self.dFile = sFile + '-new.xml'

    def run(self):
        with open(self.sFile, 'rb') as f:
            root = ElementTree.fromstring( f.read())

        tree = ElementTree.ElementTree( root)
        tree.write(self.dFile, encoding="utf-8", xml_declaration=True)

parser = argparse.ArgumentParser(description='XmlEncode class arguments:')
parser.version = '1.0'
parser.add_argument('--fn', help='xmlFile', action='store', type=str, required=True)
args = parser.parse_args()

def main():
    ob = XmlEncode(args.fn)
    ob.run()

if __name__ == '__main__':
    main()