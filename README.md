
## system installations
```
sudo apt install postgresql-client-common
```

## python installations
```
pip install kafka-python
pip install Faker
pip install psycopg2-binary

```


## Kafka

### Zookeeper
#### start
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### Server
#### configuration
```
vim config/server.properties
```
update the following ip addresses:

```
adverstised.listeners=PLAINTEXT://<server-ip-address>:9092
zookeeper.connect=<zookeeper-ip-address>:2181
```

#### start
```
JMX_PORT=8004 bin/kafka-server-start.sh config/server.properties
```


### Manager
#### configuration
```
vim conf/application.conf
```
update the following ip addresses:
```
cmak.zkhosts="<zookeeper-host>:2181"
```
#### start
```
cd target/universal/
unzip cmak--*
cd cmake*
bin/cmak -Dconfig.file=conf/application.conf -Dhttp.port=8080

```
