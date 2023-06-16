
#### MiNiFi Java

````

 downloaded client-private-key-encoded key and client-certificate-encoded.cer certificate files to a JKS Keystore
 
 openssl pkcs12 -export -in client-certificate-encoded -inkey client-private-key-encoded -out client-keystore.p12

keytool -importkeystore -srckeystore client-keystore.p12 -srcstoretype pkcs12 -destkeystore client-keystore.jks

wget https://letsencrypt.org/certs/isrgrootx1.pem
keytool -import -file isrgrootx1.pem -alias isrgrootx1 -keystore client-truststore.jks

Create a Service of type Restricted SSL Context Service with the following configuration:
Service Name
Specify a name for this service. This tutorial uses Client SSL Context Service.
Keystore Filename
[***/PATH/TO/***]client-truststore.jks
Keystore Password
[***THE PASSWORD YOU PROVIDED WHEN CREATING THE JKS STORE***]
Key Password
[***THE PASSWORD YOU PROVIDED WHEN CREATING THE JKS STORE***]
Keystore Type
JKS
Truststore Filename
client-truststore.jks
Truststore Type
JKS
Truststore Password
[***THE PASSWORD YOU PROVIDED WHEN CREATING THE CLIENT TRUSTSTORE***]

Click Apply.
Create an InvokeHTTP processor named Send to CDF with the following configuration:
Automatically Terminated Relationships
Select all relationships.
Content-type
Depends on your flow file data type. This tutorial uses text/plain.
HTTP Method
POST
Remote URL
https://[***ENDPOINT HOSTNAME COPIED FROM CDF FLOW DEPLOYMENT MANAGER***]:9000/contentListener
For example, https://my-flow.inbound.my-dfx.c94x5i9m.xcu2-8y8z.mycompany.test:9000/contentListener

SSL Context Service
Client SSL Context Service
Leave all other settings with their default values.

````

#### References

https://docs.cloudera.com/dataflow/cloud/inbound-connections-clients/topics/cdf-inbound-connections-minifi-nifi-tutorial.html
