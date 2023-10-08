import aiopg
import json
from aiogram.dispatcher.storage import BaseStorage

class PostgresStorage(BaseStorage):
    def __init__(self, dsn):
        self.dsn = dsn

    async def close(self):
        pass

    async def wait_closed(self):
        pass

    async def get_state(self, chat, user, default=None):
        async with aiopg.create_pool(self.dsn) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT state FROM states WHERE chat = %s AND user_id = %s", (chat, user))
                    row = await cur.fetchone()
                    if row is not None:
                        return row[0]
                    else:
                        return default

    async def get_data(self, chat, user, default=None):
        async with aiopg.create_pool(self.dsn) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT data FROM states WHERE chat = %s AND user_id = %s", (chat, user))
                    row = await cur.fetchone()
                    if row is not None:
                        if isinstance(row[0], str):
                            return json.loads(row[0])
                        else:
                            return row[0] # Если это уже словарь, просто возвращаем его
                    else:
                        return default

    async def set_state(self, chat, user, state):
        async with aiopg.create_pool(self.dsn) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("INSERT INTO states (chat, user_id, state) VALUES (%s, %s, %s) ON CONFLICT (chat, user_id) DO UPDATE SET state = %s", (chat, user, state, state))

    async def set_data(self, chat, user, data):
        async with aiopg.create_pool(self.dsn) as pool:
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("INSERT INTO states (chat, user_id, data) VALUES (%s, %s, %s) ON CONFLICT (chat, user_id) DO UPDATE SET data = %s", (chat, user, json.dumps(data), json.dumps(data)))

    async def update_data(self, chat, user, data):
        current_data = await self.get_data(chat, user)
        if current_data is None:
            current_data = {}
        current_data.update(data)
        await self.set_data(chat, user, current_data)

    async def reset_data(self, chat, user):
        await self.set_data(chat, user, {})

    async def finish(self, chat, user):
        await self.set_state(chat, user, None)
        await self.reset_data(chat, user)
