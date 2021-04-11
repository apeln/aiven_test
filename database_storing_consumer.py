from kafka import KafkaConsumer
import json
from settings import settings
from kafka.consumer import group
from psycopg2.extras import RealDictCursor
import psycopg2
from logger_common import get_logger
import traceback
import sys

class Database:
    def __init__(self,logger,conf):
        """ Connect to the PostgreSQL database server """
        self.db_conn = None
        self.cur = None
        self.logger = logger
        try:
            # connect to the PostgreSQL server
            
            
            logger.info('Connecting to the PostgreSQL database via uri : {0}'.format(conf.database_uri))
            database_uri = conf.database_uri
            
            self.db_conn = psycopg2.connect(database_uri)
            
            logger.info("Creating cursor")
            self.cur = self.db_conn.cursor()
            
            

            logger.info('PostgreSQL database version:')
            self.cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self.cur.fetchone()

            logger.info(db_version)

            # create table if doesn't exist
            self.cur.execute('CREATE TABLE IF NOT EXISTS website_checker ('
                                '  LOG_ID SERIAL PRIMARY KEY,  '
                                '  CHECK_TIME_EPOCH INT not null,'
                                '  STATUS_CODE INT not null,'
                                '  RESPONSE_TIME_SECONDS FLOAT not null,'
                                '  TEST_PATTERN_FOUND INT not null)')



        except (Exception, psycopg2.DatabaseError) as error: ## log error and exit
            logger.fatal(error)
            sys.exit(error)


    def close_connection(self):
        # close the communication with the PostgreSQL
        if self.cur is not None:
            self.cur.close()
        if self.db_conn is not None:
            self.db_conn.close()
        logger.info('Database connection closed.')

    def print_all_content(self):
        self.cur.execute("SELECT * from website_checker")
        rows = self.cur.fetchall()
        for row in rows:
            print("log_id =", row[0])
            print("check_time_epoch =", row[1])
            print("status_code =", row[2])
            print("response_time_seconds =", row[3])
            print("test_pattern_found =", row[4], "\n")







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
    
    
    database = Database(logger,conf)

    database.cur.execute('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\'')
    print(database.cur.fetchall())

    database.print_all_content()





 

    logger.info("starting the consumer")
    for msg in consumer:
        logger.debug("data received = {}".format(json.loads(msg.value)))
        rec = json.loads(msg.value)
        database.cur.execute("INSERT INTO website_checker (CHECK_TIME_EPOCH,STATUS_CODE,RESPONSE_TIME_SECONDS,TEST_PATTERN_FOUND) VALUES (%s, %s, %s, %s)", \
            (rec['check_time_epoch'],rec['status_code'],rec['response_time_seconds'],rec['test_pattern_found'],));
        #database.print_all_content()

    database.close_connection()