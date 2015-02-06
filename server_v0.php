<!--Tagged Server v0
Displays HTTP request headers
References: http://php.net/manual/en/function.getallheaders.php
-->

<html>
<title> Tagged Server v0 </title>
<style>
body {font-family: "Courier New", Courier, monospace}
</style>

<body>
<?php
	echo "Displaying HTTP request headers...<br/>";
	
	// Fetch all HTTP request headers and format into JSON
	$finalArray = array();
	foreach (getallheaders() as $headerName => $headerValue) {
	  $myArray = array($headerName => $headerValue);
		$finalArray = array_merge($finalArray, $myArray);
	}
	echo json_encode($finalArray);
	echo "<br/>";
	echo "Finished displaying headers";
	echo "<br />";
	echo "<br />";
	
	// DEBUGGING: check values 
	echo "Check values: <br/>";
	foreach (getallheaders() as $header => $value) {
		echo "$header: $value <br/>";
	}
?>
</body>
</html>
