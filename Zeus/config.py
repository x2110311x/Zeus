import logging
import configparser
import os
import shutil

log = logging.getLogger(__name__)
class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.find_file()
        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding='utf-8')

    def find_file(self):
        config = configparser.ConfigParser(interpolation=None)
        if not os.path.isfile(self.config_file):
            if os.path.isfile(self.config_file + '.ini'):
                self.config_file = self.config_file + '.ini'
                log.info(f"Please add .ini to the config_file name")
            elif os.path.isfile("config/example_config.ini"):
                shutil.copy('config/example_config.ini', self.config_file)
                log.warning('Config was not found. Copying exmaple_config.ini')
            else:
                raise Exception("The config file is missing. Please grab the example_config.ini from the GitHub Repo")
        
        if not config.read(self.config_file, encoding='utf-8'):
            raise Exception("Could not parse the config file. Please check it and try again")