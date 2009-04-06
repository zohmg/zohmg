<?

//
// conf
//

$wsUrl = "http://hadoopdev1.bra.int.last.fm:8080";

//
// tools
//

// http://netevil.org/blog/2006/nov/http-post-from-php-without-curl
function do_http_post($url, $data, $optional_headers = null) {
  $params = array('http' => array(
    'method' => 'POST',
    'content' => $data
  ));
  if ($optional_headers !== null) {
    $params['http']['header'] = $optional_headers;
  }
  $ctx = stream_context_create($params);
  $fp = @fopen($url, 'rb', false, $ctx);
  if (!$fp) {
    throw new Exception("Problem with $url, $php_errormsg");
  }
  $response = @stream_get_contents($fp);
  if ($response === false) {
    throw new Exception("Problem reading data from $url, $php_errormsg");
  }
  return $response;
}


//
// main
//
try {
  $result = do_http_post($wsUrl, http_build_query($_GET));
  print $result;
}
catch (Exception $e) {
    header("HTTP/1.0 500 Internal Server Error");
    print($e->getMessage());
}
?>
