from src.objects.furniture.furniture_base import FurnitureBase
from src.data.furniture_extractor import FurnitureExtractor


class FurnitureRegistry:
    
    __instance = None
    __furniture_cache: dict[str, FurnitureBase] = {}
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    @classmethod
    def load_furniture(cls, furniture_type: str) -> FurnitureBase:
        if furniture_type in cls.__furniture_cache:
            print(f"{furniture_type} from cache")
            return cls.__furniture_cache[furniture_type]
        
        print(f"Create new furniture: {furniture_type}")

        extractor = FurnitureExtractor(furniture_type)
        furniture = extractor.extract()

        if furniture:
            cls.__furniture_cache[furniture_type] = furniture
            return furniture
        else:
            return None
    
    @classmethod
    def preload_all(cls, furniture_types: list[str]):
        for furniture_type in furniture_types:
            cls.load_furniture(furniture_type)

    def get_registry(self):
        return self.__furniture_cache