from injector import Module, singleton, provider

from app.workers.border.border_crawler import BorderCrawler
from app.workers.crawler_pool_executor import CrawlerPoolExecutor
from app.workers.parser.parser_crawler import ParserCrawler


class AppModule(Module):

    @singleton
    @provider
    def provide_executor(self, border_crawler: BorderCrawler, parser_crawler: ParserCrawler) -> CrawlerPoolExecutor:
        return CrawlerPoolExecutor(border_crawler=border_crawler, parser_crawler=parser_crawler)
