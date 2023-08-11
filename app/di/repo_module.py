from injector import Module, singleton, provider

from app.repos.border_repo import BorderRepo
from app.repos.dao.border_dao import BorderDao
from app.repos.dao.data_dao import DataDao
from app.repos.data_repo import DataRepo


class RepoModule(Module):

    @singleton
    @provider
    def provide_data_dao(self) -> DataDao:
        return DataDao()

    @singleton
    @provider
    def provide_border_dao(self) -> BorderDao:
        return BorderDao()

    @singleton
    @provider
    def provide_data_repo(self, data_dao: DataDao) -> DataRepo:
        return DataRepo(data_dao)

    @singleton
    @provider
    def provide_border_repo(self, border_dao: BorderDao) -> BorderRepo:
        return BorderRepo(border_dao)
