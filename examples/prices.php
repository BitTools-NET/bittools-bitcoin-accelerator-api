<?php
// PHP 7.4+ CLI example; API key remains in the server environment.
$key = trim((string) getenv('BITTOOLS_API_KEY'));
if ($key === '' || preg_match('/[\r\n]/', $key)) {
    fwrite(STDERR, "Set BITTOOLS_API_KEY in the server environment.\n"); exit(1);
}
$base = rtrim(getenv('BITTOOLS_API_BASE') ?: 'https://www.bittools.net/api/v1', '/');
$parts = parse_url($base);
if (!$parts || ($parts['scheme'] ?? '') !== 'https' || empty($parts['host']) || isset($parts['user']) || isset($parts['pass']) || isset($parts['query']) || isset($parts['fragment'])) {
    fwrite(STDERR, "Use an HTTPS API base URL without credentials or query parameters.\n"); exit(1);
}
if (!function_exists('curl_init')) { fwrite(STDERR, "Enable the PHP cURL extension.\n"); exit(1); }
$ch = curl_init($base . '/prices?' . http_build_query(['ids' => 'bitcoin', 'fiat' => 'USD']));
curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_CONNECTTIMEOUT => 5, CURLOPT_TIMEOUT => 15,
    CURLOPT_FOLLOWLOCATION => false, CURLOPT_SSL_VERIFYPEER => true, CURLOPT_SSL_VERIFYHOST => 2,
    CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $key, 'Accept: application/json']]);
$body = curl_exec($ch); $status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch); curl_close($ch);
if ($body === false || $status < 200 || $status >= 300) { fwrite(STDERR, 'API request failed (HTTP ' . $status . '). ' . $error . "\n"); exit(1); }
$data = json_decode($body, true);
if (!is_array($data) || ($data['success'] ?? false) !== true) { fwrite(STDERR, "Invalid or unsuccessful JSON response.\n"); exit(1); }
echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
