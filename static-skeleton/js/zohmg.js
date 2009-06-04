// authors: <martind,fredrik>@last.fm
// Wed Apr  8 13:37:09 UTC 2009

// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.


// data source.
var wsUrl = 'http://localhost:8086/data/';

var chartWidth = 600;
var chartHeight = 300;
var numXTicks = chartWidth / 80; // one tick every 80 pixels

// from http://beta.dailycolorscheme.com/archive/2006/09/07
var chartWidth = 600;
var chartHeight = 300;
var numXTicks = chartWidth / 80; // one tick every 80 pixels
var graphStyles = new Array(
			    "2B6088", // blue1
			    //"0A55A3", // blue2
			    //"006EBA", // blue3
			    //"8D1C0C", // red1
			    "3EA63B", // green
			    "FF6D06", // orange
			    "FD1B15", // red2
			    "FFE812", // yellow
			    "808080"  // gray
			    );
var missingValue = '_';



// fills the form with values from the GET-request,
// falling back on the defaults.
function updateForm() {
    var fields = ["t0", "t1", "unit", "d0", "d0v", "d1", "d1v", "d2", "d2v", "d3", "d3v", "d4", "d4v"];
    var defaults = {'t0':'20090101', 't1':'20091231', 'unit':'pageviews', 'd0':'country', 'd0v':'US,DE,SE'}
    $.each(fields, function(i, item) {
        $("input#"+item).val(urldecode($(document).getUrlParam(item, defaults[item])))
    });
}

// draws the graph.
function updateGraph() {
    loadData(
	     $('#graphNav input[name=t0]')[0].value,
	     $('#graphNav input[name=t1]')[0].value,
	     $('#graphNav input[name=unit]')[0].value,
	     $('#graphNav input[name=d0]')[0].value,
	     $('#graphNav input[name=d0v]')[0].value,
	     dictToString(loadFilters())
    );
}

// create query string from dictionary of values.
function dictToString(ary) {
    var s = "";
    $.each(ary, function(a) {
	    if (ary[a] != "") {
		s += a;
		s += "=";
		s += ary[a];
		s += "&";
	    }
    });
    return s;
}

// construct dictionary from dimension fields.
// TODO: fix this up to not be so pre-defined.
function loadFilters() {
    // highly hardcoded.
    d1  = $('input#d1').val(); // and so on..
    d1v = $('#graphNav input[name=d1v]')[0].value;
    d2  = $('#graphNav input[name=d2]')[0].value;
    d2v = $('#graphNav input[name=d2v]')[0].value;
    d3  = $('#graphNav input[name=d3]')[0].value;
    d3v = $('#graphNav input[name=d3v]')[0].value;
    d4  = $('#graphNav input[name=d4]')[0].value;
    d4v = $('#graphNav input[name=d4v]')[0].value;
    return {'d1':d1, 'd1v':d1v, 'd2':d2, 'd2v':d2v, 'd3':d3, 'd3v':d3v, 'd4':d4, 'd4v':d4v};
}


// callback for the json data.
function jsonCallback(data) {
    graph = pivot(data);
    var imgUrl = chartImgUrl(graph);
    $('#graph').html('<img src="' + imgUrl + '" />');
    $('#undergraph').append(' and <a href="' +imgUrl  +'">chart</a>.');
}

function loadData(t0, t1, unit, d0, d0v, filters) {
    var dataUrl = wsUrl +
	'?t0=' + encodeURIComponent(t0) +
	'&t1=' + encodeURIComponent(t1) +
	'&unit=' + encodeURIComponent(unit) +
	'&d0=' + encodeURIComponent(d0) +
	'&d0v=' + encodeURIComponent(d0v) +
	'&' + filters +
	'&jsoncallback=?' +
	'&jsonp=jsonCallback'

    $('#undergraph').html('<a href="' +dataUrl +'">raw data</a>');

    $.getJSON(dataUrl);
}

// construct a google charts url.
function chartImgUrl(graph) {
    // axis legends: strings, limited to numXTicks entries
    var chxl = '0:|';
    for (var idx=0; idx<numXTicks; idx++) {
	var label = graph.legend[Math.round(idx * (graph.legend.length-1) / numXTicks)];
	chxl += label + '|';
    }
    // axis legends: ranges
    var chxr = '1,' +
	graph.minValue + ',' +
	graph.maxValue;

    // item chart data, labels + colours
    var series = new Array();
    var labels = new Array();
    var colours = new Array();
    var colIdx = 0;
    $.each(graph.lines, function(label, line) {
	    //series.push(line.join(',')); // text encoding
	    series.push(simpleEncode(line, graph.maxValue));
	    //alert(simpleEncode(line, graph.maxValue));
	    labels.push(label);
	    colours.push(graphStyles[colIdx++]);
	});
    var chd = 's:' + series.join(',');
    var chdl = labels.join('|');
    var chco = colours.join(',');

    return 'http://chart.apis.google.com/chart?' +
	'chs=' + chartWidth + 'x' + chartHeight +          // size
	'&cht=lc' +            // type
	'&chds=' + graph.minValue + ',' + graph.maxValue + // data scaling
	'&chd=' + chd +        // data
	'&chco=' + chco +      // colour
	'&chdl=' + chdl +      // data labels
	'&chxt=x,y' +          // axes
	'&chxl=' + chxl +      // axis labels
	'&chxr=' + chxr +      // axis ranges
	'&chxs=0,,12,-1,lt' +  // axis styles
	'';
}

