
General
------------------------------
**__Note__** : This program uses **python3**
<br />
<br />
This program implements a system that monitors website availability over the network, and passes this data through a Kafka instance
into PostgreSQL database.



Install python dependencies
---------------------------

```
pip3 install kafka-python
pip3 install Faker
pip3 install psycopg2-binary
```

Important Note
--------------------------
In my testing I used only **one** Broker. For efficient operation I would split the data of a topic across multiple brokers 
to balance the load between them. And then we will acheive parallelism by assigning each partition to **different** consumer group .

Configuration
--------------------------
1. Edit the *settings.ini* configuration file
    ```
    vim settings.ini
    ```
    This file will be used by the both scripts (website_checker_producer.py and database_storing_consumer.py)

2. For efficient operation create topic (as specified in settings.ini - Topic: website_availability) BEFORE running the **website_checker_producer** and set number of partitions to the # of target websites  (as specified in settings.ini - TargetWebsites: https://aiven.io/,https://stackoverflow.com/ - in this case **2**)

Running
--------------------------

1. Run the *website_checker_producer.py*
    ```
    python3 website_checker_producer.py
    ```
    *website_checker_producer.log* file will be created containing the log messages. </br> 
    This code monitors website (defined in settings.ini) 
    availability over network, produces metrics about this and creates Kafka producer that sends the checks results to a Kafka topic.

2. Run the *database_storing_consumer.py*  
    ```
    python3 database_storing_consumer.py
    ```
    *database_storing_consumer.log* file will be created containing the log messages. </br> 
    This code connects to PostgreSQL database (address and authentication information is defined in settings.ini), creates relevant database table and creates Kafka consumer that stores the received data to the database. </br> 
    Table **website_checker** will be created (if doesn't exist) in the target database. </br>
    The format as follows: </br>
    | column name | log_id | website_url | check_time_epoch | status_code | response_time_seconds | test_pattern_found |
    | :---: | :---: | :---: | :---: | :---: | :---: | :---: | 
    | column info  | running id | target website | check timestamp - epoch time | return code | HTTP response time | is test pattern found on the page | 

    **Note** </br>
    For efficient operation run #database_storing_consumer instances equals to the # of target websites (as specified in settings.ini).</br>
             And for even more efficient operation assign each partition to different consumer group (consumer group in specified in settings.ini - GroupId: website-checker-id)

    



<br />
<br />
Appendix
------------
------------
<br />


Kafka setup
--------------

1. Zookeeper
    - start
        ```
        bin/zookeeper-server-start.sh config/zookeeper.properties
        ```

2.  Server
    - configuration
        ```
        vim config/server.properties
        ```
        update the following ip addresses:

        ```
        adverstised.listeners=PLAINTEXT://<server-ip-address>:9092
        zookeeper.connect=<zookeeper-ip-address>:2181
        ```

    - start
        ```
        JMX_PORT=8004 bin/kafka-server-start.sh config/server.properties
        ```


3.  Manager
    - configuration
        ```
        vim conf/application.conf
        ```
        update the following ip addresses:
        ```
        cmak.zkhosts="<zookeeper-host>:2181"
        ```
    - start
        ```
        cd target/universal/
        unzip cmak--*
        cd cmake*
        bin/cmak -Dconfig.file=conf/application.conf -Dhttp.port=8080

        ```
