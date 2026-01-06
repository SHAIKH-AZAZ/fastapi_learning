import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from sqlmodel import SQLModel

from app.Database.models import Shipment , Seller , DeliveryPartner
from app.config import db_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


config.set_main_option(
    "sqlalchemy.url",db_settings.POSTGRES_URL
)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata