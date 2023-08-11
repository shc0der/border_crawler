from datetime import datetime, timedelta, date
from typing import List, Tuple

from injector import Injector

from app.di.app_module import AppModule
from app.di.core_module import CoreModule
from app.di.gateway_module import GatewayModule
from app.di.repo_module import RepoModule
from app.di.service_module import ServiceModule
from app.workers.crawler_pool_executor import CrawlerPoolExecutor


def main(borders: List[str], start_date: date, end_date: date):
    injector = Injector([AppModule, CoreModule, GatewayModule, RepoModule, ServiceModule])

    executor = injector.get(CrawlerPoolExecutor)

    executor.setup(borders, start_date, end_date)

    executor.start()
    executor.wait()


def date_range() -> Tuple[date, date]:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=730)

    return start_date, end_date


if __name__ == '__main__':

    start, end = date_range()

    main(["brest", "privalka", "kotlovka", "stone_log", "losha"], start, end)
