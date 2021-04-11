
from kafka import KafkaProducer
import json
from messages import website_info
import time
import requests
import re
from settings import settings
import time

def get_partition(key,all, available):
    return 0


def json_serializer(data):
    return json.dumps(data).encode('utf-8')



if __name__ == '__main__':
    message = website_info()
    conf = settings()
    producer = KafkaProducer(bootstrap_servers=conf.bootstrap_server, value_serializer=json_serializer)
    while 1 == 1 :
        message.check_time_epoch = int(time.time())
        try:
            response = requests.get(conf.target_website)
            message.status_code = response.status_code
            message.response_time_seconds = response.elapsed.total_seconds()
        
            test_pattern_found = re.search(conf.pattern_expected_to_be_found,response.text)
            message.test_pattern_found = 1 if test_pattern_found else 0
            
        except: #website is not available
            message.status_code = 404
            message.response_time_seconds = -1
            message.test_pattern_found = -1


        print(json_serializer(message.get_website_info()))
        producer.send(conf.website_checker_topic,message.get_website_info())
        time.sleep(conf.delta_time_availability_check_sec)