from surrealdb import Surreal
from typing import Optional
from .config import settings

class Database:
    _instance: Optional[Surreal] = None

    @classmethod
    async def get_client(cls) -> Surreal:
        if cls._instance is None:
            cls._instance = Surreal(settings.surreal_url)
            await cls._instance.connect()
            await cls._instance.signin({
                "user": settings.surreal_user,
                "pass": settings.surreal_pass,
            })
            await cls._instance.use(settings.surreal_ns, settings.surreal_db)
        return cls._instance

    @classmethod
    async def close(cls):
        if cls._instance:
            await cls._instance.close()
            cls._instance = None

async def get_db() -> Surreal:
    return await Database.get_client()
