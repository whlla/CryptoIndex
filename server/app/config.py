import configparser

config_file = 'config.ini'


def get_mongo_config():
    """
    Reads MongoDB config values from config file

    :return: set of: user, passwd, auth_db, host
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    user = config.get('MONGO', 'user', fallback='crpytoRW')
    passwd = config.get('MONGO', 'passwd', fallback='crypto')
    auth_db = config.get('MONGO', 'authDb', fallback='crypto')
    host = config.get('MONGO', 'host', fallback='database:27017')

    return user, passwd, auth_db, host


def get_exchange_config(exchange_str):
    """
    Reads MongoDB config values from config file

    :param exchange_str: exchange string for which you want config
    :return: set of: api_key, secret
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    api_key = config.get(exchange_str, 'apiKey')
    secret = config.get(exchange_str, 'secret')

    if any(x is None for x in [api_key, secret]):
        # error
        print()

    return api_key, secret
