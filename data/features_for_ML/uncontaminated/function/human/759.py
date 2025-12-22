from pylabrobot.resources.coordinate import Coordinate
from pylabrobot.resources.deck import Deck

def create_a_coin_cell_deck():
    deck = Deck(size_x=1200,
                size_y=800,
                size_z=900)

    #liaopan =  TipBox64(name="liaopan")

    #创建一个4*4的物料板
    liaopan1 =  MaterialPlate(name="liaopan1", size_x=120.8, size_y=120.5, size_z=10.0, fill=True)
    #把物料板放到桌子上
    deck.assign_child_resource(liaopan1, Coordinate(x=0, y=0, z=0))
    #创建一个极片
    for i in range(16):
        jipian = ElectrodeSheet(name=f"jipian_{i}", size_x= 12, size_y=12, size_z=0.1)
        liaopan1.children[i].assign_child_resource(jipian, location=None)
    #创建一个4*4的物料板
    liaopan2 =  MaterialPlate(name="liaopan2", size_x=120.8, size_y=120.5, size_z=10.0, fill=True)
    #把物料板放到桌子上
    deck.assign_child_resource(liaopan2, Coordinate(x=500, y=0, z=0))

    #创建一个4*4的物料板
    liaopan3 =  MaterialPlate(name="liaopan3", size_x=120.8, size_y=120.5, size_z=10.0, fill=True)
    #把物料板放到桌子上
    deck.assign_child_resource(liaopan3, Coordinate(x=1000, y=0, z=0))

    print(deck)

    return deck