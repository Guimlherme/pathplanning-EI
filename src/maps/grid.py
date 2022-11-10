from perception import Map

# Last row:
# (i, j)
# (0,0) (1, 0) (2, 0) (3, 0)
# 0 1 2 3

def get_grid_map(n=5):
    world_map = Map()
    for i in range(0, n):
        for j in range(0, n):
            index = j*(n) + i
            world_map.add_node(index, i*100, j*100)
            if i < n-1:
                world_map.add_edge(index, index + 1)
            if j < n-1:
                world_map.add_edge(index, index + n)
    return world_map