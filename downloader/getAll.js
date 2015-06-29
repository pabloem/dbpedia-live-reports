var ChangesetManager = require('./ChangesetManager.js'),
    options = {
        latestChangeset: '2014/01/05/20'
    };

var csm = new ChangesetManager(options);

csm.checkForChangesets('2014/03/01/00');




/*
var fs = require('fs'),
    c = require('./ChangesetDownloader.js'),
    cd = new c({file: 'test.csv'}),
    bod;
fs.readFile('triples_file.nt',function(e,d){bod=d;});

var inp = {_fileContents: bod};

cd._parseFileFillTriples(inp);
*/
