from items import *
from map import rooms

inventory = [item_id, item_laptop, item_money]

# Start game at the reception
current_room = rooms["Reception"]

mass = items["laptop"]["mass"] + items["id"]["mass"] + items["money"]["mass"]
maximum_weight = 4.0
