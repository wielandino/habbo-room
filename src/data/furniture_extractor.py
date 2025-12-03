import os
import definitions
from bs4 import BeautifulSoup


class FurnitureExtractor:
    path: str = f"{definitions.ROOT_DIR}/src/data/furnitures/"

    def __init__(self, type: str):
        self.type = type

        self.__set_path(type)

    def __set_path(self, type: str):
        self.path = os.path.join(self.path, f"{type}/xml/")

    def __load_furniture_manifest_xml(self):
        with open(os.path.join(self.path, "manifest.xml"), "r", encoding="utf-8") as file:
            content = file.read()

        soup = BeautifulSoup(content, "xml")
        return soup

    def __load_furniture_asset_xml(self):
        with open(os.path.join(self.path, "assets.xml"), "r", encoding="utf-8") as file:
            content = file.read()

        soup = BeautifulSoup(content, "xml")
        return soup
    
    def __load_furniture_visualization_xml(self):
        with open(os.path.join(self.path, "visualization.xml"), "r", encoding="utf-8") as file:
            content = file.read()

        soup = BeautifulSoup(content, "xml")
        return soup

    def extract(self):
        manifest_soup = self.__load_furniture_manifest_xml()

        if not self.__is_manifest_valid(manifest_soup):
            return None
        
        asset_soup = self.__load_furniture_asset_xml()
        visualization_soup = self.__load_furniture_visualization_xml()

    
        


    def __is_manifest_valid(self, soup: BeautifulSoup) -> bool:
        # Check if furniture has assets and visualization xml
        if soup.find("assets", {"name": f"{self.type}_visualization"}) is None:
            return False
        
        if soup.find("assets", {"name": f"{self.type}_assets"}) is None:
            return False

        return True

    
