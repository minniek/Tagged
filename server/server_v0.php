<?php	
	$finalArray = array();
	foreach (getallheaders() as $headerName => $headerValue) {
		$myArray = array($headerName => $headerValue);
		$finalArray = array_merge($finalArray, $myArray);
	}
	echo json_encode($finalArray);
?>
