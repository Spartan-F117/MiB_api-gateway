class Config(object):
    """
    Main Configuration for Go Out Safe API Gateway
    """
    DEBUG = False
    TESTING = False

    # configuring microservices endpoints
    import os

    REQUESTS_TIMEOUT_SECONDS = float(os.getenv("REQUESTS_TIMEOUT_SECONDS", 15))

    # configuring redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis_cache')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DB = os.getenv('REDIS_DB', '0')
    REDIS_URL = 'redis://%s:%s/%s' % (
        REDIS_HOST,
        REDIS_PORT,
        REDIS_DB
    )

    # lottery microservice
    LOTTERY_MS_PROTOCOL = os.getenv('LOTTERY_MS_PROTOCOL', 'http')
    LOTTERY_MS_HOST = os.getenv('LOTTERY_MS_HOST', 'localhost')
    LOTTERY_MS_PORT = os.getenv('LOTTERY_MS_PORT', 5004)
    LOTTERY_MS_URL = '%s://%s:%s' % (LOTTERY_MS_PROTOCOL, LOTTERY_MS_HOST, LOTTERY_MS_PORT)

    # user microservice
    USERS_MS_PROTOCOL = os.getenv('USERS_MS_PROTOCOL', 'http')
    USERS_MS_HOST = os.getenv('USERS_MS_HOST', 'localhost')
    USERS_MS_PORT = os.getenv('USERS_MS_PORT', 5002)
    USERS_MS_URL = '%s://%s:%s' % (USERS_MS_PROTOCOL, USERS_MS_HOST, USERS_MS_PORT)

    # message microservice
    MESSAGE_MS_PROTOCOL = os.getenv('MESSAGE_MS_PROTOCOL', 'http')
    MESSAGE_MS_HOST = os.getenv('MESSAGE_MS_HOST', 'localhost')
    MESSAGE_MS_PORT = os.getenv('MESSAGE_MS_PORT', 5003)
    MESSAGE_MS_URL = '%s://%s:%s' % (MESSAGE_MS_PROTOCOL, MESSAGE_MS_HOST, MESSAGE_MS_PORT)

    # Configuring sessions
    SESSION_TYPE = 'redis'

    # secret key
    SECRET_KEY = os.getenv('APP_SECRET', b'isreallynotsecretatall')


class DebugConfig(Config):
    """
    This is the main configuration object for application.
    """
    DEBUG = True
    TESTING = False


class DevConfig(DebugConfig):
    """
    This is the main configuration object for application.
    """
    pass


class TestConfig(Config):
    """
    This is the main configuration object for application.
    """
    TESTING = True

    import os
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True


class ProdConfig(Config):
    """
    This is the main configuration object for application.
    """
    TESTING = False
    DEBUG = False

    import os
    SECRET_KEY = os.getenv('APP_SECRET', os.urandom(24))


