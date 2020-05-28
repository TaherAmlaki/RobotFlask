import json


def parse_configuration_file():
    with open("./configuration.json", "r") as jf:
        conf = json.load(jf)
    return conf.get("SuitesDirectory", ".")