from dataclasses import dataclass, field

from src.data.furniture_asset import FurnitureAsset
from src.data.furniture_layer import FurnitureLayer

@dataclass
class FurnitureBase:
    name: str
    tile_width: int
    tile_height: int
    layers: list[FurnitureLayer]
    all_assets: dict[str, FurnitureAsset]
    possible_directions: list[int] 