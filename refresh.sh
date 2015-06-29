cp downloader/changesetInfo.csv .
echo "url,operation,date,triples" > cs.csv
grep -v "triples" changesetInfo.csv >> cs.csv
mv cs.csv changesetInfo.csv
pweave DbpediaLiveAnalysis.py
rst2html DbpediaLiveAnalysis.rst > index.html
