from dao.release_search_dao import ReleaseSearchDao
from model.center_trade import Stock
from model.center_trade import K

class ReleaseSearchService:
    @staticmethod
    def search(content):
        stock_info = ReleaseSearchDao.get1(content)
        return stock_info
    
    @staticmethod
    def advancedsearch(content):
        stock_info = ReleaseSearchDao.get2(content)
        return stock_info