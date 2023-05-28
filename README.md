# FLaNK-Edge
An example of FLaNK Edge


### Download Edge Flow Manager (CEM/EFM) Flow


````
curl -v --output flow.json http://nifi1:10090/efm/api/designer/rpi4thermal/flows/export

````

### Output in flows is flow.json

````
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0*   Trying 192.168.1.157:10090...
* Connected to nifi1 (192.168.1.157) port 10090 (#0)
> GET /efm/api/designer/rpi4thermal/flows/export HTTP/1.1
> Host: nifi1:10090
> User-Agent: curl/7.88.1
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Sun, 28 May 2023 01:38:33 GMT
< Set-Cookie: XSRF-TOKEN=dd9e041c-149b-43ea-89bc-d9f466b71fd8; Path=/efm
< Expires: Thu, 01 Jan 1970 00:00:00 GMT
< Content-Type: application/json
< X-Content-Type-Options: nosniff
< X-XSS-Protection: 1; mode=block
< X-Frame-Options: DENY
< Vary: Accept-Encoding, User-Agent
< Transfer-Encoding: chunked
<
{ [14128 bytes data]
100 1080k    0 1080k    0     0  15.6M      0 --:--:-- --:--:-- --:--:-- 16.7M
* Connection #0 to host nifi1 left intact
````
