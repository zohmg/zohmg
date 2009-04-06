<?

// martind 2007-01-08, 12:31:05
require_once('../tools/app.inc.php');
#$PKG_JPGRAPH = '/web/site/stats.last.fm/jpgraph';

#require_once("$PKG_CORE/memcached.php");
#require_once("$PKG_CORE/std.php");
require_once("$PKG_JPGRAPH/jpgraph.php");
require_once("$PKG_JPGRAPH/jpgraph_line.php");
require_once("$PKG_JPGRAPH/jpgraph_bar.php");
require_once("$PKG_JPGRAPH/jpgraph_regstat.php");
require_once("$PKG_JPGRAPH/jpgraph_date.php");
// ===========
// = helpers =
// ===========


// simple graph: all attributes are properly filtered, one graph data point
// per result row, potentially multiple output columns
function generateSimpleGraphData($result, $columns, $colors) {
    $data = array();
    
    // make sure we can assign a color to each graph line
    $line_colors = $colors;
    while (count($line_colors) < count($columns)) {
        $line_colors = array_merge($line_colors, $colors);
    }
    
    foreach ($columns as $column) {
        $series = array();
        $series['name'] = $column;
        $series['color'] = array_shift($line_colors);
    
        $series['x'] = array();
        $series['y'] = array();
    
        foreach ($result as $row) {
            $series['x'][] = $row['fromdate'];
            $series['y'][] = $row[$column];
            #$series['x'][] = $row['todate'];
            #$series['y'][] = $row[$column];
        }
    
        $data[] = $series;
    }
    return $data;
}

// variant graph: all except one attributes are properly filtered, creates a line per
// value of the unfiltered attribute. Use this for e.g. per-country plots.
// You can generate $vari_attr_name and $vari_attr_values with the QueryTools::getVariantAttributes function.
function generateVariantGraphData($ds, $result, $vari_attr_name, $vari_attr_values, $columns, $colors) {
    $data = array();

    // make sure we can assign a color to each graph line
    $line_colors = array();
    while (count($line_colors) < count($vari_attr_values)) {
        $line_colors = array_merge($line_colors, $colors);
    }

    $temp_data = array();
    #sort($vari_attr_values);
    foreach ($vari_attr_values as $value) {
        $series = array();
        $series['name'] = $value;
        # to show full attribute names as line title:
        $series['color'] = array_shift($line_colors);

        $series['x'] = array();
        $series['y'] = array();

        $temp_data[$value] = $series;
    }

    $column = array_pop($columns);
    foreach ($result as $row) {
        $value = $row[$vari_attr_name];
        $series =& $temp_data[$value];

        $series['x'][] = $row['fromdate'];
        $series['y'][] = $row[$column];
        #$series['x'][] = $row['todate'];
        #$series['y'][] = $row[$column];
    }

    #$data = array_values($temp_data);
    foreach (array_keys($temp_data) as $key) {
        $data[] = $temp_data[$key];
    }

    return $data;
}

// Takes two arrays, will not work with hashes.
// Makes sure the items in $derivate have the same sort order as in $original,
// returns the re-sorted array. Additional items that are not in $original get 
// appended to the end, in the order in which they appear in $derivate. 
function preserve_sort_order($original, $derivate) {
    $derivate_copy = $derivate;
    $result = array();
    foreach ($original as $oitem) {
        if (in_array($oitem, $derivate_copy)) {
            $result[] = $oitem;
            $derivate_copy = array_diff($derivate_copy, array($oitem));
        }
    }
    // append remaining items;
    $result = array_merge($result, $derivate_copy);
    return $result;
}

// ========
// = main =
// ========i

header('Content-type:  text/plain');
// get the path to bg images etc
define("RESOURCE_DIR", dirname(__FILE__) . "/resources");


// check input
$page = $_GET['page'];
$fromdate = $_GET['fromdate'];
$todate = $_GET['todate'];
$countries = $_GET['country'];
$colors = array('black', 'darkorange', 'blue', 'darkgreen', 'brown', 'gray');

// fetch data
$json_request = 
    'page=' . urlencode($page) . 
    '&fromdate=' . urlencode($fromdate) .
    '&todate=' . urlencode($todate);
foreach ($countries as $country) {
    $json_request .= '&country[]=' . urlencode($country);
}
#$json = @file_get_contents('http://127.0.0.1/ws/getdata.php?' . $json_request);
$data = json_decode($json, true);
print $json_request;
exit;

// initialize canvas/check cache
$width  = 800;
$height = 450;
$style = "default";
if (array_key_exists('style', $_GET)) {
    $style = $_GET['style'];
    if ($style == 'mini') {
        # smaller default size
        $width = 320;
        $height = 200;
    }
}
if (array_key_exists('width', $_GET)) {
    $width = $_GET['width'];
}
if (array_key_exists('height', $_GET)) {
    $height = $_GET['height'];
}

$debug = array_key_exists('debug', $_GET);
$nocache = array_key_exists('nocache', $_GET);


if ($nocache || $debug) {
    $graph = new Graph($width, $height);
}
else {
    $cache_filename = "stats_" . md5($ds->getName()) . "_" . md5($_SERVER['QUERY_STRING']) . ".png";
    $graph = new Graph($width, $height, $cache_filename, 60);
    // will automatically exit here on positive cache hit
}

