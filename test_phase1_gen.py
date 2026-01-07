
import unittest
import template_generator
import json

class TestPhase1Generation(unittest.TestCase):
    def test_fibonacci(self):
        data = template_generator.generate_fibonacci_template(1)
        self.assertIn("sceneId", data)
        self.assertEqual(data["sceneId"], "fibonacci_1")
        self.assertIn("objects", data)
        self.assertIn("actions", data)
        self.assertIn("code", data)
        print("Fibonacci: OK")

    def test_counting_sort(self):
        data = template_generator.generate_counting_sort_template(1)
        self.assertIn("sceneId", data)
        self.assertEqual(data["sceneId"], "counting_sort_1")
        print("Counting Sort: OK")

    def test_bucket_sort(self):
        data = template_generator.generate_bucket_sort_template(1)
        self.assertEqual(data["sceneId"], "bucket_sort_1")
        print("Bucket Sort: OK")

    def test_knapsack(self):
        data = template_generator.generate_knapsack_template(1)
        self.assertEqual(data["sceneId"], "knapsack_1")
        print("Knapsack: OK")

    def test_lcs(self):
        data = template_generator.generate_lcs_template(1)
        self.assertEqual(data["sceneId"], "lcs_1")
        print("LCS: OK")

    def test_edit_distance(self):
        data = template_generator.generate_edit_distance_template(1)
        self.assertEqual(data["sceneId"], "edit_distance_1")
        print("Edit Distance: OK")

    def test_nqueens(self):
        data = template_generator.generate_nqueens_template(1, n=4)
        self.assertEqual(data["sceneId"], "nqueens_1")
        print("N-Queens: OK")

    def test_kruskal(self):
        data = template_generator.generate_kruskal_mst_template(1)
        self.assertEqual(data["sceneId"], "kruskal_mst_1")
        print("Kruskal: OK")

    def test_prim(self):
        data = template_generator.generate_prim_mst_template(1)
        self.assertEqual(data["sceneId"], "prim_mst_1")
        print("Prim: OK")

    def test_max_subarray(self):
        data = template_generator.generate_max_subarray_template(1)
        self.assertEqual(data["sceneId"], "max_subarray_1")
        print("Max Subarray: OK")

if __name__ == '__main__':
    unittest.main()
