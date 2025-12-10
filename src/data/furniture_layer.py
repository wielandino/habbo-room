from src.data.furniture_asset import FurnitureAsset
from src.utils.xml_layer import get_layer_id_from_letter
from dataclasses import dataclass, field

@dataclass
class FurnitureLayer:
    layer_id: int
    type: str
    z_index: int
    assets: dict[int, list[FurnitureAsset]] = field(default_factory=dict) # int -> direction

    
    ink: str = None
    alpha: int = None
    ignore_mouse: bool = False

    @staticmethod
    def get_layer_id_from_letter(letter: str) -> int:
        return get_layer_id_from_letter(letter)

    def add_asset_to_layer(self, direction_id: int, asset: FurnitureAsset):
        self.assets[direction_id] = asset