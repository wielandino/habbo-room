import os
from data.furniture_asset import FurnitureAsset
import definitions
from bs4 import BeautifulSoup
import pygame

class FurnitureExtractor:
    path: str = f"{definitions.ROOT_DIR}/src/data/furnitures/"
    xml_path: str = "xml/"
    image_path: str = "images/"

    def __init__(self, type: str):
        self.type = type

        self.__set_path(type)

    def __set_path(self, type: str):
        self.path = os.path.join(self.path, f"{type}/")

    def __load_furniture_manifest_xml(self) -> BeautifulSoup:
        with open(os.path.join(self.path, f"{self.xml_path}manifest.xml"), "r", encoding="utf-8") as file:
            content = file.read()

        return BeautifulSoup(content, "xml")
        

    def __load_furniture_asset_xml(self) -> BeautifulSoup:
        with open(os.path.join(self.path, f"{self.xml_path}assets.xml"), "r", encoding="utf-8") as file:
            content = file.read()

        return BeautifulSoup(content, "xml")
      
    
    def __load_furniture_visualization_xml(self) -> BeautifulSoup:
        with open(os.path.join(self.path, f"{self.xml_path}visualization.xml"), "r", encoding="utf-8") as file:
            content = file.read()

        return BeautifulSoup(content, "xml")

    def __is_manifest_valid(self, soup: BeautifulSoup) -> bool:
        # Check if furniture has assets and visualization xml
        if soup.find("assets", {"name": f"{self.type}_visualization"}) is None:
            return False
        
        if soup.find("assets", {"name": f"{self.type}_assets"}) is None:
            return False

        return True
    
    def extract(self):
        manifest_xml = self.__load_furniture_manifest_xml()

        if not self.__is_manifest_valid(manifest_xml):
            return None
        
        asset_xml = self.__load_furniture_asset_xml()
        visualization_xml = self.__load_furniture_visualization_xml()

        for asset in asset_xml.find_all("asset"):
            name = asset.get("name")
            flip_h = asset.get("flipH") == "1"
            source = asset.get("source")
            offset_x = int(asset.get("x", "0"))
            offset_y = int(asset.get("y", "0"))
        
            if source is None:
                png_path = os.path.join(self.path, f"{self.image_path}{name}.png")
            else:
                png_path = os.path.join(self.path, f"{self.image_path}{source}.png")

            sprite = None
            if os.path.exists(png_path):
                sprite = pygame.image.load(png_path).convert_alpha()

            asset = FurnitureAsset(
                flip_h=flip_h,
                type=self.type,
                offset_x=offset_x,
                offset_y=offset_y,
                source_name=name,
                sprite=sprite
            )

    
