import configparser

from src.Common.Constant import *

def __read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH, encoding="utf-8")
    
    return config

def get_config(section, option):
    config = __read_config()
    value = config[section].get(option)
    
    return value

def getint_config(section, option):
    config = __read_config()
    value = config[section].getint(option)
    
    return value
