from pathlib import Path
import csv
from item import Item
from rl_inventory_api import Inventory
from rl_insider_api import RlInsider

# ?INT?TAGame.ProductSeries.Series544? são items de loja!


class RlInventoryValue:
    def __init__(self, items):
        self.items = items

    @staticmethod
    def from_inventory_csv():
        rl_insider = RlInsider.connect_pc()
        inventory = RlInventoryValue.get_tradeable_inventory()
        rl_insider.data.sort(key=lambda item: item.url_name)
        return RlInventoryValue([Item.from_inventory_item(item, rl_insider) for item in inventory.items])

    def save(self, path=str(Path.home()) + "\\priced_inventory.csv"):
        with open(path, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["product id", "name", "slot", "paint", "certification", "certification value",
                             "certification label", "quality", "crate", "tradeable", "amount", "instanceid",
                             "min price", "max price"])
            writer.writerows([list(item.__dict__.values()) for item in self.items])

    @staticmethod
    def get_tradeable_inventory():
        return Inventory.read().filter(lambda item: item.slot != "Blueprint" and item.tradeable == "true" and not
                                                    (item.quality == "Limited" and item.paint == "none") and
                                       "?INT?TAGame.ProductSeries.Series" not in item.crate
                                                and item.quality != 'UNKNOWN?')
