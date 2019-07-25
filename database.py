import os
from urllib.parse import urlparse

def parse_db_url(database_url):
    parsed = urlparse(database_url)
    return {
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'database': parsed.path[1:]
    }

def return_db():
    db_config = parse_db_url(os.environ['DATABASE_URL'])

    if os.getenv('MIGRATION', '0') == '1':
        from playhouse.postgres_ext import PostgresqlExtDatabase

        return PostgresqlExtDatabase(
            db_config['database'],
            user=db_config.get('user', None),
            password=db_config.get('password', None),
            host=db_config.get('host', 'localhost'),
            port=db_config.get('port', '5432'))

    else:
        from playhouse.pool import PooledPostgresqlExtDatabase

        return PooledPostgresqlExtDatabase(
            db_config['database'],
            max_connections=os.getenv('DB_POOL', 5),
            stale_timeout=os.getenv('DB_TIMEOUT', 300),  # 5 minutes.
            user=db_config.get('user', None),
            password=db_config.get('password', None),
            host=db_config.get('host', 'localhost'),
            port=db_config.get('port', '5432'))

db = return_db()
