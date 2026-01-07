import unittest
from template_generator import (
    generate_mergesort_template, generate_dfs_bfs_template,
    generate_bellman_ford_template, generate_floyd_warshall_template,
    generate_bst_template, generate_linked_list_template,
    generate_stack_template, generate_queue_template,
    generate_radix_sort_template, generate_astar_template
)

class TestPhase2Generation(unittest.TestCase):
    def test_mergesort(self):
        scene = generate_mergesort_template(1)
        self.assertIn("mergesort", scene["sceneId"])
        self.assertTrue(len(scene["actions"]) > 0)

    def test_dfs_bfs(self):
        for algo in ["dfs", "bfs"]:
            scene = generate_dfs_bfs_template(1, algo_type=algo)
            self.assertIn(algo, scene["sceneId"])
            self.assertTrue(len(scene["actions"]) > 0)

    def test_bellman_ford(self):
        scene = generate_bellman_ford_template(1)
        self.assertIn("bellman_ford", scene["sceneId"])
        self.assertTrue(len(scene["actions"]) > 0)

    def test_floyd_warshall(self):
        scene = generate_floyd_warshall_template(1)
        self.assertIn("floyd_warshall", scene["sceneId"])
        self.assertTrue(len(scene["actions"]) > 0)

    def test_bst(self):
        scene = generate_bst_template(1)
        self.assertIn("bst", scene["sceneId"])
        self.assertTrue(len(scene["actions"]) > 0)

    def test_structures(self):
        for func in [generate_linked_list_template, generate_stack_template, generate_queue_template]:
            scene = func(1)
            self.assertTrue(len(scene["actions"]) > 0)

    def test_radix_sort(self):
        scene = generate_radix_sort_template(1)
        self.assertIn("radix_sort", scene["sceneId"])
        self.assertTrue(len(scene["actions"]) > 0)

    def test_astar(self):
        scene = generate_astar_template(1)
        self.assertIn("astar", scene["sceneId"])
        self.assertTrue(len(scene["actions"]) > 0)

if __name__ == '__main__':
    unittest.main()
