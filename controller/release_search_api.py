import json
from flask import Blueprint, request
from service.release_search_service import ReleaseSearchService
from util.result import Result

release_search_api = Blueprint('release_search_api', __name__)

@release_search_api.route("/release_search", methods=["POST"])
def search():
    data = json.loads(request.get_data(as_text=True))
    res = ReleaseSearchService.search(data["content"])
    return Result.success(res)

@release_search_api.route("/release_search_advanced", methods=["POST"])
def advancedsearch():
    data = json.loads(request.get_data(as_text=True))
    res = ReleaseSearchService.advancedsearch(data["content"])
    return Result.success(res)