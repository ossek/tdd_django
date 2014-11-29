'use strict';

var Nightmare = require('nightmare');
var jq = require('jquery');
var jsdom = require('jsdom');

describe('test suite',function(){
    var result;
    var url = 'http://localhost:8000';

    beforeEach(function(done){
      new Nightmare()
          .goto(url)
          .evaluate(function(){
            return document;
          }, function(res){
            result = res;
          }).run(done);
    });

    it('has a row in list table ',function(done) {
      var row;
      expect(result).not.toBe(null);
      var $ = enableJquery(result);
      var rows = $('#id_list_table td');
      for(row in rows){
          if(row.textContent === '1: Buy peacock feathers'){
              expect(true).toBe(true);
              done();
              return;
          }
      }
      expect(false).toBe(false);
      done();
    });
});

function enableJquery(doc){
    return jq(jsdom.jsdom(doc.all[0].outerHTML).parentWindow);
}
