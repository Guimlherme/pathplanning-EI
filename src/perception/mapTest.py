import unittest   
from .map import Map

class TestMap(unittest.TestCase):
    def map_factory(self):
        world_map = Map()
        world_map.add_node(0, 0, 0)
        world_map.add_node(1, 1, 0)
        world_map.add_edge(0, 1)
        return world_map

    def test_builds_map(self):
        world_map = self.map_factory()
        self.assertDictEqual(world_map.nodes, {0: (0, 0), 1: (1, 0)})
        self.assertDictEqual(world_map.adjacency_list,
        {
            0: [1],
            1: [0]
        })

    def test_get_closest(self):
        world_map = self.map_factory()
        closest_node = world_map.get_closest_neighbor(0, 0.1, 0.2)
        self.assertEqual(closest_node, 0)
        closest_node = world_map.get_closest_neighbor(0, 0.8, 0.2)
        self.assertEqual(closest_node, 1)

