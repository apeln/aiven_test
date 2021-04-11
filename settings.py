import configparser
import logging


class settings:
    def __init__(self):
        filename = "settings.ini"
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
                        raise Exception('settings.ini wrong format')
                    for param in params:
                        self.conf[param[0]] = param[1]

                else:
                    raise Exception('Section {0} not found in the {1} file'.format(section, filename))


        required_options = ['KafkaServerOptions','WebsiteCheckerProducer','DatabaseStorerConsumer']
        for option in required_options:
            settings_file.has_option()

        self.bootstrap_server = settings_file.get("KafkaServerOptions","BootstrapServer")
        self.website_checker_topic = settings_file.get("KafkaServerOptions","Topic")
        self.target_website = settings_file.get("WebsiteCheckerProducer","TargetWebsite")
        self.delta_time_availability_check_sec = settings_file.getint("WebsiteCheckerProducer","DeltaTimeCheckSeconds")
        self.database_uri = settings_file.get("DatabaseStorerConsumer","DataBaseUri")
        try:
            assert settings_file.has_option("WebsiteCheckerProducer","TargetWebsite") 
        except AssertionError:
            logging.error("NTargetWebsite ", exc_info=True)

        self.pattern_expected_to_be_found = settings_file.get("WebsiteCheckerProducer","PatternToMatch")

        self.consumer_group_id = settings_file.get("DatabaseStorerConsumer","GroupId")


