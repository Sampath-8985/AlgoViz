import re

class CodeGenerator:
    """Generates code snippets for algorithms/topics in multiple languages and skill levels."""
    
    @staticmethod
    def get_code(topic, language="python", level="beginner"):
        topic = topic.lower()
        language = language.lower()
        level = level.lower()
        
        # Mapping of topics to their language-specific implementations
        implementations = {
            "bubble_sort": {
                "python": {
                    "beginner": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]",
                    "intermediate": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n                swapped = True\n        if not swapped: break",
                    "advanced": "def bubble_sort(arr: list[int]) -> None:\n    \"\"\"Bubble sort with O(n) best-case complexity.\"\"\"\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break"
                },
                "java": {
                    "beginner": "void bubbleSort(int[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n-i-1; j++) {\n            if (arr[j] > arr[j+1]) {\n                int temp = arr[j];\n                arr[j] = arr[j+1];\n                arr[j+1] = temp;\n            }\n        }\n    }\n}",
                    "intermediate": "void bubbleSort(int[] arr) {\n    int n = arr.length;\n    boolean swapped;\n    for (int i = 0; i < n; i++) {\n        swapped = false;\n        for (int j = 0; j < n-i-1; j++) {\n            if (arr[j] > arr[j+1]) {\n                int temp = arr[j];\n                arr[j] = arr[j+1];\n                arr[j+1] = temp;\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n}",
                    "advanced": "public static <T extends Comparable<T>> void bubbleSort(T[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n; i++) {\n        boolean swapped = false;\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j].compareTo(arr[j+1]) > 0) {\n                T temp = arr[j];\n                arr[j] = arr[j+1];\n                arr[j+1] = temp;\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n}"
                },
                "cpp": {
                    "beginner": "void bubbleSort(int arr[], int n) {\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n-i-1; j++) {\n            if (arr[j] > arr[j+1])\n                swap(arr[j], arr[j+1]);\n        }\n    }\n}",
                    "intermediate": "void bubbleSort(vector<int>& arr) {\n    int n = arr.size();\n    for (int i = 0; i < n; i++) {\n        bool swapped = false;\n        for (int j = 0; j < n-i-1; j++) {\n            if (arr[j] > arr[j+1]) {\n                swap(arr[j], arr[j+1]);\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n}",
                    "advanced": "template <typename T>\nvoid bubbleSort(std::vector<T>& arr) {\n    size_t n = arr.size();\n    for (size_t i = 0; i < n; ++i) {\n        bool swapped = false;\n        for (size_t j = 0; j < n - i - 1; ++j) {\n            if (arr[j] > arr[j+1]) {\n                std::swap(arr[j], arr[j+1]);\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n}"
                },
                "javascript": {
                    "beginner": "function bubbleSort(arr) {\n    let n = arr.length;\n    for (let i = 0; i < n; i++) {\n        for (let j = 0; j < n-i-1; j++) {\n            if (arr[j] > arr[j+1]) {\n                [arr[j], arr[j+1]] = [arr[j+1], arr[j]];\n            }\n        }\n    }\n}",
                    "intermediate": "function bubbleSort(arr) {\n    let n = arr.length;\n    for (let i = 0; i < n; i++) {\n        let swapped = false;\n        for (let j = 0; j < n-i-1; j++) {\n            if (arr[j] > arr[j+1]) {\n                [arr[j], arr[j+1]] = [arr[j+1], arr[j]];\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n}",
                    "advanced": "export const bubbleSort = (arr) => {\n    const n = arr.length;\n    for (let i = 0; i < n; i++) {\n        let swapped = false;\n        for (let j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];\n                swapped = true;\n            }\n        }\n        if (!swapped) break;\n    }\n    return arr;\n};"
                }
            },
            "selection_sort": {
                "python": {
                    "beginner": "def selection_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i+1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]",
                    "intermediate": "def selection_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i+1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        if min_idx != i:\n            arr[i], arr[min_idx] = arr[min_idx], arr[i]",
                    "advanced": "def selection_sort(arr: list[int]) -> None:\n    \"\"\"Selection sort implementation.\"\"\"\n    n = len(arr)\n    for i in range(n):\n        m = i\n        for j in range(i + 1, n):\n            if arr[j] < arr[m]: m = j\n        if m != i: arr[i], arr[m] = arr[m], arr[i]"
                },
                "java": {
                    "beginner": "void selectionSort(int[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n-1; i++) {\n        int min_idx = i;\n        for (int j = i+1; j < n; j++) {\n            if (arr[j] < arr[min_idx]) min_idx = j;\n        }\n        int temp = arr[min_idx];\n        arr[min_idx] = arr[i];\n        arr[i] = temp;\n    }\n}",
                    "intermediate": "void selectionSort(int[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n - 1; i++) {\n        int minIdx = i;\n        for (int j = i + 1; j < n; j++) {\n            if (arr[j] < arr[minIdx]) minIdx = j;\n        }\n        if (minIdx != i) {\n            int temp = arr[minIdx];\n            arr[minIdx] = arr[i];\n            arr[i] = temp;\n        }\n    }\n}",
                    "advanced": "public static <T extends Comparable<T>> void selectionSort(T[] arr) {\n    int n = arr.length;\n    for (int i = 0; i < n - 1; i++) {\n        int min = i;\n        for (int j = i + 1; j < n; j++) {\n            if (arr[j].compareTo(arr[min]) < 0) min = j;\n        }\n        if (min != i) {\n            T temp = arr[min];\n            arr[min] = arr[i];\n            arr[i] = temp;\n        }\n    }\n}"
                },
                "cpp": {
                    "beginner": "void selectionSort(int arr[], int n) {\n    for (int i = 0; i < n-1; i++) {\n        int min_idx = i;\n        for (int j = i+1; j < n; j++) {\n            if (arr[j] < arr[min_idx]) min_idx = j;\n        }\n        swap(arr[min_idx], arr[i]);\n    }\n}",
                    "intermediate": "void selectionSort(vector<int>& arr) {\n    int n = arr.size();\n    for (int i = 0; i < n - 1; i++) {\n        int min_idx = i;\n        for (int j = i + 1; j < n; j++) {\n            if (arr[j] < arr[min_idx]) min_idx = j;\n        }\n        if (min_idx != i) swap(arr[i], arr[min_idx]);\n    }\n}",
                    "advanced": "template <typename T>\nvoid selectionSort(std::vector<T>& arr) {\n    for (auto it = arr.begin(); it != arr.end(); ++it) {\n        auto min_it = std::min_element(it, arr.end());\n        if (it != min_it) std::iter_swap(it, min_it);\n    }\n}"
                },
                "javascript": {
                    "beginner": "function selectionSort(arr) {\n    for (let i = 0; i < arr.length; i++) {\n        let min = i;\n        for (let j = i + 1; j < arr.length; j++) {\n            if (arr[j] < arr[min]) min = j;\n        }\n        [arr[i], arr[min]] = [arr[min], arr[i]];\n    }\n}",
                    "intermediate": "function selectionSort(arr) {\n    const n = arr.length;\n    for (let i = 0; i < n - 1; i++) {\n        let min = i;\n        for (let j = i + 1; j < n; j++) {\n            if (arr[j] < arr[min]) min = j;\n        }\n        if (min !== i) [arr[i], arr[min]] = [arr[min], arr[i]];\n    }\n}",
                    "advanced": "export const selectionSort = (arr) => {\n    for (let i = 0; i < arr.length - 1; i++) {\n        let minIdx = i;\n        for (let j = i + 1; j < arr.length; j++) {\n            if (arr[j] < arr[minIdx]) minIdx = j;\n        }\n        if (minIdx !== i) [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];\n    }\n    return arr;\n};"
                }
            },
            "binary_search": {
                "python": {
                    "beginner": "def binary_search(arr, target):\n    low, high = 0, len(arr)-1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
                    "intermediate": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = low + (high - low) // 2\n        if arr[mid] == target: return mid\n        if arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
                    "advanced": "import bisect\ndef binary_search(arr, target):\n    idx = bisect.bisect_left(arr, target)\n    if idx < len(arr) and arr[idx] == target:\n        return idx\n    return -1"
                },
                "java": {
                    "beginner": "int binarySearch(int[] arr, int target) {\n    int low = 0, high = arr.length - 1;\n    while (low <= high) {\n        int mid = (low + high) / 2;\n        if (arr[mid] == target) return mid;\n        else if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}",
                    "intermediate": "int binarySearch(int[] arr, int target) {\n    int low = 0, high = arr.length - 1;\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}",
                    "advanced": "public static int binarySearch(int[] arr, int target) {\n    return java.util.Arrays.binarySearch(arr, target);\n}"
                },
                "cpp": {
                    "beginner": "int binarySearch(int arr[], int n, int target) {\n    int low = 0, high = n - 1;\n    while (low <= high) {\n        int mid = (low + high) / 2;\n        if (arr[mid] == target) return mid;\n        else if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}",
                    "intermediate": "int binarySearch(const vector<int>& arr, int target) {\n    int low = 0, high = arr.size() - 1;\n    while (low <= high) {\n        int mid = low + (high - low) / 2;\n        if (arr[mid] == target) return mid;\n        if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}",
                    "advanced": "#include <algorithm>\nbool binarySearch(const std::vector<int>& arr, int target) {\n    return std::binary_search(arr.begin(), arr.end(), target);\n}"
                },
                "javascript": {
                    "beginner": "function binarySearch(arr, target) {\n    let low = 0, high = arr.length - 1;\n    while (low <= high) {\n        let mid = Math.floor((low + high) / 2);\n        if (arr[mid] === target) return mid;\n        else if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}",
                    "intermediate": "function binarySearch(arr, target) {\n    let low = 0, high = arr.length - 1;\n    while (low <= high) {\n        let mid = low + Math.floor((high - low) / 2);\n        if (arr[mid] === target) return mid;\n        if (arr[mid] < target) low = mid + 1;\n        else high = mid - 1;\n    }\n    return -1;\n}",
                    "advanced": "const binarySearch = (arr, target) => {\n    let idx = _.sortedIndex(arr, target);\n    return (idx < arr.length && arr[idx] === target) ? idx : -1;\n};"
                }
            },
            "quicksort": {
                "python": {
                    "beginner": "def quicksort(arr):\n    if len(arr) <= 1: return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
                    "intermediate": "def partition(arr, low, high):\n    pivot = arr[high]\n    i = low - 1\n    for j in range(low, high):\n        if arr[j] <= pivot:\n            i += 1\n            arr[i], arr[j] = arr[j], arr[i]\n    arr[i+1], arr[high] = arr[high], arr[i+1]\n    return i + 1",
                    "advanced": "import random\ndef quicksort(arr, low, high):\n    if low < high:\n        p = randomized_partition(arr, low, high)\n        quicksort(arr, low, p - 1)\n        quicksort(arr, p + 1, high)"
                },
                "javascript": {
                    "beginner": "function quicksort(arr) {\n    if (arr.length <= 1) return arr;\n    const pivot = arr[Math.floor(arr.length / 2)];\n    const left = arr.filter(x => x < pivot);\n    const mid = arr.filter(x => x === pivot);\n    const right = arr.filter(x => x > pivot);\n    return [...quicksort(left), ...mid, ...quicksort(right)];\n}",
                    "intermediate": "function partition(arr, low, high) {\n    let pivot = arr[high];\n    let i = low - 1;\n    for (let j = low; j < high; j++) {\n        if (arr[j] <= pivot) {\n            i++;\n            [arr[i], arr[j]] = [arr[j], arr[i]];\n        }\n    }\n    [arr[i+1], arr[high]] = [arr[high], arr[i+1]];\n    return i + 1;\n}",
                    "advanced": "const quickSort = (arr, left = 0, right = arr.length - 1) => {\n    if (left < right) {\n        let pivotIndex = partition(arr, left, right);\n        quickSort(arr, left, pivotIndex - 1);\n        quickSort(arr, pivotIndex + 1, right);\n    }\n    return arr;\n};"
                }
            },
            "dijkstra": {
                "python": {
                    "beginner": "def dijkstra(graph, start):\n    distances = {node: float('infinity') for node in graph}\n    distances[start] = 0\n    queue = [start]\n    while queue:\n        current = queue.pop(0)\n        for neighbor, weight in graph[current]:\n            if distances[current] + weight < distances[neighbor]:\n                distances[neighbor] = distances[current] + weight\n                queue.append(neighbor)\n    return distances",
                    "intermediate": "import heapq\ndef dijkstra(graph, start):\n    pq = [(0, start)]\n    distances = {n: float('inf') for n in graph}\n    distances[start] = 0\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > distances[u]: continue\n        for v, w in graph[u]:\n            if distances[u] + w < distances[v]:\n                distances[v] = distances[u] + w\n                heapq.heappush(pq, (distances[v], v))",
                    "advanced": "class PriorityQueue:\n    # Optimized Fib-Heap implementation placeholder\n    pass\ndef dijkstra(adj_list, source):\n    dist = [float('inf')] * len(adj_list)\n    dist[source] = 0\n    pq = PriorityQueue([(0, source)])\n    # ... Main Loop"
                }
            },
            "fibonacci": {
                "python": {
                    "beginner": "def fibonacci(n):\n    if n <= 1:\n        return n\n    fib = [0, 1]\n    for i in range(2, n+1):\n        fib.append(fib[i-1] + fib[i-2])\n    return fib",
                    "intermediate": "def fibonacci(n):\n    \"\"\"Generate Fibonacci sequence using DP.\"\"\"\n    if n <= 1:\n        return [0] if n == 0 else [0, 1]\n    dp = [0, 1]\n    for i in range(2, n+1):\n        dp.append(dp[-1] + dp[-2])\n    return dp",
                    "advanced": "def fibonacci(n):\n    \"\"\"Optimized Fibonacci with space O(1).\"\"\"\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n+1):\n        a, b = b, a + b\n    return b"
                },
                "java": {
                    "beginner": "int[] fibonacci(int n) {\n    int[] fib = new int[n+1];\n    fib[0] = 0;\n    fib[1] = 1;\n    for (int i = 2; i <= n; i++) {\n        fib[i] = fib[i-1] + fib[i-2];\n    }\n    return fib;\n}",
                    "intermediate": "List<Integer> fibonacci(int n) {\n    List<Integer> fib = new ArrayList<>();\n    fib.add(0);\n    fib.add(1);\n    for (int i = 2; i <= n; i++) {\n        fib.add(fib.get(i-1) + fib.get(i-2));\n    }\n    return fib;\n}",
                    "advanced": "long fibonacci(int n) {\n    if (n <= 1) return n;\n    long a = 0, b = 1;\n    for (int i = 2; i <= n; i++) {\n        long temp = a + b;\n        a = b;\n        b = temp;\n    }\n    return b;\n}"
                },
                "javascript": {
                    "beginner": "function fibonacci(n) {\n    const fib = [0, 1];\n    for (let i = 2; i <= n; i++) {\n        fib[i] = fib[i-1] + fib[i-2];\n    }\n    return fib;\n}",
                    "intermediate": "function fibonacci(n) {\n    if (n <= 1) return [0, 1].slice(0, n+1);\n    const fib = [0, 1];\n    for (let i = 2; i <= n; i++) {\n        fib.push(fib[i-1] + fib[i-2]);\n    }\n    return fib;\n}",
                    "advanced": "const fibonacci = (n) => {\n    if (n <= 1) return n;\n    let [a, b] = [0, 1];\n    for (let i = 2; i <= n; i++) {\n        [a, b] = [b, a + b];\n    }\n    return b;\n};"
                }
            },
            "counting_sort": {
                "python": {
                    "beginner": "def counting_sort(arr):\n    max_val = max(arr)\n    count = [0] * (max_val + 1)\n    for num in arr:\n        count[num] += 1\n    result = []\n    for i, c in enumerate(count):\n        result.extend([i] * c)\n    return result",
                    "intermediate": "def counting_sort(arr):\n    if not arr:\n        return arr\n    max_val, min_val = max(arr), min(arr)\n    range_size = max_val - min_val + 1\n    count = [0] * range_size\n    for num in arr:\n        count[num - min_val] += 1\n    result = []\n    for i, c in enumerate(count):\n        result.extend([i + min_val] * c)\n    return result",
                    "advanced": "def counting_sort(arr, exp=1):\n    \"\"\"Counting sort for radix sort.\"\"\"\n    n = len(arr)\n    output = [0] * n\n    count = [0] * 10\n    for i in range(n):\n        index = arr[i] // exp\n        count[index % 10] += 1\n    for i in range(1, 10):\n        count[i] += count[i - 1]\n    i = n - 1\n    while i >= 0:\n        index = arr[i] // exp\n        output[count[index % 10] - 1] = arr[i]\n        count[index % 10] -= 1\n        i -= 1\n    return output"
                },
                "java": {
                    "beginner": "int[] countingSort(int[] arr) {\n    int max = Arrays.stream(arr).max().getAsInt();\n    int[] count = new int[max + 1];\n    for (int num : arr) {\n        count[num]++;\n    }\n    int idx = 0;\n    for (int i = 0; i <= max; i++) {\n        while (count[i]-- > 0) {\n            arr[idx++] = i;\n        }\n    }\n    return arr;\n}",
                    "intermediate": "int[] countingSort(int[] arr) {\n    if (arr.length == 0) return arr;\n    int max = Arrays.stream(arr).max().getAsInt();\n    int min = Arrays.stream(arr).min().getAsInt();\n    int range = max - min + 1;\n    int[] count = new int[range];\n    int[] output = new int[arr.length];\n    for (int num : arr) {\n        count[num - min]++;\n    }\n    int idx = 0;\n    for (int i = 0; i < range; i++) {\n        while (count[i]-- > 0) {\n            output[idx++] = i + min;\n        }\n    }\n    return output;\n}",
                    "advanced": "void countingSort(int[] arr, int exp) {\n    int n = arr.length;\n    int[] output = new int[n];\n    int[] count = new int[10];\n    for (int i = 0; i < n; i++) {\n        count[(arr[i] / exp) % 10]++;\n    }\n    for (int i = 1; i < 10; i++) {\n        count[i] += count[i - 1];\n    }\n    for (int i = n - 1; i >= 0; i--) {\n        output[count[(arr[i] / exp) % 10] - 1] = arr[i];\n        count[(arr[i] / exp) % 10]--;\n    }\n    System.arraycopy(output, 0, arr, 0, n);\n}"
                }
            },
            "bucket_sort": {
                "python": {
                    "beginner": "def bucket_sort(arr):\n    \"\"\"Distribute elements into buckets, sort buckets, and concatenate.\"\"\"\n    bucket = []\n    for i in range(len(arr)):\n         bucket.append([])\n    for j in arr:\n         index_b = int(10 * j)\n         bucket[index_b].append(j)\n    for i in range(len(arr)):\n         bucket[i] = sorted(bucket[i])\n    k = 0\n    for i in range(len(arr)):\n         for j in range(len(bucket[i])):\n             arr[k] = bucket[i][j]\n             k += 1\n    return arr",
                    "intermediate": "def bucket_sort(arr):\n    if not arr: return arr\n    # Dynamic bucket count based on length\n    slot_num = 10 \n    buckets = [[] for _ in range(slot_num)]\n    for num in arr:\n        b_index = int(slot_num * num)\n        buckets[b_index].append(num)\n    for i in range(slot_num):\n        buckets[i] = sorted(buckets[i])\n    \n    k = 0\n    for i in range(slot_num):\n        for j in range(len(buckets[i])):\n            arr[k] = buckets[i][j]\n            k += 1\n    return arr",
                    "advanced": "import itertools\ndef bucket_sort(arr: list[float]) -> list[float]:\n    \"\"\"Bucket sort with insertion sort for buckets.\"\"\"\n    if not arr: return arr\n    slot_num = len(arr)\n    buckets = [[] for _ in range(slot_num)]\n    \n    for num in arr:\n        b_index = int(slot_num * num)\n        # Boundary check for 1.0\n        if b_index == slot_num: b_index -= 1 \n        buckets[b_index].append(num)\n        \n    # Sort individually using insertion sort (or default sort)\n    for b in buckets:\n        b.sort()\n        \n    return list(itertools.chain(*buckets))"
                },
                "java": {
                    "beginner": "public void bucketSort(float[] arr, int n) {\n    if (n <= 0) return;\n    ArrayList<Float>[] buckets = new ArrayList[n];\n    for (int i = 0; i < n; i++) buckets[i] = new ArrayList<Float>();\n    for (int i = 0; i < n; i++) {\n        int bucketIdx = (int) arr[i] * n;\n        buckets[bucketIdx].add(arr[i]);\n    }\n    for (int i = 0; i < n; i++) Collections.sort(buckets[i]);\n    int index = 0;\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < buckets[i].size(); j++) {\n            arr[index++] = buckets[i].get(j);\n        }\n    }\n}",
                    "intermediate": "void bucketSort(float[] arr, int n) {\n    if (n <= 0) return;\n    ArrayList<Float>[] buckets = new ArrayList[n];\n    for (int i = 0; i < n; i++) buckets[i] = new ArrayList<>();\n    for (float val : arr) {\n        int idx = (int) (val * n);\n        if (idx == n) idx--; // Handle 1.0\n        buckets[idx].add(val);\n    }\n    for (ArrayList<Float> bucket : buckets) Collections.sort(bucket);\n    int index = 0;\n    for (ArrayList<Float> bucket : buckets) {\n        for (float val : bucket) arr[index++] = val;\n    }\n}",
                    "advanced": "public static void bucketSort(float[] arr) {\n    // Parallel bucket sort or optimized stream usage\n    int n = arr.length;\n    List<Float>[] buckets = new List[n];\n    for (int i=0; i<n; i++) buckets[i] = new ArrayList<>();\n    for (float f : arr) buckets[(int)(f * n)].add(f);\n    Arrays.stream(buckets).parallel().forEach(Collections::sort);\n    // Flatten...\n}"
                },
                "cpp": {
                    "beginner": "void bucketSort(float arr[], int n) {\n    vector<float> b[n];\n    for (int i = 0; i < n; i++) {\n        int bi = n * arr[i];\n        b[bi].push_back(arr[i]);\n    }\n    for (int i = 0; i < n; i++) sort(b[i].begin(), b[i].end());\n    int index = 0;\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < b[i].size(); j++)\n            arr[index++] = b[i][j];\n}",
                    "intermediate": "void bucketSort(vector<float>& arr) {\n    int n = arr.size();\n    vector<vector<float>> b(n);\n    for (float x : arr) {\n        int bi = n * x;\n        if (bi == n) bi--; \n        b[bi].push_back(x);\n    }\n    for (auto& bucket : b) sort(bucket.begin(), bucket.end());\n    int index = 0;\n    for (const auto& bucket : b)\n        for (float x : bucket) arr[index++] = x;\n}",
                    "advanced": "void bucketSort(std::vector<float>& arr) {\n    // Optimized with move semantics\n    // ...\n}"
                },
                "javascript": {
                    "beginner": "function bucketSort(arr, n) {\n    if (n <= 0) return;\n    let buckets = Array.from({ length: n }, () => []);\n    for (let i = 0; i < n; i++) {\n        let idx = Math.floor(n * arr[i]);\n        buckets[idx].push(arr[i]);\n    }\n    for (let i = 0; i < n; i++) buckets[i].sort((a, b) => a - b);\n    return [].concat(...buckets);\n}",
                    "intermediate": "function bucketSort(arr) {\n    const n = arr.length;\n    const buckets = Array.from({length: n}, () => []);\n    arr.forEach(x => {\n        const i = Math.floor(n * x);\n        buckets[Math.min(i, n-1)].push(x);\n    });\n    return buckets.reduce((acc, b) => [...acc, ...b.sort((a,b)=>a-b)], []);\n}",
                    "advanced": "const bucketSort = (arr) => {\n    // Functional immutable style\n    // ...\n};"
                }
            },
            "knapsack": {
                "python": {
                    "beginner": "def knapsack(W, wt, val, n):\n    \"\"\"Recursive implementation with branching.\"\"\"\n    if n == 0 or W == 0:\n        return 0\n    if (wt[n-1] > W):\n        return knapsack(W, wt, val, n-1)\n    else:\n        return max(val[n-1] + knapsack(W-wt[n-1], wt, val, n-1), \n                   knapsack(W, wt, val, n-1))",
                    "intermediate": "def knapsack(W, wt, val, n):\n    \"\"\"Iterative DP implementation using a 2D table.\"\"\"\n    K = [[0 for x in range(W + 1)] for x in range(n + 1)]\n    for i in range(n + 1):\n        for w in range(W + 1):\n            if i == 0 or w == 0:\n                K[i][w] = 0\n            elif wt[i-1] <= w:\n                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])\n            else:\n                K[i][w] = K[i-1][w]\n    return K[n][W]",
                    "advanced": "def knapsack(W, wt, val, n):\n    \"\"\"Space optimized DP (1D array).\"\"\"\n    dp = [0 for _ in range(W + 1)]\n    for i in range(1, n + 1):\n        for w in range(W, 0, -1):\n            if wt[i-1] <= w:\n                dp[w] = max(dp[w], dp[w-wt[i-1]] + val[i-1])\n    return dp[W]"
                },
                "java": {
                    "beginner": "static int knapSack(int W, int wt[], int val[], int n) {\n    int[][] K = new int[n + 1][W + 1];\n    for (int i = 0; i <= n; i++) {\n        for (int w = 0; w <= W; w++) {\n            if (i == 0 || w == 0) K[i][w] = 0;\n            else if (wt[i - 1] <= w)\n                K[i][w] = Math.max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);\n            else K[i][w] = K[i - 1][w];\n        }\n    }\n    return K[n][W];\n}",
                    "intermediate": "static int knapSack(int W, int wt[], int val[], int n) {\n    int[] dp = new int[W + 1];\n    for (int i = 1; i < n + 1; i++) {\n        for (int w = W; w >= 0; w--) {\n            if (wt[i - 1] <= w)\n                dp[w] = Math.max(dp[w], dp[w - wt[i - 1]] + val[i - 1]);\n        }\n    }\n    return dp[W];\n}",
                    "advanced": "public int knapsack(int W, int[] wt, int[] val) {\n    // Advanced logic handling large W or fractional knapsack if applicable\n    return 0;\n}"
                },
                "cpp": {
                    "beginner": "int knapSack(int W, int wt[], int val[], int n) {\n    vector<vector<int>> K(n + 1, vector<int>(W + 1));\n    for (int i = 0; i <= n; i++) {\n        for (int w = 0; w <= W; w++) {\n            if (i == 0 || w == 0) K[i][w] = 0;\n            else if (wt[i - 1] <= w)\n                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);\n            else K[i][w] = K[i - 1][w];\n        }\n    }\n    return K[n][W];\n}",
                    "intermediate": "int knapSack(int W, const vector<int>& wt, const vector<int>& val) {\n    int n = wt.size();\n    vector<int> dp(W + 1, 0);\n    for (int i = 0; i < n; i++) {\n        for (int w = W; w >= wt[i]; w--) {\n            dp[w] = max(dp[w], val[i] + dp[w - wt[i]]);\n        }\n    }\n    return dp[W];\n}",
                    "advanced": "int knapSack(int W, vector<int>& wt, vector<int>& val) {\n    // Space optimized with bitsets or meet-in-the-middle for subset sum\n    return 0;\n}"
                },
                "javascript": {
                    "beginner": "function knapSack(W, wt, val, n) {\n    let i, w;\n    let K = Array.from({ length: n + 1 }, () => Array(W + 1).fill(0));\n    for (i = 0; i <= n; i++) {\n        for (w = 0; w <= W; w++) {\n            if (i == 0 || w == 0) K[i][w] = 0;\n            else if (wt[i-1] <= w)\n                K[i][w] = Math.max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w]);\n            else K[i][w] = K[i-1][w];\n        }\n    }\n    return K[n][W];\n}",
                    "intermediate": "function knapSack(W, wt, val, n) {\n    let dp = new Array(W + 1).fill(0);\n    for (let i = 0; i < n; i++) {\n        for (let w = W; w >= 0; w--) {\n            if (wt[i] <= w) dp[w] = Math.max(dp[w], dp[w - wt[i]] + val[i]);\n        }\n    }\n    return dp[W];\n}",
                    "advanced": "const knapSack = (W, wt, val) => {\n    // Functional JS style space-optimized\n};"
                }
            },
            "lcs": {
                "python": {
                    "beginner": "def lcs(X, Y, m, n):\n    \"\"\"Recursive Longest Common Subsequence.\"\"\"\n    if m == 0 or n == 0:\n       return 0\n    elif X[m-1] == Y[n-1]:\n       return 1 + lcs(X, Y, m-1, n-1)\n    else:\n       return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n))",
                    "intermediate": "def lcs(X, Y):\n    \"\"\"Iterative DP Longest Common Subsequence.\"\"\"\n    m, n = len(X), len(Y)\n    L = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(m+1):\n        for j in range(n+1):\n            if i == 0 or j == 0:\n                L[i][j] = 0\n            elif X[i-1] == Y[j-1]:\n                L[i][j] = L[i-1][j-1] + 1\n            else:\n                L[i][j] = max(L[i-1][j], L[i][j-1])\n    return L[m][n]",
                    "advanced": "def lcs(X, Y):\n    \"\"\"Space Optimized LCS (2 rows).\"\"\"\n    m, n = len(X), len(Y)\n    if m < n: X, Y, m, n = Y, X, n, m\n    L = [[0]*(n+1) for _ in range(2)]\n    bi = bool(0)\n    for i in range(m):\n        bi = bool(i & 1)\n        for j in range(n+1):\n            if j == 0: L[bi][j] = 0\n            elif X[i] == Y[j-1]: L[bi][j] = L[1-bi][j-1] + 1\n            else: L[bi][j] = max(L[1-bi][j], L[bi][j-1])\n    return L[bi][n]"
                },
                "java": {
                    "beginner": "int lcs(char[] X, char[] Y, int m, int n) {\n    int L[][] = new int[m + 1][n + 1];\n    for (int i = 0; i <= m; i++) {\n        for (int j = 0; j <= n; j++) {\n            if (i == 0 || j == 0) L[i][j] = 0;\n            else if (X[i - 1] == Y[j - 1]) L[i][j] = L[i - 1][j - 1] + 1;\n            else L[i][j] = Math.max(L[i - 1][j], L[i][j - 1]);\n        }\n    }\n    return L[m][n];\n}",
                    "intermediate": "int lcs(char[] X, char[] Y, int m, int n) {\n    // Standard DP solution\n    int dp[][] = new int[m + 1][n + 1];\n    // ...\n    return dp[m][n];\n}",
                    "advanced": "public int lcs(String s1, String s2) {\n    // Space optimized or Hirschberg's\n    return 0;\n}"
                },
                "cpp": {
                    "beginner": "int lcs(string X, string Y, int m, int n) {\n    int L[m + 1][n + 1];\n    for (int i = 0; i <= m; i++) {\n        for (int j = 0; j <= n; j++) {\n            if (i == 0 || j == 0) L[i][j] = 0;\n            else if (X[i - 1] == Y[j - 1]) L[i][j] = L[i - 1][j - 1] + 1;\n            else L[i][j] = max(L[i - 1][j], L[i][j - 1]);\n        }\n    }\n    return L[m][n];\n}",
                    "intermediate": "int lcs(const string& X, const string& Y) {\n    int m = X.length(), n = Y.length();\n    vector<vector<int>> L(m + 1, vector<int>(n + 1));\n    // ...\n    return L[m][n];\n}",
                    "advanced": "int lcs(string X, string Y) {\n    // Space optimized 2*N\n    return 0;\n}"
                },
                "javascript": {
                    "beginner": "function lcs(X, Y, m, n) {\n    let L = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));\n    for (let i = 0; i <= m; i++) {\n        for (let j = 0; j <= n; j++) {\n            if (i == 0 || j == 0) L[i][j] = 0;\n            else if (X[i - 1] == Y[j - 1]) L[i][j] = L[i - 1][j - 1] + 1;\n            else L[i][j] = Math.max(L[i - 1][j], L[i][j - 1]);\n        }\n    }\n    return L[m][n];\n}",
                    "intermediate": "function lcs(X, Y) {\n    // Text-book DP\n}",
                    "advanced": "const lcs = (s1, s2) => {\n   // Functional optimized\n};"
                }
            },
            "edit_distance": {
                "python": {
                    "beginner": "def editDistance(str1, str2, m, n):\n    \"\"\"Recursive Levenshtein Edit Distance.\"\"\"\n    if m == 0: return n\n    if n == 0: return m\n    if str1[m-1] == str2[n-1]:\n        return editDistance(str1, str2, m-1, n-1)\n    return 1 + min(editDistance(str1, str2, m, n-1), # Insert\n                   editDistance(str1, str2, m-1, n), # Remove\n                   editDistance(str1, str2, m-1, n-1) # Replace\n                   )",
                    "intermediate": "def editDistance(str1, str2):\n    \"\"\"Iterative Levenshtein with 2D DP Table.\"\"\"\n    m, n = len(str1), len(str2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(m+1): dp[i][0] = i\n    for j in range(n+1): dp[0][j] = j\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if str1[i-1] == str2[j-1]: dp[i][j] = dp[i-1][j-1]\n            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])\n    return dp[m][n]",
                    "advanced": "def edit_distance(s1, s2):\n    \"\"\"Space optimized edit distance (2 rows).\"\"\"\n    if len(s1) < len(s2): return edit_distance(s2, s1)\n    if len(s2) == 0: return len(s1)\n    previous_row = range(len(s2) + 1)\n    for i, c1 in enumerate(s1):\n        current_row = [i + 1]\n        for j, c2 in enumerate(s2):\n            insertions = previous_row[j + 1] + 1 \n            deletions = current_row[j] + 1       \n            substitutions = previous_row[j] + (c1 != c2)\n            current_row.append(min(insertions, deletions, substitutions))\n        previous_row = current_row\n    return previous_row[-1]"
                },
                "java": {
                    "beginner": "static int editDist(String str1, String str2, int m, int n) {\n    int dp[][] = new int[m + 1][n + 1];\n    for (int i = 0; i <= m; i++) {\n        for (int j = 0; j <= n; j++) {\n            if (i == 0) dp[i][j] = j;\n            else if (j == 0) dp[i][j] = i;\n            else if (str1.charAt(i - 1) == str2.charAt(j - 1)) dp[i][j] = dp[i - 1][j - 1];\n            else dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1]));\n        }\n    }\n    return dp[m][n];\n}",
                    "intermediate": "public int minDistance(String word1, String word2) {\n    int m = word1.length(), n = word2.length();\n    int[][] dp = new int[m + 1][n + 1];\n    // ...\n    return dp[m][n];\n}",
                    "advanced": "public int minDistance(String word1, String word2) {\n    // O(min(m,n)) space\n    return 0;\n}"
                },
                "cpp": {
                    "beginner": "int editDist(string str1, string str2, int m, int n) {\n    int dp[m + 1][n + 1];\n    for (int i = 0; i <= m; i++) {\n        for (int j = 0; j <= n; j++) {\n            if (i == 0) dp[i][j] = j;\n            else if (j == 0) dp[i][j] = i;\n            else if (str1[i - 1] == str2[j - 1]) dp[i][j] = dp[i - 1][j - 1];\n            else dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});\n        }\n    }\n    return dp[m][n];\n}",
                    "intermediate": "int editDist(const string& s1, const string& s2) {\n    // Standard DP\n    return 0;\n}",
                    "advanced": "int editDist(const string& s1, const string& s2) {\n    // Space optimized\n    return 0;\n}"
                },
                "javascript": {
                    "beginner": "function editDist(str1, str2, m, n) {\n    let dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));\n    for (let i = 0; i <= m; i++) {\n        for (let j = 0; j <= n; j++) {\n            if (i === 0) dp[i][j] = j;\n            else if (j === 0) dp[i][j] = i;\n            else if (str1[i - 1] === str2[j - 1]) dp[i][j] = dp[i - 1][j - 1];\n            else dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);\n        }\n    }\n    return dp[m][n];\n}",
                    "intermediate": "function editDist(s1, s2) {\n    // Standard DP with O(mn) space\n}",
                    "advanced": "const editDist = (s1, s2) => {\n    // O(min(m,n)) space\n};"
                }
            },
            "nqueens": {
                "python": {
                    "beginner": "def solveNQ(board, col):\n    \"\"\"Backtracking to solve N-Queens.\"\"\"\n    if col >= N: return True\n    for i in range(N):\n        if isSafe(board, i, col):\n            board[i][col] = 1\n            if solveNQ(board, col + 1): return True\n            board[i][col] = 0\n    return False",
                    "intermediate": "def solveNQ(n):\n    cols, diag1, diag2 = set(), set(), set()\n    res = []\n    def backtrack(r):\n        if r == n:\n            res.append(True)\n            return\n        for c in range(n):\n            if c in cols or (r+c) in diag1 or (r-c) in diag2: continue\n            cols.add(c)\n            diag1.add(r+c)\n            diag2.add(r-c)\n            backtrack(r+1)\n            cols.remove(c)\n            diag1.remove(r+c)\n            diag2.remove(r-c)\n    backtrack(0)\n    return res",
                    "advanced": "def n_queens_opt(n):\n    # Bitmask optimization for N-Queens\n    def solve(row, ld, rd, solutions):\n        if row == (1 << n) - 1: return solutions + 1\n        avail = ~(row | ld | rd) & ((1 << n) - 1)\n        while avail:\n            p = avail & -avail\n            avail -= p\n            solutions = solve(row | p, (ld | p) << 1, (rd | p) >> 1, solutions)\n        return solutions\n    return solve(0, 0, 0, 0)"
                },
                "java": {
                    "beginner": "boolean solveNQUtil(int board[][], int col) {\n    if (col >= N) return true;\n    for (int i = 0; i < N; i++) {\n        if (isSafe(board, i, col)) {\n            board[i][col] = 1;\n            if (solveNQUtil(board, col + 1)) return true;\n            board[i][col] = 0; // BACKTRACK\n        }\n    }\n    return false;\n}",
                    "intermediate": "public void solveNQ(int n) {\n    // Optimized object-oriented backtracking with arrays\n    // ...\n}",
                    "advanced": "public class NQueens {\n    // Bit masking solution\n}"
                },
                "cpp": {
                    "beginner": "bool solveNQUtil(int board[N][N], int col) {\n    if (col >= N) return true;\n    for (int i = 0; i < N; i++) {\n        if (isSafe(board, i, col)) {\n            board[i][col] = 1;\n            if (solveNQUtil(board, col + 1)) return true;\n            board[i][col] = 0; // BACKTRACK\n        }\n    }\n    return false;\n}",
                    "intermediate": "void solveNQ(int n) {\n    // Std::vector optimized\n}",
                    "advanced": "int solve(int n) {\n    // Bitmask\n    return 0;\n}"
                },
                "javascript": {
                    "beginner": "function solveNQUtil(board, col) {\n    if (col >= N) return true;\n    for (let i = 0; i < N; i++) {\n        if (isSafe(board, i, col)) {\n            board[i][col] = 1;\n            if (solveNQUtil(board, col + 1)) return true;\n            board[i][col] = 0; // BACKTRACK\n        }\n    }\n    return false;\n}",
                    "intermediate": "function solveNQ(n) {\n    // Standard recursive backtracking\n}",
                    "advanced": "const solveNQ = (n) => {\n    // Bitwise ops\n};"
                }
            },
            "kruskal_mst": {
                "python": {
                    "beginner": "def kruskal(graph, V):\n    \"\"\"Kruskal's MST Algorithm using Disjoint Set.\"\"\"\n    result = []\n    i, e = 0, 0\n    graph = sorted(graph, key=lambda item: item[2])\n    parent, rank = [], []\n    for node in range(V):\n        parent.append(node)\n        rank.append(0)\n    while e < V - 1:\n        u, v, w = graph[i]\n        i += 1\n        x = find(parent, u)\n        y = find(parent, v)\n        if x != y:\n            e += 1\n            result.append([u, v, w])\n            union(parent, rank, x, y)\n    return result",
                    "intermediate": "class UnionFind:\n    def __init__(self, n):\n        self.parent = list(range(n))\n    def find(self, i):\n        if self.parent[i] == i: return i\n        self.parent[i] = self.find(self.parent[i])\n        return self.parent[i]\n    def union(self, i, j):\n        root_i = self.find(i)\n        root_j = self.find(j)\n        if root_i != root_j:\n            self.parent[root_i] = root_j\n            return True\n        return False\n\ndef kruskal(graph, V):\n    uf = UnionFind(V)\n    mst = []\n    graph.sort(key=lambda x: x[2])\n    for u, v, w in graph:\n        if uf.union(u, v):\n            mst.append((u,v,w))\n    return mst",
                    "advanced": "def kruskal_opt(graph, V):\n    # Optimized with Rank and Path Compression\n    pass"
                },
                "java": {
                    "beginner": "void KruskalMST() {\n    Edge result[] = new Edge[V];\n    for (int i = 0; i < V; ++i) result[i] = new Edge();\n    Arrays.sort(edge);\n    subset subsets[] = new subset[V];\n    for (int i = 0; i < V; ++i) subsets[i] = new subset(i, 0);\n    int i = 0, e = 0;\n    while (e < V - 1) {\n        Edge next_edge = edge[i++];\n        int x = find(subsets, next_edge.src);\n        int y = find(subsets, next_edge.dest);\n        if (x != y) {\n            result[e++] = next_edge;\n            Union(subsets, x, y);\n        }\n    }\n}",
                    "intermediate": "class UnionFind {\n    // Class implementation\n}\nvoid Kruskal() {\n    // Object oriented Kruskal\n}",
                    "advanced": "public List<Edge> kruskal(List<Edge> edges, int n) {\n    // Stream sorted edges\n    return null;\n}"
                },
                "cpp": {
                    "beginner": "void KruskalMST(Graph* graph) {\n    int V = graph->V;\n    Edge result[V];\n    int i = 0, e = 0;\n    sort(graph->edge, graph->edge + graph->E, [](Edge a, Edge b) { return a.weight < b.weight; });\n    subset* subsets = new subset[(V * sizeof(subset))];\n    for (int v = 0; v < V; ++v) { subsets[v].parent = v; subsets[v].rank = 0; }\n    while (e < V - 1 && i < graph->E) {\n        Edge next_edge = graph->edge[i++];\n        int x = find(subsets, next_edge.src);\n        int y = find(subsets, next_edge.dest);\n        if (x != y) { result[e++] = next_edge; Union(subsets, x, y); }\n    }\n}",
                    "intermediate": "struct DSU {\n    // Struct based DSU\n};\nvoid Kruskal() {\n    // C++ STL sort\n}",
                    "advanced": "auto kruskal(int n, vector<Edge>& edges) {\n    // Modern C++17 structured bindings\n    return vector<Edge>{};\n}"
                },
                "javascript": {
                    "beginner": "function KruskalMST(edges, V) {\n    let result = [];\n    edges.sort((a, b) => a.weight - b.weight);\n    let subsets = Array.from({ length: V }, (_, i) => ({ parent: i, rank: 0 }));\n    let i = 0, e = 0;\n    while (e < V - 1) {\n        let next_edge = edges[i++];\n        let x = find(subsets, next_edge.src);\n        let y = find(subsets, next_edge.dest);\n        if (x !== y) {\n            result.push(next_edge);\n            union(subsets, x, y);\n            e++;\n        }\n    }\n    return result;\n}",
                    "intermediate": "class UnionFind {\n    // Class based\n}\nfunction kruskal(edges, n) {\n    // ...\n}",
                    "advanced": "const kruskal = (edges, n) => {\n    // Functional\n};"
                }
            },
            "prim_mst": {
                "python": {
                    "beginner": "def prim(graph, V):\n    \"\"\"Prim's MST Algorithm using Adjacency Matrix.\"\"\"\n    key = [float('inf')] * V\n    parent = [None] * V\n    key[0] = 0\n    mstSet = [False] * V\n    parent[0] = -1\n    for cout in range(V):\n        u = minKey(key, mstSet)\n        mstSet[u] = True\n        for v in range(V):\n             if graph[u][v] > 0 and mstSet[v] == False and key[v] > graph[u][v]:\n                 key[v] = graph[u][v]\n                 parent[v] = u",
                    "intermediate": "import heapq\ndef prim(graph, start):\n    mst = []\n    visited = set()\n    edges = [(0, start, -1)]\n    while edges:\n        w, u, p = heapq.heappop(edges)\n        if u not in visited:\n            visited.add(u)\n            if p != -1: mst.append((p, u, w))\n            for v, weight in graph[u]:\n                if v not in visited:\n                    heapq.heappush(edges, (weight, v, u))\n    return mst",
                    "advanced": "def prim_fib_heap(graph, V):\n    # Fibonacci Heap optimization\n    pass"
                },
                "java": {
                    "beginner": "void primMST(int graph[][]) {\n    int parent[] = new int[V];\n    int key[] = new int[V];\n    Boolean mstSet[] = new Boolean[V];\n    for (int i = 0; i < V; i++) {\n        key[i] = Integer.MAX_VALUE;\n        mstSet[i] = false;\n    }\n    key[0] = 0; parent[0] = -1;\n    for (int count = 0; count < V - 1; count++) {\n        int u = minKey(key, mstSet);\n        mstSet[u] = true;\n        for (int v = 0; v < V; v++)\n            if (graph[u][v] != 0 && mstSet[v] == false && graph[u][v] < key[v]) {\n                parent[v] = u; key[v] = graph[u][v];\n            }\n    }\n}",
                    "intermediate": "public void primMST(List<List<Node>> adj) {\n    // PriorityQueue implementation\n}",
                    "advanced": "public void prim(int n, List<Edge> edges) {\n    // Optimized dense graph approach\n}"
                },
                "cpp": {
                    "beginner": "void primMST(int graph[V][V]) {\n    int parent[V], key[V];\n    bool mstSet[V];\n    for (int i = 0; i < V; i++) { key[i] = INT_MAX; mstSet[i] = false; }\n    key[0] = 0; parent[0] = -1;\n    for (int count = 0; count < V - 1; count++) {\n        int u = minKey(key, mstSet);\n        mstSet[u] = true;\n        for (int v = 0; v < V; v++)\n            if (graph[u][v] && mstSet[v] == false && graph[u][v] < key[v])\n                parent[v] = u, key[v] = graph[u][v];\n    }\n}",
                    "intermediate": "void prim(int src) {\n    priority_queue<ipair, vector<ipair>, greater<ipair>> pq;\n    // ...\n}",
                    "advanced": "auto prim(int n, const auto& adj) {\n    // auto-deduced types C++20\n    return 0;\n}"
                },
                "javascript": {
                    "beginner": "function primMST(graph) {\n    let parent = [], key = [], mstSet = [];\n    for (let i = 0; i < V; i++) { key[i] = Infinity; mstSet[i] = false; }\n    key[0] = 0; parent[0] = -1;\n    for (let count = 0; count < V - 1; count++) {\n        let u = minKey(key, mstSet);\n        mstSet[u] = true;\n        for (let v = 0; v < V; v++)\n            if (graph[u][v] && mstSet[v] == false && graph[u][v] < key[v]) {\n                parent[v] = u; key[v] = graph[u][v];\n            }\n    }\n}",
                    "intermediate": "function prim(graph) {\n    // Min-Priority Queue implementation\n}",
                    "advanced": "const prim = (adj) => {\n   // Functional optimized\n};"
                }
            },
            "max_subarray": {
                "python": {
                    "beginner": "def maxSubArraySum(a, size):\n    \"\"\"Kadane's Algorithm for Maximum Subarray Sum.\"\"\"\n    max_so_far = -float('inf')\n    max_ending_here = 0\n    for i in range(0, size):\n        max_ending_here = max_ending_here + a[i]\n        if (max_so_far < max_ending_here):\n            max_so_far = max_ending_here\n        if max_ending_here < 0:\n            max_ending_here = 0\n    return max_so_far",
                    "intermediate": "def maxSubArray(nums):\n    \"\"\"Kadane's Algorithm optimized version.\"\"\"\n    current_subarray = max_subarray = nums[0]\n    for num in nums[1:]:\n        current_subarray = max(num, current_subarray + num)\n        max_subarray = max(max_subarray, current_subarray)\n    return max_subarray",
                    "advanced": "def max_sub_array_dc(nums):\n    \"\"\"Divide and Conquer O(n log n).\"\"\"\n    # Implementation details for Divide and Conquer\n    pass"
                },
                "java": {
                    "beginner": "static int maxSubArraySum(int a[]) {\n    int max_so_far = Integer.MIN_VALUE, max_ending_here = 0;\n    for (int i = 0; i < a.length; i++) {\n        max_ending_here += a[i];\n        if (max_so_far < max_ending_here) max_so_far = max_ending_here;\n        if (max_ending_here < 0) max_ending_here = 0;\n    }\n    return max_so_far;\n}",
                    "intermediate": "int maxSubArray(int[] nums) {\n   int maxSoFar = nums[0], maxEndingHere = nums[0];\n   for (int i = 1; i < nums.length; i++) {\n        maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);\n        maxSoFar = Math.max(maxSoFar, maxEndingHere);\n   }\n   return maxSoFar;\n}",
                    "advanced": "public int maxSubArray(int[] nums) {\n    // Divide and Conquer approach\n    return 0;\n}"
                },
                "cpp": {
                    "beginner": "int maxSubArraySum(int a[], int size) {\n    int max_so_far = INT_MIN, max_ending_here = 0;\n    for (int i = 0; i < size; i++) {\n        max_ending_here += a[i];\n        if (max_so_far < max_ending_here) max_so_far = max_ending_here;\n        if (max_ending_here < 0) max_ending_here = 0;\n    }\n    return max_so_far;\n}",
                    "intermediate": "int maxSubArray(vector<int>& nums) {\n    int max_so_far = nums[0], curr = nums[0];\n    for(size_t i=1; i<nums.size(); ++i) {\n        curr = max(nums[i], curr + nums[i]);\n        max_so_far = max(max_so_far, curr);\n    }\n    return max_so_far;\n}",
                    "advanced": "int maxSubArray(const vector<int>& nums) {\n    // Parallel reduction or D&C\n    return 0;\n}"
                },
                "javascript": {
                    "beginner": "function maxSubArraySum(a, size) {\n    let max_so_far = -Infinity, max_ending_here = 0;\n    for (let i = 0; i < size; i++) {\n        max_ending_here += a[i];\n        if (max_so_far < max_ending_here) max_so_far = max_ending_here;\n        if (max_ending_here < 0) max_ending_here = 0;\n    }\n    return max_so_far;\n}",
                    "intermediate": "function maxSubArray(nums) {\n    let curr = nums[0], max_val = nums[0];\n    for (let i = 1; i < nums.length; i++) {\n        curr = Math.max(nums[i], curr + nums[i]);\n        max_val = Math.max(max_val, curr);\n    }\n    return max_val;\n}",
                    "advanced": "const maxSubArray = (nums) => {\n    // Functional reduce\n};"
                }
            },
            "mergesort": {
                "python": {
                    "beginner": "def mergeSort(arr):\n    if len(arr) > 1:\n        mid = len(arr)//2\n        L = arr[:mid]\n        R = arr[mid:]\n        mergeSort(L)\n        mergeSort(R)\n        i = j = k = 0\n        while i < len(L) and j < len(R):\n            if L[i] < R[j]:\n                arr[k] = L[i]; i += 1\n            else:\n                arr[k] = R[j]; j += 1\n            k += 1\n        while i < len(L):\n            arr[k] = L[i]; i += 1; k += 1\n        while j < len(R):\n            arr[k] = R[j]; j += 1; k += 1",
                    "intermediate": "def merge_sort(arr):\n    \"\"\"Standard Recursive Merge Sort.\"\"\"\n    if len(arr) <= 1: return arr\n    \n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    \n    return merge(left, right)\n\ndef merge(left, right):\n    sorted_arr = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] < right[j]:\n            sorted_arr.append(left[i])\n            i += 1\n        else:\n            sorted_arr.append(right[j])\n            j += 1\n    sorted_arr.extend(left[i:])\n    sorted_arr.extend(right[j:])\n    return sorted_arr",
                    "advanced": "def merge_sort(arr: list[int]) -> list[int]:\n    \"\"\"Optimized Merge Sort using slice assignment.\"\"\"\n    if len(arr) <= 1:\n        return arr\n    \n    mid = len(arr) // 2\n    L = arr[:mid]\n    R = arr[mid:]\n    \n    merge_sort(L)\n    merge_sort(R)\n    \n    i = j = k = 0\n    # Merge in-place\n    while i < len(L) and j < len(R):\n        if L[i] < R[j]:\n            arr[k] = L[i]\n            i += 1\n        else:\n            arr[k] = R[j]\n            j += 1\n        k += 1\n        \n    while i < len(L):\n        arr[k] = L[i]\n        i += 1\n        k += 1\n    \n    while j < len(R):\n        arr[k] = R[j]\n        j += 1\n        k += 1\n    return arr"
                },
                "java": {
                    "beginner": "void merge(int arr[], int l, int m, int r) {\n    int n1 = m - l + 1, n2 = r - m;\n    int L[] = new int[n1], R[] = new int[n2];\n    for (int i = 0; i < n1; ++i) L[i] = arr[l + i];\n    for (int j = 0; j < n2; ++j) R[j] = arr[m + 1 + j];\n    int i = 0, j = 0, k = l;\n    while (i < n1 && j < n2) {\n        if (L[i] <= R[j]) arr[k] = L[i++];\n        else arr[k] = R[j++];\n        k++;\n    }\n    while (i < n1) arr[k++] = L[i++];\n    while (j < n2) arr[k++] = R[j++];\n}\nvoid sort(int arr[], int l, int r) {\n    if (l < r) {\n        int m = l + (r - l) / 2;\n        sort(arr, l, m); sort(arr, m + 1, r);\n        merge(arr, l, m, r);\n    }\n}",
                    "intermediate": "public class MergeSort {\n    public void sort(int[] arr, int l, int r) {\n        if (l < r) {\n            int m = l + (r - l) / 2;\n            sort(arr, l, m);\n            sort(arr, m + 1, r);\n            merge(arr, l, m, r);\n        }\n    }\n    private void merge(int[] arr, int l, int m, int r) {\n        // Merge logic same as beginner but cleaner class structure\n        // ...\n    }\n}",
                    "advanced": "public class MergeSort {\n    // Optimized with System.arraycopy and reduced object creation\n    public static void sort(int[] arr) {\n        if (arr.length < 2) return;\n        int mid = arr.length / 2;\n        int[] left = new int[mid];\n        int[] right = new int[arr.length - mid];\n        System.arraycopy(arr, 0, left, 0, mid);\n        System.arraycopy(arr, mid, right, 0, arr.length - mid);\n        sort(left);\n        sort(right);\n        merge(arr, left, right);\n    }\n    private static void merge(int[] arr, int[] left, int[] right) {\n        // Merge implementation\n    }\n}"
                },
                "cpp": {
                    "beginner": "void merge(int arr[], int l, int m, int r) {\n    int n1 = m - l + 1, n2 = r - m;\n    int L[n1], R[n2];\n    for (int i = 0; i < n1; i++) L[i] = arr[l + i];\n    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];\n    int i = 0, j = 0, k = l;\n    while (i < n1 && j < n2) {\n        if (L[i] <= R[j]) arr[k++] = L[i++];\n        else arr[k++] = R[j++];\n    }\n    while (i < n1) arr[k++] = L[i++];\n    while (j < n2) arr[k++] = R[j++];\n}\nvoid mergeSort(int arr[], int l, int r) {\n    if (l < r) {\n        int m = l + (r - l) / 2;\n        mergeSort(arr, l, m); mergeSort(arr, m + 1, r);\n        merge(arr, l, m, r);\n    }\n}",
                    "intermediate": "void merge(vector<int>& arr, int l, int m, int r) {\n    vector<int> left, right;\n    // Standard vector implementation\n}\nvoid mergeSort(vector<int>& arr, int l, int r) {\n    // ...\n}",
                    "advanced": "template<typename T>\nvoid mergeSort(std::vector<T>& arr) {\n    if (arr.size() > 1) {\n        auto mid = arr.begin() + arr.size() / 2;\n        std::vector<T> left(arr.begin(), mid);\n        std::vector<T> right(mid, arr.end());\n        mergeSort(left);\n        mergeSort(right);\n        std::merge(left.begin(), left.end(), right.begin(), right.end(), arr.begin());\n    }\n}"
                },
                "javascript": {
                    "beginner": "function merge(arr, l, m, r) {\n    var n1 = m - l + 1, n2 = r - m;\n    var L = new Array(n1), R = new Array(n2);\n    for (var i = 0; i < n1; i++) L[i] = arr[l + i];\n    for (var j = 0; j < n2; j++) R[j] = arr[m + 1 + j];\n    var i = 0, j = 0, k = l;\n    while (i < n1 && j < n2) {\n        if (L[i] <= R[j]) arr[k++] = L[i++];\n        else arr[k++] = R[j++];\n    }\n    while (i < n1) arr[k++] = L[i++];\n    while (j < n2) arr[k++] = R[j++];\n}\nfunction mergeSort(arr, l, r) {\n    if (l >= r) return;\n    var m = l + Math.floor((r - l) / 2);\n    mergeSort(arr, l, m); mergeSort(arr, m + 1, r);\n    merge(arr, l, m, r);\n}",
                    "intermediate": "function mergeSort(arr) {\n    if (arr.length <= 1) return arr;\n    const mid = Math.floor(arr.length / 2);\n    const left = mergeSort(arr.slice(0, mid));\n    const right = mergeSort(arr.slice(mid));\n    return merge(left, right);\n}\nfunction merge(left, right) {\n    let result = [], i = 0, j = 0;\n    while (i < left.length && j < right.length) {\n        if (left[i] < right[j]) result.push(left[i++]);\n        else result.push(right[j++]);\n    }\n    return result.concat(left.slice(i)).concat(right.slice(j));\n}",
                    "advanced": "const mergeSort = (arr) => {\n    if (arr.length <= 1) return arr;\n    const mid = Math.floor(arr.length / 2);\n    const left = mergeSort(arr.slice(0, mid));\n    const right = mergeSort(arr.slice(mid));\n    return merge(left, right);\n};\nconst merge = (left, right) => {\n    let sorted = [];\n    while (left.length && right.length) {\n        sorted.push(left[0] < right[0] ? left.shift() : right.shift());\n    }\n    return [...sorted, ...left, ...right];\n};"
                }
            },
            "bfs": {
                "python": {
                    "beginner": "def bfs(graph, start):\n    visited = set()\n    queue = [start]\n    visited.add(start)\n    while queue:\n        vertex = queue.pop(0)\n        print(vertex)\n        for neighbor in graph[vertex]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)",
                    "intermediate": "from collections import deque\ndef bfs(graph, start):\n    visited, queue = set(), deque([start])\n    visited.add(start)\n    while queue:\n        vertex = queue.popleft()\n        print(str(vertex) + \" \", end=\"\")\n        for neighbor in graph[vertex]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)",
                    "advanced": "def bfs_generator(graph, start):\n    \"\"\"Yields vertices in BFS order.\"\"\"\n    visited, queue = {start}, collections.deque([start])\n    while queue:\n        vertex = queue.popleft()\n        yield vertex\n        new_nodes = set(graph[vertex]) - visited\n        visited.update(new_nodes)\n        queue.extend(new_nodes)"
                },
                "java": {
                    "beginner": "void BFS(int s) {\n    boolean visited[] = new boolean[V];\n    LinkedList<Integer> queue = new LinkedList<Integer>();\n    visited[s] = true;\n    queue.add(s);\n    while (queue.size() != 0) {\n        s = queue.poll();\n        System.out.print(s + \" \");\n        Iterator<Integer> i = adj[s].listIterator();\n        while (i.hasNext()) {\n            int n = i.next();\n            if (!visited[n]) {\n                visited[n] = true;\n                queue.add(n);\n            }\n        }\n    }\n}",
                    "intermediate": "void BFS(int s) {\n    // Buffered output, optimized queue usage\n    boolean visited[] = new boolean[V];\n    Queue<Integer> queue = new ArrayDeque<>();\n    visited[s] = true;\n    queue.add(s);\n    while (!queue.isEmpty()) {\n        s = queue.poll();\n        // process(s)\n        for (int n : adj[s]) {\n             if (!visited[n]) { visited[n] = true; queue.add(n); }\n        }\n    }\n}",
                    "advanced": "public Stream<T> bfsStream(T start) {\n    // Stream-based BFS implementation placeholder\n    return Stream.of(start);\n}"
                },
                "cpp": {
                    "beginner": "void BFS(int s) {\n    vector<bool> visited(V, false);\n    list<int> queue;\n    visited[s] = true;\n    queue.push_back(s);\n    while(!queue.empty()) {\n        s = queue.front();\n        cout << s << \" \";\n        queue.pop_front();\n        for (auto adjEC : adj[s]) {\n            if (!visited[adjEC]) {\n                visited[adjEC] = true;\n                queue.push_back(adjEC);\n            }\n        }\n    }\n}",
                    "intermediate": "void BFS(int s) {\n    vector<bool> visited(V, false);\n    queue<int> q;\n    visited[s] = true;\n    q.push(s);\n    while(!q.empty()) {\n        int u = q.front();\n        q.pop();\n        for(auto &v : adj[u]) \n             if(!visited[v]) { visited[v] = true; q.push(v); }\n    }\n}",
                    "advanced": "template <typename Func>\nvoid BFS(int start, Func visitor) {\n    std::queue<int> q; \n    std::vector<bool> visited(V, false);\n    visited[start] = true;\n    q.push(start);\n    while(!q.empty()) {\n        int u = q.front(); q.pop();\n        visitor(u);\n        for(const auto& v : adj[u]) if(!visited[v]) {\n            visited[v] = true; q.push(v);\n        }\n    }\n}"
                },
                "javascript": {
                    "beginner": "function BFS(graph, start) {\n    let visited = new Set();\n    let queue = [start];\n    visited.add(start);\n    while (queue.length > 0) {\n        let vertex = queue.shift();\n        console.log(vertex);\n        graph[vertex].forEach(neighbor => {\n            if (!visited.has(neighbor)) {\n                visited.add(neighbor);\n                queue.push(neighbor);\n            }\n        });\n    }\n}",
                    "intermediate": "function BFS(graph, start) {\n    const visited = new Set([start]);\n    const queue = [start];\n    while (queue.length) {\n        const u = queue.shift();\n        for (const v of graph[u]) {\n            if (!visited.has(v)) {\n                visited.add(v);\n                queue.push(v);\n            }\n        }\n    }\n}",
                    "advanced": "function* bfsGenerator(graph, start) {\n    const visited = new Set([start]);\n    const queue = [start];\n    while (queue.length) {\n        const u = queue.shift();\n        yield u;\n        for (const v of graph[u]) {\n            if (!visited.has(v)) {\n                visited.add(v);\n                queue.push(v);\n            }\n        }\n    }\n}"
                }
            },
            "dfs": {
                "python": {
                    "beginner": "def dfs(graph, start, visited=None):\n    if visited is None: visited = set()\n    visited.add(start)\n    print(start)\n    for next_node in graph[start] - visited:\n        dfs(graph, next_node, visited)\n    return visited",
                    "intermediate": "def dfs_iterative(graph, start):\n    visited = set()\n    stack = [start]\n    while stack:\n        vertex = stack.pop()\n        if vertex not in visited:\n             print(vertex)\n             visited.add(vertex)\n             # Add neighbors to stack in reverse order to correct visit order\n             stack.extend(reversed(list(graph[vertex])))",
                    "advanced": "def dfs(graph, start, visited=None):\n    \"\"\"One-liner inspired recursive DFS.\"\"\"\n    visited = visited or set()\n    visited.add(start)\n    # Logic processing...\n    [dfs(graph, next_node, visited) for next_node in graph[start] if next_node not in visited]\n    return visited"
                },
                "java": {
                    "beginner": "void DFSUtil(int v, boolean visited[]) {\n    visited[v] = true;\n    System.out.print(v + \" \");\n    Iterator<Integer> i = adj[v].listIterator();\n    while (i.hasNext()) {\n        int n = i.next();\n        if (!visited[n]) DFSUtil(n, visited);\n    }\n}\nvoid DFS(int v) {\n    boolean visited[] = new boolean[V];\n    DFSUtil(v, visited);\n}",
                    "intermediate": "void DFS(int s) {\n    // Iterative using Stack\n    boolean visited[] = new boolean[V];\n    Stack<Integer> stack = new Stack<>();\n    stack.push(s);\n    while (!stack.empty()) {\n        s = stack.pop();\n        if (!visited[s]) {\n            System.out.print(s + \" \");\n            visited[s] = true;\n        }\n        for (int n : adj[s]) if (!visited[n]) stack.push(n);\n    }\n}",
                    "advanced": "public void dfs(int v) {\n    // ForkJoin or Parallel DFS placeholder\n    new RecursiveDFS(v).compute();\n}"
                },
                "cpp": {
                    "beginner": "void DFSUtil(int v, bool visited[]) {\n    visited[v] = true;\n    cout << v << \" \";\n    for (auto i = adj[v].begin(); i != adj[v].end(); ++i)\n        if (!visited[*i]) DFSUtil(*i, visited);\n}\nvoid DFS(int v) {\n    bool *visited = new bool[V];\n    for (int i = 0; i < V; i++) visited[i] = false;\n    DFSUtil(v, visited);\n}",
                    "intermediate": "void DFS(int s) {\n    vector<bool> visited(V, false);\n    stack<int> stack;\n    stack.push(s);\n    while(!stack.empty()) {\n        s = stack.top(); stack.pop();\n        if (!visited[s]) {\n            visited[s] = true;\n            for (auto it = adj[s].rbegin(); it != adj[s].rend(); ++it) \n                if (!visited[*it]) stack.push(*it);\n        }\n    }\n}",
                    "advanced": "template <typename Func>\nvoid DFS(int v, vector<bool>& visited, Func f) {\n    visited[v] = true;\n    f(v);\n    for(const auto& u : adj[v]) \n        if(!visited[u]) DFS(u, visited, f);\n}"
                },
                "javascript": {
                    "beginner": "function DFS(graph, start, visited = new Set()) {\n    console.log(start);\n    visited.add(start);\n    graph[start].forEach(neighbor => {\n        if (!visited.has(neighbor)) {\n            DFS(graph, neighbor, visited);\n        }\n    });\n}",
                    "intermediate": "function dfsIterative(graph, start) {\n    const stack = [start];\n    const visited = new Set();\n    while (stack.length) {\n        const u = stack.pop();\n        if (!visited.has(u)) {\n            visited.add(u);\n            graph[u].forEach(v => stack.push(v));\n        }\n    }\n}",
                    "advanced": "const dfs = (graph, start, visited = new Set()) => {\n    visited.add(start);\n    // advanced functional approach\n    graph[start].filter(n => !visited.has(n)).forEach(n => dfs(graph, n, visited));\n};"
                }
            },
            "bellman_ford": {
                "python": {
                    "beginner": "def bellmanFord(graph, V, E, src):\n    dist = [float('inf')] * V\n    dist[src] = 0\n    for i in range(V - 1):\n        for u, v, w in graph:\n            if dist[u] != float('inf') and dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n    for u, v, w in graph:\n        if dist[u] != float('inf') and dist[u] + w < dist[v]:\n            print(\"Negative cycle detected\")",
                    "intermediate": "def bellman_ford(graph, start):\n    distances = {node: float('infinity') for node in graph}\n    distances[start] = 0\n    for _ in range(len(graph) - 1):\n        for u in graph:\n            for v, w in graph[u].items():\n                if distances[u] + w < distances[v]:\n                    distances[v] = distances[u] + w\n    # Check negative cycles...\n    return distances",
                    "advanced": "def bellman_ford_spfa(graph, start):\n    # Shortest Path Faster Algorithm (SPFA) optimization\n    pass"
                },
                "java": {
                    "beginner": "void BellmanFord(Graph graph, int src) {\n    int V = graph.V, E = graph.E;\n    int dist[] = new int[V];\n    for (int i = 0; i < V; ++i) dist[i] = Integer.MAX_VALUE;\n    dist[src] = 0;\n    for (int i = 1; i < V; ++i) {\n        for (int j = 0; j < E; ++j) {\n            int u = graph.edge[j].src, v = graph.edge[j].dest, w = graph.edge[j].weight;\n            if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) dist[v] = dist[u] + w;\n        }\n    }\n}",
                    "intermediate": "void bellmanFord(int start) {\n    // Standard OO implementation\n}",
                    "advanced": "public boolean spfa(int start) {\n    // SPFA queue based optimization\n    return true;\n}"
                },
                "cpp": {
                    "beginner": "void BellmanFord(struct Graph* graph, int src) {\n    int V = graph->V, E = graph->E;\n    int dist[V];\n    for (int i = 0; i < V; i++) dist[i] = INT_MAX;\n    dist[src] = 0;\n    for (int i = 1; i <= V - 1; i++) {\n        for (int j = 0; j < E; j++) {\n            int u = graph->edge[j].src, v = graph->edge[j].dest, w = graph->edge[j].weight;\n            if (dist[u] != INT_MAX && dist[u] + w < dist[v]) dist[v] = dist[u] + w;\n        }\n    }\n}",
                    "intermediate": "bool bellmanFord(int src) {\n    vector<int> dist(V, INF);\n    // ...\n    return true;\n}",
                    "advanced": "bool spfa(int s) {\n    // Queue optimization\n    return true;\n}"
                },
                "javascript": {
                    "beginner": "function bellmanFord(edges, V, src) {\n    let dist = Array(V).fill(Infinity);\n    dist[src] = 0;\n    for (let i = 0; i < V - 1; i++) {\n        for (let [u, v, w] of edges) {\n            if (dist[u] !== Infinity && dist[u] + w < dist[v]) dist[v] = dist[u] + w;\n        }\n    }\n    return dist;\n}",
                    "intermediate": "function bellmanFord(graph, start) {\n    // Adjacency list based\n}",
                    "advanced": "const spfa = (start) => {\n    // SPFA\n};"
                }
            },
            "floyd_warshall": {
                "python": {
                    "beginner": "def floydWarshall(graph, V):\n    dist = list(map(lambda i: list(map(lambda j: j, i)), graph))\n    for k in range(V):\n        for i in range(V):\n            for j in range(V):\n                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])\n    return dist",
                    "intermediate": "def floyd_warshall(graph):\n    # Standard nested loop implementation\n    n = len(graph)\n    dist = [row[:] for row in graph]\n    for k in range(n):\n        for i in range(n):\n            for j in range(n):\n                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])\n    return dist",
                    "advanced": "import numpy as np\ndef floyd_warshall_numpy(graph):\n    # Numpy vectorized optimization\n    dist = np.array(graph)\n    n = len(dist)\n    for k in range(n):\n        dist = np.minimum(dist, dist[:, k, None] + dist[None, k, :])\n    return dist"
                },
                "java": {
                    "beginner": "void floydWarshall(int graph[][]) {\n    int dist[][] = new int[V][V];\n    for (int i = 0; i < V; i++) for (int j = 0; j < V; j++) dist[i][j] = graph[i][j];\n    for (int k = 0; k < V; k++) {\n        for (int i = 0; i < V; i++) {\n            for (int j = 0; j < V; j++) {\n                if (dist[i][k] + dist[k][j] < dist[i][j]) dist[i][j] = dist[i][k] + dist[k][j];\n            }\n        }\n    }\n}",
                    "intermediate": "public void floydWarshall(int[][] adj) {\n    // Standard implementation\n}",
                    "advanced": "public void floydWarshallBlocked(int[][] adj) {\n    // Cache friendly blocked algo\n}"
                },
                "cpp": {
                    "beginner": "void floydWarshall(int graph[V][V]) {\n    int dist[V][V];\n    for (int i = 0; i < V; i++) for (int j = 0; j < V; j++) dist[i][j] = graph[i][j];\n    for (int k = 0; k < V; k++)\n        for (int i = 0; i < V; i++)\n            for (int j = 0; j < V; j++)\n                if (dist[i][k] + dist[k][j] < dist[i][j]) dist[i][j] = dist[i][k] + dist[k][j];\n}",
                    "intermediate": "void floydWarshall(vector<vector<int>>& dist) {\n    // ...\n}",
                    "advanced": "void floydWarshall(vector<vector<int>>& dist) {\n    // SIMD or Blocked\n}"
                },
                "javascript": {
                    "beginner": "function floydWarshall(graph, V) {\n    let dist = Array.from(graph, row => [...row]);\n    for (let k = 0; k < V; k++) {\n        for (let i = 0; i < V; i++) {\n            for (let j = 0; j < V; j++) {\n                if (dist[i][k] + dist[k][j] < dist[i][j]) dist[i][j] = dist[i][k] + dist[k][j];\n            }\n        }\n    }\n    return dist;\n}",
                    "intermediate": "function floydWarshall(graph) {\n    // ...\n}",
                    "advanced": "const floydWarshall = (graph) => {\n    // ...\n};"
                }
            },
            "bst": {
                "python": {
                    "beginner": "class Node:\n    def __init__(self, key):\n        self.left = None\n        self.right = None\n        self.val = key\n\ndef insert(root, key):\n    if root is None: return Node(key)\n    if root.val < key: root.right = insert(root.right, key)\n    else: root.left = insert(root.left, key)\n    return root",
                    "intermediate": "class BST:\n    def __init__(self):\n        self.root = None\n    def insert(self, key):\n        if not self.root:\n            self.root = Node(key)\n        else:\n            self._insert(self.root, key)\n    def _insert(self, node, key):\n        if key < node.val:\n             if node.left: self._insert(node.left, key)\n             else: node.left = Node(key)\n        else:\n             if node.right: self._insert(node.right, key)\n             else: node.right = Node(key)",
                    "advanced": "class BST[T]:\n    # Type hinting and internal classes for pythonic BST\n    pass"
                },
                "java": {
                    "beginner": "class Node {\n    int key;\n    Node left, right;\n    public Node(int item) { key = item; left = right = null; }\n}\nNode insert(Node root, int key) {\n    if (root == null) { root = new Node(key); return root; }\n    if (key < root.key) root.left = insert(root.left, key);\n    else if (key > root.key) root.right = insert(root.right, key);\n    return root;\n}",
                    "intermediate": "class BST {\n    Node root;\n    void insert(int key) { root = insertRec(root, key); }\n    Node insertRec(Node root, int key) {\n        // Recursive implementation inside encapsulation\n        if (root == null) return new Node(key);\n        if (key < root.key) root.left = insertRec(root.left, key);\n        else if (key > root.key) root.right = insertRec(root.right, key);\n        return root;\n    }\n}",
                    "advanced": "public class BST<T extends Comparable<T>> {\n    // Generic implementation\n}"
                },
                "cpp": {
                    "beginner": "struct Node {\n    int key;\n    struct Node *left, *right;\n};\nstruct Node* insert(struct Node* node, int key) {\n    if (node == NULL) return newNode(key);\n    if (key < node->key) node->left = insert(node->left, key);\n    else if (key > node->key) node->right = insert(node->right, key);\n    return node;\n}",
                    "intermediate": "class BST {\n    Node* root;\n    // Class based insertion\n};",
                    "advanced": "template <typename T>\nclass BST {\n    // Template based balanced tree (AVL/RedBlack)\n};"
                },
                "javascript": {
                    "beginner": "class Node {\n    constructor(val) {\n        this.val = val;\n        this.left = null; this.right = null;\n    }\n}\nfunction insert(root, val) {\n    if (root === null) return new Node(val);\n    if (val < root.val) root.left = insert(root.left, val);\n    else root.right = insert(root.right, val);\n    return root;\n}",
                    "intermediate": "class BST {\n    constructor() { this.root = null; }\n    insert(val) {\n        if (!this.root) this.root = new Node(val);\n        else this.insertNode(this.root, val);\n    }\n}",
                    "advanced": "class BST {\n    // Advanced logic with auto-balancing rotation placeholders\n}"
                }
            },
            "linked_list": {
                "python": {
                    "beginner": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self): self.head = None",
                    "intermediate": "class LinkedList:\n    def __init__(self):\n        self.head = None\n    def append(self, data):\n        if not self.head: self.head = Node(data)\n        else:\n             cur = self.head\n             while cur.next: cur = cur.next\n             cur.next = Node(data)",
                    "advanced": "class LinkedList:\n    __slots__ = ['head', 'tail']\n    # Optimized with tail pointer"
                },
                "java": {
                    "beginner": "class LinkedList {\n    Node head;\n    class Node {\n        int data; Node next;\n        Node(int d) { data = d; next = null; }\n    }\n}",
                    "intermediate": "class LinkedList {\n    Node head;\n    public void add(int data) {\n        // Traversal logic\n    }\n}",
                    "advanced": "class LinkedList<T> implements Iterable<T> {\n    // Generic implementation\n}"
                },
                "cpp": {
                    "beginner": "struct Node {\n    int data; struct Node* next;\n};\nvoid push(struct Node** head_ref, int new_data) {\n    struct Node* new_node = (struct Node*) malloc(sizeof(struct Node));\n    new_node->data = new_data; new_node->next = (*head_ref);\n    (*head_ref) = new_node;\n}",
                    "intermediate": "class LinkedList {\n    Node* head;\npublic:\n    void push(int data) {\n        // ...\n    }\n};",
                    "advanced": "template <typename T>\nclass LinkedList {\n    // Smart pointers (unique_ptr)\n};"
                },
                "javascript": {
                    "beginner": "class Node {\n    constructor(data) {\n        this.data = data; this.next = null;\n    }\n}\nclass LinkedList {\n    constructor() { this.head = null; }\n}",
                    "intermediate": "class LinkedList {\n    // methods\n}",
                    "advanced": "class LinkedList {\n    // Doubly linked or circular\n}"
                }
            },
            "stack": {
                "python": {
                    "beginner": "stack = []\nstack.append('a')\nstack.append('b')\nprint(stack.pop())",
                    "intermediate": "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item): self.items.append(item)\n    def pop(self): return self.items.pop()",
                    "advanced": "from collections import deque\nstack = deque()"
                },
                "java": {
                    "beginner": "Stack<String> stack = new Stack<String>();\nstack.push(\"a\");\nstack.push(\"b\");\nSystem.out.println(stack.pop());",
                    "intermediate": "class MyStack {\n   // ArrayList based implementation\n}",
                    "advanced": "Deque<String> stack = new ArrayDeque<>();"
                },
                "cpp": {
                    "beginner": "stack<string> s;\ns.push(\"a\");\ns.push(\"b\");\ncout << s.top(); s.pop();",
                    "intermediate": "template <typename T>\nclass Stack {\n    // Vector based\n};",
                    "advanced": "std::stack<T, std::vector<T>> s; // Explicit underlying container"
                },
                "javascript": {
                    "beginner": "let stack = [];\nstack.push(\"a\");\nstack.push(\"b\");\nconsole.log(stack.pop());",
                    "intermediate": "class Stack {\n    constructor() { this.items = []; }\n    // methods\n}",
                    "advanced": "const stack = { ... } // Functional or Prototype"
                }
            },
            "queue": {
                "python": {
                    "beginner": "from collections import deque\nqueue = deque([\"a\", \"b\"])\nqueue.append(\"c\")\nprint(queue.popleft())",
                    "intermediate": "class Queue:\n    def __init__(self):\n        self.items = []\n    def enqueue(self, item): self.items.append(item)\n    def dequeue(self): return self.items.pop(0)",
                    "advanced": "import multiprocessing\nqueue = multiprocessing.Queue()"
                },
                "java": {
                    "beginner": "Queue<String> q = new LinkedList<>();\nq.add(\"a\");\nq.add(\"b\");\nSystem.out.println(q.remove());",
                    "intermediate": "class Queue {\n    // Array-based circular queue\n}",
                    "advanced": "BlockingQueue<String> q = new LinkedBlockingQueue<>();"
                },
                "cpp": {
                    "beginner": "queue<string> q;\nq.push(\"a\");\nq.push(\"b\");\ncout << q.front(); q.pop();",
                    "intermediate": "class Queue {\n    // Linked List based\n};",
                    "advanced": "// Lock-free queue using atomics"
                },
                "javascript": {
                    "beginner": "let queue = [];\nqueue.push(\"a\");\nqueue.push(\"b\");\nconsole.log(queue.shift());",
                    "intermediate": "class Queue {\n   // ...\n}",
                    "advanced": "// Stream-based"
                }
            },
            "radix_sort": {
                "python": {
                    "beginner": "def countingSort(arr, exp1):\n    n = len(arr); output = [0]*n; count = [0]*10\n    for i in range(n): index = arr[i] // exp1; count[index % 10] += 1\n    for i in range(1, 10): count[i] += count[i-1]\n    i = n - 1\n    while i >= 0: index = arr[i] // exp1; output[count[index % 10] - 1] = arr[i]; count[index % 10] -= 1; i -= 1\n    for i in range(n): arr[i] = output[i]\n\ndef radixSort(arr):\n    max1 = max(arr); exp = 1\n    while max1 / exp > 1: countingSort(arr, exp); exp *= 10",
                    "intermediate": "def radix_sort(arr):\n    # Standard implementation with comments\n    PAD = 10\n    max_val = max(arr)\n    exp = 1\n    while max_val // exp > 0:\n        counting_sort_radix(arr, exp)\n        exp *= 10\n\ndef counting_sort_radix(arr, exp):\n    n = len(arr)\n    output = [0] * n\n    count = [0] * 10\n    for i in range(n):\n        index = arr[i] // exp\n        count[index % 10] += 1\n    for i in range(1, 10):\n        count[i] += count[i-1]\n    i = n - 1\n    while i >= 0:\n        index = arr[i] // exp\n        output[count[index % 10] - 1] = arr[i]\n        count[index % 10] -= 1\n        i -= 1\n    for i in range(n):\n        arr[i] = output[i]",
                    "advanced": "def radix_sort(arr):\n    # Bitwise Radix Sort (base 2/16/256)\n    # ...\n    pass"
                },
                "java": {
                    "beginner": "static int getMax(int arr[], int n) {\n    int mx = arr[0];\n    for (int i = 1; i < n; i++) if (arr[i] > mx) mx = arr[i];\n    return mx;\n}\nstatic void countSort(int arr[], int n, int exp) {\n    int output[] = new int[n]; int i; int count[] = new int[10];\n    Arrays.fill(count, 0);\n    for (i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;\n    for (i = 1; i < 10; i++) count[i] += count[i - 1];\n    for (i = n - 1; i >= 0; i--) { output[count[(arr[i] / exp) % 10] - 1] = arr[i]; count[(arr[i] / exp) % 10]--; }\n    for (i = 0; i < n; i++) arr[i] = output[i];\n}\nstatic void radixsort(int arr[], int n) {\n    int m = getMax(arr, n);\n    for (int exp = 1; m / exp > 0; exp *= 10) countSort(arr, n, exp);\n}",
                    "intermediate": "public static void radixSort(int[] arr) {\n    // Standard with ArrayList buckets\n}",
                    "advanced": "public static void radixSort(int[] arr) {\n   // In-place LSD or MSD\n}"
                },
                "cpp": {
                    "beginner": "void countSort(int arr[], int n, int exp) {\n    int output[n]; int i, count[10] = {0};\n    for (i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;\n    for (i = 1; i < 10; i++) count[i] += count[i - 1];\n    for (i = n - 1; i >= 0; i--) { output[count[(arr[i] / exp) % 10] - 1] = arr[i]; count[(arr[i] / exp) % 10]--; }\n    for (i = 0; i < n; i++) arr[i] = output[i];\n}\nvoid radixsort(int arr[], int n) {\n    int m = getMax(arr, n);\n    for (int exp = 1; m / exp > 0; exp *= 10) countSort(arr, n, exp);\n}",
                    "intermediate": "void radixSort(vector<int>& arr) {\n    // Vector based\n}",
                    "advanced": "void radixSort(vector<int>& arr) {\n    // Parallel or Cache optimized\n}"
                },
                "javascript": {
                    "beginner": "function getNext(arr) { ... }\nfunction countingSort(arr, exp) {\n    let output = Array(arr.length); let count = Array(10).fill(0);\n    for (let i = 0; i < arr.length; i++) count[Math.floor(arr[i] / exp) % 10]++;\n    for (let i = 1; i < 10; i++) count[i] += count[i - 1];\n    for (let i = arr.length - 1; i >= 0; i--) { output[count[Math.floor(arr[i] / exp) % 10] - 1] = arr[i]; count[Math.floor(arr[i] / exp) % 10]--; }\n    for (let i = 0; i < arr.length; i++) arr[i] = output[i];\n}\nfunction radixSort(arr) {\n    let m = Math.max(...arr);\n    for (let exp = 1; Math.floor(m / exp) > 0; exp *= 10) countingSort(arr, exp);\n}",
                    "intermediate": "function radixSort(arr) {\n    // ...\n}",
                    "advanced": "const radixSort = (arr) => {\n    // ...\n};"
                }
            },
            "astar": {
                "python": {
                    "beginner": "def a_star(maze, start, end):\n    # Simplified A*\n    open_list = [start]\n    # ... (standard heuristic search logic)",
                    "intermediate": "def a_star(graph, start, end):\n    # Priority Queue based A*\n    # ...",
                    "advanced": "def a_star_bi_directional(graph, start, end):\n    # ...\n    pass"
                },
                "java": {
                    "beginner": "public void aStarSearch(int[][] grid, int[] start, int[] end) {\n    PriorityQueue<Node> openList = new PriorityQueue<>();\n    // ... (logic using Manhattan distance)",
                    "intermediate": "public void aStar(Graph g) {\n    // ...\n}",
                    "advanced": "public void aStarOptimized() {\n    // ...\n}"
                },
                "cpp": {
                    "beginner": "void aStarSearch(int grid[ROW][COL], Pair start, Pair dest) {\n    // ... (logic with open list and f=g+h scores)",
                    "intermediate": "void aStar() {\n    // ...\n}",
                    "advanced": "void aStar() {\n    // ...\n}"
                },
                "javascript": {
                    "beginner": "function aStar(grid, start, end) {\n    let openList = [start];\n    // ... (heuristic pathfinding logic)\n}",
                    "intermediate": "function aStar() {\n    // ...\n}",
                    "advanced": "const aStar = () => {\n    // ...\n};"
                }
            },
         }
        
        # Default to Python/Beginner if not found
        topic_impl = implementations.get(topic, implementations.get("bubble_sort"))
        lang_impl = topic_impl.get(language, topic_impl.get("python"))
        return lang_impl.get(level, lang_impl.get("beginner"))

    @staticmethod
    def get_narrative(type, val1=None, val2=None, language="python", level="beginner"):
        level = level.lower()
        
        if type == "compare":
            if level == "kids":
                return f"Is {val1} bigger than {val2}?"
            elif level == "beginner":
                return f"Compare {val1} and {val2}."
            elif level == "intermediate":
                return f"Check if {val1} > {val2}. If so, they are out of order."
            else: # advanced
                return f"Check inversion property: arr[j] > arr[j+1] where {val1} and {val2} are being evaluated."
        
        if type == "swap":
            if level == "kids":
                return f"Switch them! Pop!"
            elif level == "beginner":
                return f"Swap {val1} and {val2}."
            elif level == "intermediate":
                return f"Perform a swap to move {val1} further right."
            else: # advanced
                return f"Reorder elements via temporary storage or XOR swap."

        if type == "binary_mid":
             if level == "kids":
                 return f"Look at the middle number: {val1}"
             elif level == "beginner":
                 return f"Middle element is {val1}."
             elif level == "intermediate":
                 return f"Calculate pivot: (low + high) // 2. Value is {val1}."
             else: # advanced
                 return f"Evaluating median element at index mid for comparison with target."
        
        if type == "dijkstra_update":
            if level == "beginner": return f"Update distance to {val1} to {val2}."
            return f"Relaxing edge to {val1}: potential new dist = {val2}."

        if type == "knapsack_update":
             if level == "kids": return f"Can we fit {val1}?"
             return f"Checking item {val1} with weight {val2}."

        return None
