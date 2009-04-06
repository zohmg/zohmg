<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
  <meta name="generator" content="MicroLink 5.6">

  <title>index</title>
  
  <style type="text/css" media="screen">
    body, p, td {
      font-size: 1em;
      font-family: Verdana, Helvetica, Arial, sans-serif;
    }
    #nav {
      margin-bottom: 2em;
      font-size: 0.8em;
    }
    pre {
/*      display: none; */
      
      font-size: 0.75em;
      color:#33ff33;
      background-color:#000000;
      margin-top: 0;
      padding-top: 1em;
      margin-right: 0;
      padding-right: 1em;
      margin-bottom: 0;
      padding-bottom: 1em;
      margin-left: 0;
      padding-left: 1em;
      width: 30em;
      overflow: auto; /* enables automatic scroll bars for wide content */
    }
  </style>

  <script type="text/javascript" src="jquery-1.3.2.min.js"></script> 
  <script type="application/x-javascript">

  //var wsUrl = './testdata.json';
  var wsUrl = './data.php';
  
  var chartWidth = 600;
  var chartHeight = 300;
  var numXTicks = chartWidth / 80; // one tick every 80 pixels
  
  // from http://beta.dailycolorscheme.com/archive/2006/09/07
  
  var chartWidth = 600;
  var chartHeight = 300;
  var numXTicks = chartWidth / 80; // one tick every 80 pixels
  
  // from http://beta.dailycolorscheme.com/archive/2006/09/07
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

  function updateGraph() {
    loadData(
      $('#graphNav input[name=period_start]')[0].value, 
      $('#graphNav input[name=period_end]')[0].value, 
      $('#graphNav input[name=page]')[0].value, 
      $('#graphNav input[name=countries]')[0].value);
  }
  
  function loadData(period_start, period_end, page, countries) {
    var dataUrl = wsUrl + 
      '?period_start=' + encodeURIComponent(period_start) +
      '&period_end=' + encodeURIComponent(period_end) +
      '&page=' + encodeURIComponent(page) +
      '&countries=' + encodeURIComponent(countries);
    $.getJSON(dataUrl,
      function(data){
        var graph = pivot(data);
        var imgUrl = chartImgUrl(graph);
        $('#graph').html(
          '<img src="' + imgUrl + '" /> ' +
          '<pre>' + dataUrl + '</pre>' +
          '<pre>' + imgUrl + '</pre>')
      }
    );
  }
  
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
  </script>
</head>

<body onload="updateGraph();">

<?
function getValue($name, $default=null) {
    if (array_key_exists($name, $_GET)) {
        return $_GET[$name];
    }
    return $default;
}
?>

Here's plotting pageviews per path.<br \>


<form id="graphNav">

<table id="nav">
<tr>
  <td>From: <br />
    <input type="text" name="period_start" value="<?= getValue('period_start', '20070101') ?>" /></td>
  <td>To: <br />      
    <input type="text" name="period_end" value="<?= getValue('period_end', '20070431') ?>" /></td>
</tr>
<tr>
  <td colspan="2">Page:<br/>
    <input type="text" name="page" value="<?= getValue('page', '/music/Radiohead') ?>" size="40"/></td>
</tr>
<tr>
  <td>Countries:<br/>
    <input type="text" name="countries" value="<?= getValue('countries', 'US,GB,DE,FR,SE,IT') ?>" /></td>
  <td colspan="3" align="right">
    <input type="submit" value="Update" /></td>
</tr>
</table>
</form>

<div id="graph" />

</body>
</html>
