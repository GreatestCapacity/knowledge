from lib import database
from lib.data_access import DataAccess
import config


class Environment:
    # SQLAlchemy engine
    engine = database.engine

    # SQLAlchemy Base
    Base = database.Base

    # Work Directory
    working_directory = '/'

    # configuration
    configuration = config

    # Database Entities
    Base = database.Base
    Notebook = database.Notebook
    Note = database.Note
    Tag = database.Tag
    Image = database.Image

    # Commands
    cmd_descriptions = []
    cmd_details = {}
    cmd_processors = {}
    cmd_completers = {}

    # Data Access Method
    data_access = DataAccess(engine)
