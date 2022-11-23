from aiohttp import web


class PostgresAccessor:
    def __init__(self):
        from app.forum.models import Message
        self.message = Message
        self.db = None

    async def _on_connect(self, application: web.Application):
        from app.store.database.models import db
        self.config = application["config"]["postgres"]
        await db.set_bind(self.config["database_url"])
        self.db = db

    async def _on_disconnect(self, _):
        if self.db is not None:
            await self.db.pop_bind().close()

    def setup(self, application: web.Application):
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)
