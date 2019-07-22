from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import (
    database_exists,
    create_database)

from models import Base

# in the other world in better times we will get our db_connection_string from config file
db_connection_string = 'sqlite:///robot.db'


class Connection:
    # let's create connection object
    def __init__(self, url):
        self._engine = create_engine(url)
        self._session = sessionmaker(bind=self._engine).__call__()

    def get_engine(self):
        return self._engine

    @property
    def session(self):
        return self._session

    def close(self):
        self._session.close()


@contextmanager
def session_scope():
    # if we work with sqlalchemy we want to keep our sessions in the good state
    connection = Connection(db_connection_string)
    session = connection.session

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def db_maker():
    # just for convenience
    engine = create_engine(db_connection_string)
    if not database_exists(engine.url):
        create_database(engine.url)


def create_table():
    # just for convenience
    Base.metadata.create_all(create_engine(db_connection_string))


def convert_to_stop_points(self):
    result = []
    for idx, val in enumerate(self.routing_points):
        try:
            result.append([val, self.routing_points[idx + 1]])
        except IndexError:
            break
    return result

