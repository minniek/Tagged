<?php
	// Uncomment to see all request headers
	//echo json_encode(getallheaders());

	// Store headers and values into associative array "reqHeaderArray"
	foreach (getallheaders() as $headerName => $headerValue) {
		$reqHeaderArray[$headerName] = $headerValue;
	}

	// Generate a digital signature using Tagged server's private key
	$privKeyFile = '//private_key.pem';
	$privKey = openssl_pkey_get_private($privKeyFile);
 	ksort($reqHeaderArray); // Sort keys in ascending order
	$data = json_encode($reqHeaderArray);
	//echo "\$data: $data";
	openssl_sign($data, $digSig, $privKey, OPENSSL_ALGO_SHA256);

	// Encode signature in base64
	$digSigEncoded = base64_encode($digSig);
	//echo $digSigEncoded;

	// Add signature to array
	$reqHeaderArray["Auth"] = $digSigEncoded;
	echo json_encode($reqHeaderArray);

	// Free the key from memory
	openssl_free_key($privKey);
?>
