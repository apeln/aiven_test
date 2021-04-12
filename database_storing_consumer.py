from kafka import KafkaConsumer
import json
from settings import settings
from kafka.consumer import group
from psycopg2.extras import RealDictCursor
from logger_common import get_logger
import traceback
import sys
from database import database_handler





if __name__ == "__main__":
    logger = get_logger( 'database_storing_consumer.log')
    conf = settings(logger)
    
    try:
        consumer = KafkaConsumer(
        conf.website_checker_topic,
        bootstrap_servers=conf.bootstrap_server,
        auto_offset_reset = 'earliest',
        group_id=conf.consumer_group_id)
    except Exception as e:
        msg = traceback.format_exc()
        logger.error(traceback.format_exc())
        sys.exit(msg)


    logger.info('KafkaConsumer successfully initialized')
    logger.info("website_checker_topic is {0}".format(conf.website_checker_topic))
    
    
    database = database_handler(logger,conf)
    database.connect()

    database.execute_sql_query('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\'')
    print(database.cur.fetchall())

    database.print_all_content()





 

    logger.info("starting the consumer")
    for msg in consumer:
        logger.debug("data received = {}".format(json.loads(msg.value)))
        rec = json.loads(msg.value)
        query = "INSERT INTO website_checker (CHECK_TIME_EPOCH,STATUS_CODE,RESPONSE_TIME_SECONDS,TEST_PATTERN_FOUND) VALUES ({0}, {1}, {2}, {3})".format( \
            rec['check_time_epoch'],rec['status_code'],rec['response_time_seconds'],rec['test_pattern_found'])
        database.execute_sql_query(query);
        database.print_latest_record()

    database.close_connection()