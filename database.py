
import psycopg2
from logger_common import get_logger
import traceback
import sys

class database_handler:
    def __init__(self,logger,conf):
        self.db_conn = None
        self.cur = None
        self.logger = logger
        self.conf = conf
        self.connect()
        

    
    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # connect to the PostgreSQL server
            
            
            self.logger.info('Connecting to the PostgreSQL database via uri : {0}'.format(self.conf.database_uri))
            database_uri = self.conf.database_uri
            
            self.db_conn = psycopg2.connect(database_uri)
            
            self.logger.info("Creating cursor")
            self.cur = self.db_conn.cursor()
            
            

            self.logger.info('PostgreSQL database version:')
            self.cur.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self.cur.fetchone()

            self.logger.info(db_version)

            # create table if doesn't exist
            self.cur.execute('CREATE TABLE IF NOT EXISTS website_checker ('
                                '  LOG_ID SERIAL PRIMARY KEY,  '
                                '  CHECK_TIME_EPOCH INT not null,'
                                '  STATUS_CODE INT not null,'
                                '  RESPONSE_TIME_SECONDS FLOAT not null,'
                                '  TEST_PATTERN_FOUND INT not null)')



        except (Exception, psycopg2.DatabaseError) as error: ## log error and exit
            self.logger.fatal(error)
            sys.exit(error)

    def execute_sql_query(self,sql_query):
        self.cur.execute(sql_query)

    def close_connection(self):
        # close the communication with the PostgreSQL
        if self.cur is not None:
            self.cur.close()
        if self.db_conn is not None:
            self.db_conn.close()
        self.logger.info('Database connection closed.')

    def print_all_content(self):
        self.cur.execute("SELECT * from website_checker")
        rows = self.cur.fetchall()
        for row in rows:
            print("log_id =", row[0])
            print("check_time_epoch =", row[1])
            print("status_code =", row[2])
            print("response_time_seconds =", row[3])
            print("test_pattern_found =", row[4], "\n")
