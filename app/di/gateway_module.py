from injector import Module, singleton, provider

from app.core.settings import Settings
from app.db.engine_database import EngineDatabase


class GatewayModule(Module):

    @singleton
    @provider
    def provide_engine(self, settings: Settings) -> EngineDatabase:
        return EngineDatabase(settings.SQLALCHEMY_DATABASE_URI)
