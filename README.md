# FLaNK-Edge
An example of FLaNK Edge


### Download Edge Flow Manager (CEM/EFM) Flow

Check out http://nifi1:10090/efm/swagger/


````
curl -v --output flow.json http://nifi1:10090/efm/api/designer/rpi4thermal/flows/export

curl -v --output rp400.json http://nifi1:10090/efm/api/designer/rpi400/flows/export

curl -v --output rp4thermalcpp.json http://nifi1:10090/efm/api/designer/rp4thermalcpp/flows/export

curl -v --output rpi4weather.json http://nifi1:10090/efm/api/designer/rpi4weather/flows/export

curl -v --output enviroplus.json http://nifi1:10090/efm/api/designer/enviroplus/flows/export

curl -v --output enviropluscpp.json http://nifi1:10090/efm/api/designer/enviropluscpp/flows/export

curl -v --output mactimm1java.json http://nifi1:10090/efm/api/designer/mactimm1java/flows/export

curl -v --output rpi400c.json http://nifi1:10090/efm/api/designer/rpi400c/flows/export

# Generic Shell
curl -v --output $1.json http://nifi1:10090/efm/api/designer/$1/flows/export

````

### Import Edge Flow Manager (CEM/EFM) Flow



````
curl -X 'POST' 'http://nifi1:10090/efm/api/designer/rp4weather/flows/import' -H 'accept: application/json' -H 'Content-Type: application/json' -H 'X-XSRF-TOKEN: 7f2b530e-9ae5-4ee3-948e-5eee2dc6b36e' -d  @rpi4weather.json
  

{"identifier":"f94595fb-da35-4513-b658-6e21c7b3de15","agentClass":"rp4weather","rootProcessGroupIdentifier":"7620b7cd-f23c-4d77-af66-aa637910d286","created":1686239548463,"updated":1686241423524}

````

### Send assets to a device

See: https://docs.cloudera.com/cem/1.5.1/using-asset-push-command/topics/cem-using-asset-push-command.html

### payload.txt

````

{
    "assetFileName": "stormy.jpg",
    "assetUri": "/opt/demo/stormy.jpg",
    "forceDownload": false
}

````

### Execute

````

curl -X 'POST' \
  'http://nifi1:10090/efm/api/commands/rpi400/update-asset' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-XSRF-TOKEN: 8b23c87e-17da-4b6d-adfd-0864c6deb1c3' \
  -d '{"assetFileName": "stormy.jpg","assetUri":"/opt/demo/stormy.jpg","forceDownload": false}'

{"bulkOperation":{"id":"7bac07cd-28a9-4527-a46e-8081e73714ef","agentClass":"rpi400","state":"NEW"}}

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

### minifi.properties for c2 c++ rpi

````
## Enabling C2 Uncomment each of the following options
## define those with missing options
nifi.c2.enable=true
## define protocol parameters
## The default is RESTSender.
## Alternatively, you may use CoapProtocol if that extension is built.
nifi.c2.agent.protocol.class=RESTSender
#nifi.c2.agent.protocol.class=CoapProtocol
#nifi.c2.agent.coap.host=
#nifi.c2.agent.coap.port=
## base URL of the c2 server,
## very likely the same base url of rest urls
nifi.c2.flow.base.url=http://nifi1:10090/efm/api
nifi.c2.rest.url=http://nifi1:10090/efm/api/c2-protocol/heartbeat
nifi.c2.rest.url.ack=http://nifi1:10090/efm/api/c2-protocol/acknowledge
nifi.c2.rest.ssl.context.service=
nifi.c2.root.classes=DeviceInfoNode,AgentInformation,FlowInformation
## Minimize heartbeat payload size by excluding agent manifest from the heartbeat
nifi.c2.full.heartbeat=false
## heartbeat twice a minute
nifi.c2.agent.heartbeat.period=30 sec
## define parameters about your agent
nifi.c2.agent.class=rpi400c
nifi.c2.agent.identifier=splootrpi400c
## define metrics reported
nifi.c2.root.class.definitions=metrics
nifi.c2.root.class.definitions.metrics.name=metrics
nifi.c2.root.class.definitions.metrics.metrics=runtimemetrics,loadmetrics,processorMetrics
nifi.c2.root.class.definitions.metrics.metrics.runtimemetrics.name=RuntimeMetrics
nifi.c2.root.class.definitions.metrics.metrics.runtimemetrics.classes=DeviceInfoNode,FlowInformation
nifi.c2.root.class.definitions.metrics.metrics.loadmetrics.name=LoadMetrics
nifi.c2.root.class.definitions.metrics.metrics.loadmetrics.classes=QueueMetrics,RepositoryMetrics
nifi.c2.root.class.definitions.metrics.metrics.processorMetrics.name=ProcessorMetric
nifi.c2.root.class.definitions.metrics.metrics.processorMetrics.classes=GetFileMetrics

````

### Bootstrap.conf for c2 java

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

[https://docs.cloudera.com/cem/1.5.1/installation-minifi-cpp-agent/topics/cem-configure-minifi-cpp-agent.html](https://docs.cloudera.com/cem/1.5.1/installation-minifi-cpp-agent/topics/cem-configure-minifi-cpp-agent.html)


[https://github.com/apache/nifi-minifi-cpp/blob/main/C2.md](https://github.com/apache/nifi-minifi-cpp/blob/main/C2.md)


[https://community.cloudera.com/t5/Community-Articles/Building-and-Running-MiniFi-CPP-in-OrangePi-Zero/ta-p/247684](https://community.cloudera.com/t5/Community-Articles/Building-and-Running-MiniFi-CPP-in-OrangePi-Zero/ta-p/247684)


[https://github.com/apache/nifi-minifi-cpp/blob/master/PROCESSORS.md#appendhostinfo](https://github.com/apache/nifi-minifi-cpp/blob/master/PROCESSORS.md#appendhostinfo)


[https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=65145325](https://cwiki.apache.org/confluence/pages/viewpage.action?pageId=65145325)


[https://www.datainmotion.dev/2019/05/cloudera-edge-management-introduction.html](https://www.datainmotion.dev/2019/05/cloudera-edge-management-introduction.html)



[https://www.datainmotion.dev/2020/02/edgeai-jetson-nano-with-minifi-c-agent.html](https://www.datainmotion.dev/2020/02/edgeai-jetson-nano-with-minifi-c-agent.html)https://www.datainmotion.dev/2020/02/edgeai-jetson-nano-with-minifi-c-agent.html

[https://github.com/apache/nifi-minifi-cpp/blob/main/PROCESSORS.md#appendhostinfo](https://github.com/apache/nifi-minifi-cpp/blob/main/PROCESSORS.md#appendhostinfo)https://github.com/apache/nifi-minifi-cpp/blob/main/PROCESSORS.md#appendhostinfo