#$graph->img->SetAntiAliasing(); 


// -> no cache hit, or request for debug output
$result = $ds->findRows($constraints, $fromdate, $todate);

if (DB::isError($result)) {
    print_r($result);
}

// make sure only one variant attribute remains
$attr_values = QueryTools::getVariantAttributes($ds, $result);
$vari_attr_name = null;
$vari_attr_values = array();
if (sizeof(array_keys($attr_values)) > 1) {
    die("There can only be one unfiltered attribute. Currently unfiltered attributes: " . implode(', ', array_keys($attr_values)));
}
elseif (sizeof(array_keys($attr_values)) == 1) {
    $vari_attr_name = array_pop(array_keys($attr_values));
    $vari_attr_values = $attr_values[$vari_attr_name];
    // preserve original sort order, if it was given in parameters
    $vari_attr_values = preserve_sort_order($constraints[$vari_attr_name], $vari_attr_values);
}

// for multiline graphs: make sure that we either have one variant attribute OR multiple column definitions, not both
if (($vari_attr_name != NULL) && sizeof($columns) > 1) {
    die("You can either leave one attribute unfiltered or define multiple columns, but not both at the same time. Unfiltered attribute: ${vari_attr_name}, columns: " . implode(', ', $columns));
}

// generate graph data structures
if ($vari_attr_name != NULL) {
    // one unfiltered attribute
    $data = generateVariantGraphData($ds, $result, $vari_attr_name, $vari_attr_values, $columns, $colors);
}
else {
    // no unfiltered attribute
    $data = generateSimpleGraphData($result, $columns, $colors);
}

if ($debug) {
    print_r($data);
    die();
}


// build graph
$graph->title->Set($title);
$graph->setBackgroundImage(RESOURCE_DIR . "/graphlogo.gif", BGIMG_CENTER);
$graph->SetMarginColor('white');
$graph->SetScale("datlin");
$graph->xaxis->SetLabelAngle(90);
$graph->SetTickDensity(TICKD_NORMAL, TICKD_NORMAL);

if ($style == 'mini') {
    $graph->title->SetFont(FF_FONT1, FS_NORMAL, 10);
    $graph->adjBackgroundImage(0.95);
    $graph->img->SetMargin(35, 15, 10, 20);

    $graph->xaxis->HideLabels(true);
    $graph->xaxis->SetLabelFormat('Y-m-d', true);
    function yLabelFormat($num) {
        return FormatTools::formatNumberForDisplay($num);
    }
    $graph->yaxis->SetLabelFormatCallback('yLabelFormat');
    $graph->yaxis->SetFont(FF_FONT0, FS_NORMAL, 8);
    //$graph->yaxis->HideLabels(true);

    // display date of last data point
    $series = $data[0];
    $xdata = $series['x'];
    $n = count($xdata);
    $max_x = $xdata[$n-1];

    $txt = new Text(date('Y-m-d', $max_x));
    $txt->Pos($width-15, $height-80);
    $txt->SetColor('darkgray');
    $txt->SetFont(FF_FONT0, FS_NORMAL, 8);
    $txt->SetAngle(90);
    $graph->addText($txt);

}
else {
    $graph->adjBackgroundImage(0.90);
    $graph->img->SetMargin(55, 20, 20, 95);

    function xLabelFormat($num) {
        return date('Y-m-d', $num);
    }
    $graph->xaxis->SetLabelFormatCallback('xLabelFormat');
    function yLabelFormat($num) {
        return FormatTools::formatNumberForDisplay($num);
    }
    $graph->yaxis->SetLabelFormatCallback('yLabelFormat');

    // date
    #$txt = new Text("Generated: " . $date);
    $txt = new Text("Generated: " . date('Y-m-d H:i:s'));
    $txt->Pos($width-200, $height-20);
    $txt->SetColor('gray');
    $graph->addText($txt);
}


// graph lines and captions
$lines = array();
$captions = array();
if ($style == 'mini') {
    $caption_xpos = 35;
    $caption_xpos_increment = 10;
    $caption_ypos = $height - 17;
}
else {
    $caption_xpos = 55;
    $caption_xpos_increment = 20;
    $caption_ypos = $height - 20;
}
for ($i=0; $i<count($data); $i++) {
    $series = $data[$i];
    
    if (count($series['x']) > 0) {
        // only if we actually have data for this series
        
        # standard linear interpolation
        $lines[$i] = new LinePlot($series['y'], $series['x']);
        #$lines[$i]->SetStepStyle(true);

        # cubic spline interpolation
        #$spline = new Spline($series['x'], $series['y']);
        #list($xdata, $ydata) = $spline->get(min($width, count($series['x'])*3));
        #$lines[$i] = new LinePlot($ydata, $xdata);

        $lines[$i]->SetColor($series['color']);
        $graph->Add($lines[$i]);

        
        $captions[$i] = new Text($series['name']);
        $captions[$i]->SetColor($series['color']);
        $captions[$i]->Pos($caption_xpos, $caption_ypos);
        $caption_xpos += $captions[$i]->GetWidth($graph->img) + $caption_xpos_increment;
        $graph->AddText($captions[$i]);
    }
}

// paint
$graph->Stroke();
?>
