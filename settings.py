import configparser
from pathlib import Path
import sys




class settings:
    def __init__(self, logger):
        filename = "settings.ini"
        filename_path = Path(filename)
        if not filename_path.is_file():
            msg = "{0} - file doesn't exist. Aborting".format(filename)
            logger.critical(msg)
            sys.exit(msg)
        settings_file = configparser.ConfigParser()
        settings_file.read(filename) #check for successful read and all the required parameters are present

        required_components_dict = {
            'KafkaServerOptions' : ["BootstrapServer","Topic"],
            'WebsiteCheckerProducer' : ["TargetWebsite","DeltaTimeCheckSeconds", "PatternToMatch"],
            'DatabaseStorerConsumer' : ["GroupId","DataBaseUri"],
        }

        self.conf = {}
        for section in required_components_dict:
                if settings_file.has_section(section):
                    params = settings_file.items(section)
                    params_names = [item[0].lower() for item in params]
                    params_names_required = [item.lower() for item in required_components_dict[section]]
                    intersection = list(set(params_names) & set(params_names_required))
                    if(len(intersection)!=len(params_names_required)):
                        msg = "{0} - wrong format. Aborting".format(filename)
                        logger.critical(msg)
                        sys.exit(msg)
                else:
                    msg = 'Section {0} not found in the {1} file'.format(section, filename)
                    logger.critical(msg)
                    sys.exit(msg)

        self.bootstrap_server = settings_file.get("KafkaServerOptions","BootstrapServer")
        self.website_checker_topic = settings_file.get("KafkaServerOptions","Topic")
        self.target_website = settings_file.get("WebsiteCheckerProducer","TargetWebsite")
        self.delta_time_availability_check_sec = settings_file.getint("WebsiteCheckerProducer","DeltaTimeCheckSeconds")
        self.database_uri = settings_file.get("DatabaseStorerConsumer","DataBaseUri")
        self.pattern_expected_to_be_found = settings_file.get("WebsiteCheckerProducer","PatternToMatch")
        self.consumer_group_id = settings_file.get("DatabaseStorerConsumer","GroupId")

        msg = '{0} configuration file successfull load'.format(filename)
        logger.info(msg)


