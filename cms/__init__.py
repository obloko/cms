import logger
from django.conf import settings
from mongoengine import connection
import mongodb_proxy

logger = logging.getLogger(__name__)


def init_mongo_connection(settings_databases_conf):
    '''
    Initialize MongoDB connectivity
    '''
    for db_name, kwargs in settings_databases_conf.items():
        connection.connect(db_name, **kwargs)
        db_alias = kwargs['alias']
        # wrap the connections with the proxy which handles AutoReconnect
        mongo_conn = connection._connections[db_alias]
        mongo_conn_proxied = mongodb_proxy.MongoProxy(mongo_conn)
        connection._connections[db_alias] = mongo_conn_proxied
        logger.debug('Connected to %s', db_name)


init_mongo_connection(settings.MONGODB_DATABASES)
