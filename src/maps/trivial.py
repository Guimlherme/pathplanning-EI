from perception import Map

def get_trivial_map():
    world_map = Map()
    world_map.add_node(0, 0, 0)
    world_map.add_node(1, 1, 0)
    world_map.add_edge(0, 1)
    return world_map