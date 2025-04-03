from configparser import ConfigParser
from typing import Dict


def config(filename="config.ini", section="postgres") -> Dict:
    """функция для чтения файла конфигурации"""
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} is not found in the {1} file".format(section, filename)
        )

    print(f"Database parameters: {db}")
    return db


if __name__ == "__main__":
    config()
