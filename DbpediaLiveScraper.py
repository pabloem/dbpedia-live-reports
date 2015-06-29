import urllib2
from bs4 import BeautifulSoup
import gzip
import requests
import urllib2 # Two HTTP libraries, hehe...
import StringIO
from rdflib import Graph
from datetime import datetime, timedelta
import json
import sys

class DbpediaLiveScraper(object):
    def __init__(self):
        self._changesets = list()
        self._accepted_cs = ['added','removed']
        self._baseUrl = 'http://live.dbpedia.org/changesets/'
        self._end = False

    def full_scrape(self,outfile,start,end):
        st_time = datetime.now()
        print("Starting the scrape at " +str(st_time))
        self._outfile = outfile
        self.get_data(start,end)
        st_time = datetime.now()
        print("Ending the scrape at " +str(st_time))


    def _save_progress(self):
        with open(self._outfile,'w') as of:
            json.dump(self._changesets,of)

    # Default start time is 2014/Jan/1 00:00
    def get_data(self,start=datetime(2014,1,1,0),end=datetime.now()):
        step = timedelta(hours=1)
        while start < end and not self._end:
            self.get_page_data(start)
            start = start+step
            self._save_progress()
        return
        
    def get_page_data(self,date):
        url = self.make_url(date)
        print('Obtaining url: '+ url)
        r = requests.get(self.make_url(date))
        #sp = BeautifulSoup(r.text)
        files = []
        dates = []
        sizes = []

        lines = r.text.split('\r\n')
        lists = [[a for a in lines[i].split(' ') if len(a) > 0] for i in range(len(lines))]
        for i,l in enumerate(lists):
            if len(l) > 1 and self.get_operation(l[1]):
                link = l[1].split('"')[1]
                files.append(link)
                dates.append(datetime.strptime(l[2]+' '+l[3],'%d-%b-%Y %H:%M'))
                sizes.append(l[4])

        self._download_changesets(files,dates,sizes,date)
        pass

    def _download_changesets(self,files,dates,sizes,url_base):
        for i,f in enumerate(files):
            date = dates[i]
            g = Graph()
            try:
                rep = urllib2.urlopen(self.make_url(url_base)+f)
                comp = StringIO.StringIO(rep.read())
                decomp = gzip.GzipFile(fileobj=comp)
                g.parse(data=decomp.read(), format="nt")
            except KeyboardInterrupt:
                self._end = True
                return
            except:
                print("ERROR: "+str(sys.exc_info()))
            size = self._size_str_to_int(sizes[i])
            self._changesets.append({'triples':len(g), 
                                     'operation':self.get_operation(f),
                                     'date': str(date), 
                                     'size': size,
                                     'file': str(f),
                                     'url_date': str(url_base)})
            print(self._changesets[len(self._changesets)-1])
            
    def _size_str_to_int(self,sz):
        #if len(sz) > 0 and sz[-1] in ['k','K']:
        #return int(sz[:-1])*1000
        return str(sz)

    def make_url(self,date):
        return self._baseUrl+date.strftime('%Y/%m/%d/%H')+'/'

    def get_operation(self,f):
        for acc in self._accepted_cs:
            if acc in f:
                return acc
        return False
