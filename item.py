from rl_inventory_api import Item as InventoryItem
from rl_insider_api.rlinsider import RlInsider
from rl_insider_api.item import Item as RLII
from rocket_league_utils import compare_rarities, compare_types, compare_colors, compare_certificates, is_decal
from rl_insider_api.constants import Rarities, Types

decal_cars = {'Metal-Carpus', 'Harbinger', 'Propeller', 'Masamune', 'Road Hog', 'X-Devil', 'Traction', 'Agasaya',
              'Breakout', 'Octane', 'Tanker', 'Dominus', 'Polyergic', 'Venom', 'Blacklight', 'Paladin', 'Endo',
              'Dominus GT', 'Imperator DT5', 'Jäger 619', 'Esoto 4R', 'X-Devil Mk2', 'Aftershock', '3-Lobe', 'Mantis',
              'Zadeh S3', 'Hotshot', 'Mandala', 'Gadabout', 'Ripper', 'Esper', 'Peregrine TT', 'R3MX', 'Centio',
              'Animus GP', 'Hamster', 'Breakout Type-S', 'Merc', 'Takumi', 'Fennec', 'Ruinator', 'Gizmo', 'Takumi RX-T',
              'Octane ZSR'}


class Item(InventoryItem):
    def __init__(self, product_id, name, slot, paint, certification, certification_value, certification_label, quality,
                 crate, tradeable, amount, instance_id, min_price, max_price):
        super().__init__(product_id, name, slot, paint, certification, certification_value, certification_label,
                         quality, crate, tradeable, amount, instance_id)
        self.min_price, self.max_price = min_price, max_price

    @staticmethod
    def from_inventory_item(item, rl_insider: RlInsider):
        search = rl_insider.search(lambda rli: Item.custom_search(item, rli))
        try:
            insider_item = search.get_item()
        except IndexError:
            search = rl_insider.search(lambda rli: Item.custom_search(item, rli, True))
            insider_item = search.get_item()
        try:
            min_price, max_price = insider_item.get_price_pc("Default" if item.paint == "none" else item.paint)
        except TypeError:
            min_price, max_price = 0, 0
        return Item(*item.__dict__.values(), min_price, max_price)

    @staticmethod
    def custom_search(item: InventoryItem, rli: RLII, ignore_rarity=False):
        if is_decal(item.slot) and any([car in item.name for car in decal_cars]):
            nc = Item.translate_decal_name(item.name).lower() in rli.translations[0].lower()
        else:
            nc = item.name.lower() in rli.translations[0].lower()
        cc = any(compare_colors(item.paint, c) for c in rli.get_colors())
        if ignore_rarity:
            rc = True
        else:
            rc = any(compare_rarities(item.quality, r) for r in rli.get_rarities())
        tc = compare_types(item.slot, rli.get_type())
        return all([nc, cc, rc, tc])

    @staticmethod
    def translate_decal_name(name):
        car, decal_name = name.split(":")
        return f"{decal_name.strip()} [{car}]"
