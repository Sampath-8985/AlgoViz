import unittest
from code_generator import CodeGenerator

class TestCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.algorithms = [
            "fibonacci", "counting_sort", "bucket_sort", "knapsack",
            "lcs", "edit_distance", "nqueens", "kruskal_mst",
            "prim_mst", "max_subarray", "mergesort", "bfs", "dfs",
            "bellman_ford", "floyd_warshall", "bst", "linked_list",
            "stack", "queue", "radix_sort", "astar"
        ]
        self.languages = ["python", "java", "cpp", "javascript"]

    def test_all_algorithms_all_languages(self):
        for algo in self.algorithms:
            for lang in self.languages:
                with self.subTest(algo=algo, lang=lang):
                    code = CodeGenerator.get_code(algo, language=lang)
                    self.assertIsNotNone(code)
                    self.assertIsInstance(code, str)
                    self.assertTrue(len(code) > 0, f"Code for {algo} in {lang} is empty")
                    # Check if it didn't fallback to bubble_sort (unless it's actually bubble_sort)
                    if algo != "bubble_sort":
                        # This is a bit weak but better than nothing
                        bubble_code = CodeGenerator.get_code("bubble_sort", language=lang)
                        self.assertNotEqual(code, bubble_code, f"Code for {algo} in {lang} appears to be a fallback to bubble_sort")
                    print(f"Verified {algo} in {lang}")

if __name__ == '__main__':
    unittest.main()
