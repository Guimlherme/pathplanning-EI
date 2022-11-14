from perception import Map

def get_eight_map(client=False):
    if client:
        from perception import ClientMap
        world_map = ClientMap()
    else:
        world_map = Map()

    world_map.add_node(0, 845, 234)
    world_map.add_node(1, 495, 234)
    world_map.add_node(2, 143, 234)
    world_map.add_node(3, 817, 331)
    world_map.add_node(4, 817, 160)
    world_map.add_node(5, 187, 331)
    world_map.add_node(6, 154, 160)

    # world_map.add_node(i, 300, 97)
    # world_map.add_node(i, 300, 384)
    # world_map.add_node(i, 690, 376)
    # world_map.add_node(i, 690, 90)

    world_map.add_node(7, 330, 104)
    world_map.add_node(8, 330, 380)
    world_map.add_node(9, 660, 91)
    world_map.add_node(10, 660, 368)

    world_map.add_edge(0, 3)
    world_map.add_edge(0, 4)
    world_map.add_edge(2, 5)
    world_map.add_edge(2, 6)
    world_map.add_edge(7, 6)
    world_map.add_edge(8, 5)

        # world_map.add_edge(7, 8)
    world_map.add_edge(8, 1)
    world_map.add_edge(9, 4)
    world_map.add_edge(10, 3)
    world_map.add_edge(8, 9)

    world_map.add_edge(1, 10)
    world_map.add_edge(1, 9)    
    world_map.add_edge(1, 8)
    world_map.add_edge(1, 7)

    return world_map