// Transforms the input data into a data structure
// better suited for graphing. Detects missing values
// for each time series.
function pivot(data) {
    graph = {
	legend: [],
	lines: {},
	minValue: 0,
	maxValue: 0
    };
    var numRows = 0;

    // get list of all dates, so we can guarantee sort order
    // get list of all items, so we can detect gaps in their time series
    var dates = new Array();
    var items = new Array();
    var actual_data = new Array();
    $.each(data, function(index, d) {
	    $.each(d, function(date,row) {
		    if (date!=0) { dates.push(date); } // not sure why we always get a 0 as last date
		    actual_data[date] = row;
		    $.each(row, function(item,value){
			    if ($.inArray(item, items) == -1) {
				items.push(item);
				if (!graph.lines[item]) {
				    graph.lines[item] = new Array();
				}
			    }
			});
		});
	});

    dates.sort();

    // build graph
    $.each(dates, function(idx, date){
	    var row = actual_data[date];
	    graph.legend.push(date);
	    $.each(items, function(idx,item) {
		    var value = row[item];
		    if (!value) {
			graph.lines[item].push(missingValue);
		    }
		    else {
			graph.minValue = Math.min(graph.minValue, value);
			graph.maxValue = Math.max(graph.maxValue, value);
			graph.lines[item].push(value);
		    }
		});
	    numRows++;
	});
    return graph;
}

// modified from http://code.google.com/apis/chart/formats.html
var simpleEncoding = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
function simpleEncode(valueArray,maxValue) {
    var chartData = [];
    for (var i = 0; i < valueArray.length; i++) {
	var currentValue = valueArray[i];
	if (!isNaN(currentValue) && currentValue >= 0) {
	    chartData.push(simpleEncoding.charAt(Math.round((simpleEncoding.length-1) * currentValue / maxValue)));
	}
	else {
	    chartData.push('_');
	}
    }
    return chartData.join('');
}


// snatched from http://kevin.vanzonneveld.net/techblog/article/javascript_equivalent_for_phps_urldecode/
function urldecode( str ) {
    // http://kevin.vanzonneveld.net

    if (str === undefined || str == null) { return undefined; }

    var histogram = {};
    var ret = str.toString();

    var replacer = function(search, replace, str) {
        var tmp_arr = [];
        tmp_arr = str.split(search);
        return tmp_arr.join(replace);
    };

    // The histogram is identical to the one in urlencode.
    histogram["'"]   = '%27';
    histogram['(']   = '%28';
    histogram[')']   = '%29';
    histogram['*']   = '%2A';
    histogram['~']   = '%7E';
    histogram['!']   = '%21';
    histogram['%20'] = '+';
    histogram['\u20AC'] = '%80';
    histogram['\u0081'] = '%81';
    histogram['\u201A'] = '%82';
    histogram['\u0192'] = '%83';
    histogram['\u201E'] = '%84';
    histogram['\u2026'] = '%85';
    histogram['\u2020'] = '%86';
    histogram['\u2021'] = '%87';
    histogram['\u02C6'] = '%88';
    histogram['\u2030'] = '%89';
    histogram['\u0160'] = '%8A';
    histogram['\u2039'] = '%8B';
    histogram['\u0152'] = '%8C';
    histogram['\u008D'] = '%8D';
    histogram['\u017D'] = '%8E';
    histogram['\u008F'] = '%8F';
    histogram['\u0090'] = '%90';
    histogram['\u2018'] = '%91';
    histogram['\u2019'] = '%92';
    histogram['\u201C'] = '%93';
    histogram['\u201D'] = '%94';
    histogram['\u2022'] = '%95';
    histogram['\u2013'] = '%96';
    histogram['\u2014'] = '%97';
    histogram['\u02DC'] = '%98';
    histogram['\u2122'] = '%99';
    histogram['\u0161'] = '%9A';
    histogram['\u203A'] = '%9B';
    histogram['\u0153'] = '%9C';
    histogram['\u009D'] = '%9D';
    histogram['\u017E'] = '%9E';
    histogram['\u0178'] = '%9F';

    for (replace in histogram) {
        search = histogram[replace]; // Switch order when decoding
        ret = replacer(search, replace, ret) // Custom replace. No regexing
    }

    // End with decodeURIComponent, which most resembles PHP's encoding functions
    ret = decodeURIComponent(ret);

    return ret;
}
