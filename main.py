from rl_inventory_value import RlInventoryValue


if __name__ == '__main__':
    rl_inventory_value = RlInventoryValue.from_inventory_csv()
    rl_inventory_value.save()
