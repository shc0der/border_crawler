from injector import Module, singleton, provider

from app.core.settings import Settings
from app.db.engine_database import EngineDatabase
from app.repos.border_repo import BorderRepo
from app.repos.data_repo import DataRepo
from app.workers.border.border_crawler import BorderCrawler
from app.workers.border.border_worker_factory import BorderWorkerFactory
from app.workers.parser.parser_crawler import ParserCrawler
from app.workers.parser.parser_worker_factory import ParserWorkerFactory


class ServiceModule(Module):

    @singleton
    @provider
    def provide_border_worker_factory(self, settings: Settings, data_repo: DataRepo, engine: EngineDatabase) -> BorderWorkerFactory:
        return BorderWorkerFactory(settings.BORDER_URL, settings.COOKIE_URL, settings.HEADERS, data_repo, engine)

    @singleton
    @provider
    def provide_parser_worker_factory(self, data_repo: DataRepo, border_repo: BorderRepo, engine: EngineDatabase) -> ParserWorkerFactory:
        return ParserWorkerFactory(data_repo, border_repo, engine)

    @provider
    def provide_border_crawler(self, border_factory: BorderWorkerFactory) -> BorderCrawler:
        return BorderCrawler(border_factory)

    @provider
    def provide_parser_crawler(self, parser_factory: ParserWorkerFactory) -> ParserCrawler:
        return ParserCrawler(parser_factory)
