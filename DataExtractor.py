

class DataExtractor(object):
    def __init__(self):
        pass
    
    def extract (self, json_data):
        data_dict = {}
        if len(json_data) != 0:            
            data_dict["created_at"] = json_data["created_at"]
            data_dict["text"] = json_data["text"]
            data_dict["user_name"] = json_data ["user"]["name"]
            data_dict["user_location"] = json_data["user"]["location"]
        return data_dict

        





