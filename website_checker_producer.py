
from logging import warning
from kafka import KafkaProducer
import json
from messages import website_info
import time
import requests
import re
from settings import settings
import time
from logger_common import get_logger
import traceback
import sys
from threading import Thread
from time import sleep
from kafka import KafkaAdminClient
from kafka.admin.new_partitions import NewPartitions
from kafka.admin import NewTopic


def get_partition(key,all, available):
    return 0


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


def website_check(producer, logger, partition, topic, website, pattern_to_match, delta_time_availability_check_sec):
    message = website_info()
    while 1 == 1 :
        message.check_time_epoch = int(time.time())
        message.website_address = website
        try:
            response = requests.get(website)
            message.status_code = response.status_code
            message.response_time_seconds = response.elapsed.total_seconds()
            
            test_pattern_found = re.search(pattern_to_match,response.text)
            message.test_pattern_found = 1 if test_pattern_found else 0
            
        except: #website is not available
            message.status_code = 404
            message.response_time_seconds = -1
            message.test_pattern_found = -1
            
        try:
            producer.send(topic,message.get_website_info(),partition=partition)
        except:
            logger.warning("Sending {} failed".format(json_serializer(message.get_website_info())))
        logger.info(json_serializer(message.get_website_info()))
        time.sleep(delta_time_availability_check_sec)



if __name__ == '__main__':
    
    logger = get_logger( 'website_checker_producer.log')
    conf = settings(logger)
    try:
        producer = KafkaProducer(bootstrap_servers=conf.bootstrap_server, value_serializer=json_serializer)
    except Exception as e:
        msg = traceback.format_exc()
        logger.error(traceback.format_exc())
        sys.exit(msg)

    logger.info('KafkaProducer successfully initialized')
    for i in range(len(conf.target_websites)):
        logger.info("Checking availability of {0} website every {1} seconds".format(conf.target_websites[i],str(conf.delta_times_availability_check_sec[i])))
        logger.info("Pattern to match - {0}".format(conf.patterns_expected_to_be_found[i]))
    logger.info("Sending info to topic {0}".format(conf.website_checker_topic))

    # check wether number of partitions configured properly
    enough_partitions = True
    partitions = producer.partitions_for(conf.website_checker_topic)
    if(len(partitions)!= len(conf.target_websites)):
        logger.warning("Increase number of partitions for topic {0} . \
         Number of partitions (current = {1}) needs to be equal to the number of target_websites specified in settings.ini = {2}" \
         .format(conf.website_checker_topic,len(partitions),len(conf.target_websites) ))
        enough_partitions = False


    threads = list()
    for i in range(len(conf.target_websites)):
        partitions_assigned = i if enough_partitions else 0
        thread = Thread(target = website_check, args = (producer, logger, partitions_assigned, conf.website_checker_topic, conf.target_websites[i], \
                                                            conf.patterns_expected_to_be_found[i], conf.delta_times_availability_check_sec[i],))
        thread.start()
        threads.append(thread)
    
    for t in threads:
        t.join()


  