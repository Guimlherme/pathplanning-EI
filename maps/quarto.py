from perception import Map

# Last row:
# (i, j)
# (0,0) (1, 0) (2, 0) (3, 0)
# 0 1 2 3

def get_quarto_map(client=False):
    if client:
        from perception import ClientMap
        world_map = ClientMap()
    else:
        world_map = Map()

    world_map.add_node(0, 0, 0)
    world_map.add_node(1, 0, 100)
    world_map.add_node(2, 0, 200)
    world_map.add_node(3, 100, 0)
    world_map.add_node(4, 100, 100)
    world_map.add_node(5, 100, 200)
    world_map.add_node(6, 100, 300)
    world_map.add_edge(0, 1)
    world_map.add_edge(1, 2)
    world_map.add_edge(3, 4)
    world_map.add_edge(4, 5)
    world_map.add_edge(5, 6)
    world_map.add_edge(0, 3)
    world_map.add_edge(1, 4)
    world_map.add_edge(2, 5)

    return world_map