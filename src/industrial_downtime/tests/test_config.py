import pytest
from src.industrial_downtime.config import config

def test_db_config_keys():
    db = config.DB_CONFIG
    assert all(k in db for k in ["host", "port", "database", "user", "password"])
    assert isinstance(db["port"], int)