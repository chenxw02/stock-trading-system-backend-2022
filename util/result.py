class Result:
    @staticmethod
    def error(code, message):
        result = {}
        result["code"] = code
        result["message"] = message
        return result

    @staticmethod
    def success(data):
        result = {}
        result["code"] = 0
        result["message"] = "success"
        result["data"] = data
        return result