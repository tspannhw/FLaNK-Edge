# FLaNK-Edge
An example of FLaNK Edge


### Download Edge Flow Manager (CEM/EFM) Flow


````
curl -v --output flow.json http://nifi1:10090/efm/api/designer/rpi4thermal/flows/export

curl -v --output rp400.json http://nifi1:10090/efm/api/designer/rpi400/flows/export

curl -v --output rpi4weather.json http://nifi1:10090/efm/api/designer/rpi4weather/flows/export

````

### Import Edge Flow Manager (CEM/EFM) Flow



````
curl -X 'POST' 'http://nifi1:10090/efm/api/designer/rp4weather/flows/import' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'X-XSRF-TOKEN: 7f2b530e-9ae5-4ee3-948e-5eee2dc6b36e' -d  @rpi4weather.json
  

{"identifier":"f94595fb-da35-4513-b658-6e21c7b3de15","agentClass":"rp4weather","rootProcessGroupIdentifier":"7620b7cd-f23c-4d77-af66-aa637910d286","created":1686239548463,"updated":1686241423524}

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

### Bootstrap.conf for c2

````

# MiNiFi Command & Control Configuration
# C2 Properties
# Enabling C2 Uncomment each of the following options
c2.enable=true
c2.rest.url=http://nifi1:10090/efm/api/c2-protocol/heartbeat
c2.rest.url.ack=http://nifi1:10090/efm/api/c2-protocol/acknowledge
# C2 Rest Path Properties
# The base path of the C2 server's REST API, eg.: http://localhost/c2-server/api
c2.rest.path.base=http://nifi1:10090/efm/api
# Relative url of the C2 server's heartbeat endpoint, eg.: /heartbeat
c2.rest.path.heartbeat=/c2-protocol/heartbeat
# Relative url of the C2 server's acknowledge endpoint, eg.: /acknowledge
c2.rest.path.acknowledge=/c2-protocol/acknowledge
## c2 timeouts
c2.rest.connectionTimeout=5 sec
c2.rest.readTimeout=5 sec
c2.rest.callTimeout=10 sec
## heartbeat in milliseconds
c2.agent.heartbeat.period=5000
## define parameters about your agent
c2.agent.class=macm1java
c2.config.directory=./conf
c2.runtime.manifest.identifier=minifi
c2.runtime.type=minifi-java
# Optional.  Defaults to a hardware based unique identifier
#c2.agent.identifier=
# If set to false heartbeat won't contain the manifest. Defaults to true.
c2.full.heartbeat=false
# Directory for storing assets downloaded via C2 update/asset command
c2.asset.directory=./asset


````
