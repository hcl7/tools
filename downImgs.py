import sys
import requests
import json

imdbAPISearchMovie = 'https://imdb-api.com/en/API/SearchMovie/k_z9yeskhc/'
imdbApiSearchPosterById = 'https://imdb-api.com/en/API/Posters/k_z9yeskhc/'

class ImageDownload:
    def __init__(self, title):
        self.title = title.replace('"', "")
        self.data = self.formatData(imdbAPISearchMovie + self.title)
        self.id = self.getMovieId(self.data)
        #self.sizes = ['800x1200', '1920x1080', '1920x1078', '960x1440', '720x1080']
        self.sizes = ['720x1080']
        self.posters = self.formatData(imdbApiSearchPosterById + self.id)
        self.links = self.searchLinkBySize()

    def search(self,url):
        req = requests.request('GET', url)
        return req

    def formatData(self, url):
        req = self.search(url)
        data = req.text
        data = json.loads(data)
        return data

    def getMovieId(self, data):
        ids = []
        for i in data['results']:
            ids.append(i['id'])
        return ids[0]

    def searchLinkBySize(self):
        links = {}
        for s in self.sizes:
            for i in self.posters['posters']:
                if(i['width'] == int(s.split('x')[0]) and i['height'] == int(s.split('x')[1])):
                    links[s] = (i['link'])
            for j in self.posters['backdrops']:
                if(j['width'] == int(s.split('x')[0]) and j['height'] == int(s.split('x')[1])):
                    links[s] = (j['link'])
        return links

    def downloadImg(self):
        if(bool(self.links) == True):
            for key in self.links.keys():
                print("[+] Downloading " + self.title + " with size: " + key)
                f = open(self.title +'_' + key + '.jpg', 'wb')
                req = requests.get(self.links[key])
                if(req.status_code == 200):
                    for chunk in req:
                        f.write(chunk)
                f.close()
                print("[+] Done!...")


if len(sys.argv) < 2:
    print("[+] Usage: ", sys.argv[0], " <Movie Title>" )
else:
    imgObj = ImageDownload(sys.argv[1])
    imgObj.downloadImg()
