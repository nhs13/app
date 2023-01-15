import json
from pathlib import Path

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine

config_file = Path(__file__).parent / "config.json"
print(config_file)
with config_file.open() as f:
    config = json.load(f)


url = f"postgresql+asyncpg://{config['username']}:{config['password']}@localhost:5432/app_db"
engine = create_async_engine(
    url, pool_recycle=4000, pool_pre_ping=True, pool_use_lifo=True, pool_size=3
)
