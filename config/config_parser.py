from enum import Enum

class ConfigType(Enum):
    CONIG_TYPE_JSON = 1

config_type_used = ConfigType.CONIG_TYPE_JSON
config_file_name = 'config'

def loadConfigFile_JSON(path):
	import json
	data = json.load(open(path + config_file_name + ".json", 'r'))
	return data


configs = {
	ConfigType.CONIG_TYPE_JSON: loadConfigFile_JSON
}

def loadConfigFile(path):
	config_dict = configs[config_type_used](path+"/")
	return config_dict

