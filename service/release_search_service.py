from dao.release_search_dao import ReleaseSearchDao
from model.release_search import Stock
from model.release_search import K

class ReleaseSearchService:
    @staticmethod
    def search(content):
        stock_info = ReleaseSearchDao.get1(content)
        return stock_info
    
    @staticmethod
    def advancedsearch(content):
        stock_info = ReleaseSearchDao.get2(content)
        return stock_info