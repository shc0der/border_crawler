from injector import Module, singleton, provider

from app.core.settings import Settings


class CoreModule(Module):

    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()
