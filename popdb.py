import sys
import os
import pyodbc
from datetime import datetime

class PopulateDatabase:
    def __init__(self, file):
        self.file = file
        self.txtlst = self.FileToList()

    def dbconn(self):
        conn_str = 'Driver={SQL Server};Server=DESKTOP-09NO8V1;Database=lespot_archive;UID=seven;PWD=root@123;Trusted_Connection=yes;'
        conn = pyodbc.connect(conn_str)
        return conn

    def getStringUntilChar(self, str, char):
        return str[:str.find(char) + len(char)-1]

    def getStringAfterChar(self, strg, char):
        return strg[str.find(char) + len(char):]

    def removeUntilTheLastCharacter(self, s, c):
        return s.rsplit(c,1)[-1]

    def fileDateCreated(self, f):
        t = os.path.getmtime(f)
        return datetime.fromtimestamp(t)

    def FileToList(self):
        txtfile = open(self.file, "r", encoding="utf-8")
        txtlst = []
        for line in txtfile:
            txtlst.append(line.rstrip())
        txtfile.close()
        return txtlst
        
    def run(self):
        count = 0
        conn = self.dbconn()
        cursor = conn.cursor()
        for line in self.txtlst:
            title = self.getStringUntilChar(self.removeUntilTheLastCharacter(line, '\\'),'.')
            path = line
            ext = self.removeUntilTheLastCharacter(line, '.')
            now = datetime.now()
            created = self.fileDateCreated(line)
            year = line.split("\\")[1]
            company = line.split("\\")[2]
            project = line.split("\\")[3]

            print(created,now,year)
            try:
                cursor.execute("""INSERT INTO [lespot_archive].[dbo].[asset] (title, path, ext, datecreated, dateinserted, year, company, project) VALUES (?,?,?,?,?,?,?,?)""",title,path,ext,created,now,year,company,project).rowcount
                conn.commit()
                count += 1
            except:
                continue
            
        print('[+] Rows inserted: ' + str(count))
        cursor.close()
        conn.close()

if len(sys.argv) < 2:
    print('[+] Usage: python ', sys.argv[0], "<txt file>")
else:
    obj = PopulateDatabase(sys.argv[1])
    print(obj.run())
