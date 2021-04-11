class website_info:
    def __init__(self):
        self.check_time_epoch = 0
        self.status_code = 0
        self.response_time_seconds = 0
        self.test_pattern_found = 0

    def get_website_info(self):
        return{
        "check_time_epoch": self.check_time_epoch,
        "status_code": self.status_code,
        "response_time_seconds": self.response_time_seconds,
        "test_pattern_found" : self.test_pattern_found
    }