# 代码生成时间: 2025-09-07 11:05:21
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import DEFAULT_DB_ALIAS as DEFAULT_DB_ALIAS
from psycopg2 import pool
import logging

"""
Database connection pool management for Django applications.
This module provides a way to manage database connections using a connection pool.
"""

logger = logging.getLogger(__name__)

class DBPool:
    """
    A connection pool manager for Django databases.

    This class manages a pool of database connections, allowing for efficient
    reuse of connections and reducing the overhead of repeatedly
    creating and destroying connections.
    """
    def __init__(self, db_alias=DEFAULT_DB_ALIAS):
        """
        Initialize the connection pool.

        Args:
            db_alias (str, optional): The alias of the database to manage. Defaults to DEFAULT_DB_ALIAS.
        """
        self.db_alias = db_alias
        self.pool = None
        self._setup_pool()

    def _setup_pool(self):
        """
        Set up the connection pool.

        This method creates a new connection pool based on the database settings
        specified in the Django project's settings file.
        """
        settings_dict = connections[self.db_alias].settings_dict
        max_connections = settings_dict.get('POOL_MAX_CONNECTIONS', 10)
        min_connections = settings_dict.get('POOL_MIN_CONNECTIONS', 2)
        self.pool = pool.ThreadedConnectionPool(
            min_connections,
            max_connections,
            settings_dict['NAME'],
            user=settings_dict['USER'],
            password=settings_dict['PASSWORD'],
            host=settings_dict['HOST'],
            port=settings_dict['PORT'],
            requiressl=settings_dict.get('REQUIRESSL', False),
        )
        logger.info(f'Connection pool set up for {self.db_alias}')

    def get_connection(self):
        """
        Get a connection from the pool.

        Returns:
            connection: A database connection from the pool.
        """
        try:
            connection = self.pool.getconn()
            logger.info('Connection retrieved from pool')
            return connection
        except Exception as e:
            logger.error('Failed to retrieve connection from pool', exc_info=True)
            raise e

    def release_connection(self, connection):
        """
        Release a connection back to the pool.

        Args:
            connection: The connection to release.
        """
        try:
            self.pool.putconn(connection)
            logger.info('Connection released to pool')
        except Exception as e:
            logger.error('Failed to release connection to pool', exc_info=True)
            raise e

    def close_all_connections(self):
        """
        Close all connections in the pool.
        """
        try:
            self.pool.closeall()
            logger.info('All connections closed')
        except Exception as e:
            logger.error('Failed to close all connections', exc_info=True)
            raise e

# Example usage:
if __name__ == '__main__':
    db_pool = DBPool()
    connection = db_pool.get_connection()
    # Use the connection for database operations
    db_pool.release_connection(connection)
    db_pool.close_all_connections()
