from abc import ABC, abstractmethod
import pandas as pd


class DataStorageInterface(ABC):
    
    @abstractmethod
    def store_data (self, data):
        pass

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def get_data(self, tag_list):
        pass


class InMemoryDataStorage (DataStorageInterface):

    def __init__(self, data_extractor):
        self.dataStore = []
        self.data_extractor = data_extractor

    def store_data (self, data):
        if self.data_extractor is not None:
            extract_data = self.data_extractor.extract (data)
            self.dataStore.append (extract_data)
        else:
            self.dataStore.append (data)
    
    def read_data(self):
        return self.dataStore

    def get_data(self, tag_list):
        if len(tag_list) != 0:
            try:
                df = pd.DataFrame (self.read_data())
                return df [tag_list]
            except Exception as err:
                raise err

        else:
            print ("Tag List Empty")

        

