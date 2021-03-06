import logging
from django.conf import settings
from mongoengine import connection
import mongo_proxy

logger = logging.getLogger(__name__)


def init_mongo_connection(settings_databases_conf):
    '''
    Initialize MongoDB connectivity
    '''
    for db_name, kwargs in settings_databases_conf.items():
        if not db_name:
            logger.info('Skipping empty mongodb name')
            continue

        if kwargs.get('disabled'):
            logger.info('Skipping disabled MongoDB configuration for "%s"' % db_name)
            continue

        if not kwargs.get('alias') or not kwargs.get('host'):
            raise RuntimeError('MongoDB configuration for "%s" needs to specify alias and host' % db_name) 
        
        connection.connect(db_name, **kwargs)
        db_alias = kwargs['alias']
        # wrap the connections with the proxy which handles AutoReconnect
        mongo_conn = connection._connections[db_alias]
        mongo_conn_proxied = mongo_proxy.MongoProxy(mongo_conn)
        connection._connections[db_alias] = mongo_conn_proxied
        logger.debug('Connected to %s', db_name)


init_mongo_connection(settings.MONGODB_DATABASES)
