import os

if os.getenv('MIGRATION', '0') == '1':
    from playhouse.postgres_ext import PostgresqlExtDatabase
    db = PostgresqlExtDatabase('nextagram_dev')

else:
    from playhouse.db_url import parse
    from playhouse.pool import PooledPostgresqlExtDatabase

    db_config = parse(os.environ['DATABASE_URL'])

    db = PooledPostgresqlExtDatabase(
        db_config['database'],
        max_connections=os.getenv('DB_POOL', 5),
        stale_timeout=os.getenv('DB_TIMEOUT', 300),  # 5 minutes.
        user=db_config.get('user', None),
        password=db_config.get('password', None),
        host=db_config.get('host', 'localhost'),
        port=db_config.get('port', '5432'))

