from perception import Map

# Last row:
# (i, j)
# (0,0) (1, 0) (2, 0) (3, 0)
# 0 1 2 3

def get_quarto_map(n=5, client=False):
    if client:
        from perception import ClientMap
        world_map = ClientMap()
    else:
        world_map = Map()

    world_map.add_node(0, 0, 0)
    world_map.add_node(1, 100, 0)
    world_map.add_node(2, 100, -53)
    world_map.add_node(3, 200, -53)
    world_map.add_edge(0, 1)
    world_map.add_edge(1, 2)
    world_map.add_edge(2, 3)

    return world_map