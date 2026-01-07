import re

class RuleBasedIntentParser:
    def __init__(self):
        # Map specific keywords to their template keys (as defined in app.py)
        # using a list of tuples for priority order (first match wins)
        self.patterns = [
            # Sorting
            (r'selection\s*sort', 'selection'),
            (r'bubble\s*sort', 'bubble'),
            (r'merge\s*sort', 'merge_sort'),
            (r'sort', 'bubble'), # Default sort
            (r'counting\s*sort', 'counting_sort'),
            (r'bucket\s*sort', 'bucket_sort'),
            (r'radix\s*sort', 'radix_sort'),

            # Search
            (r'binary\s*search', 'binary'),
            (r'bfs|breadth', 'bfs'),
            (r'dfs|depth', 'dfs'),
            
            # Data Structures
            (r'bst|binary\s*search\s*tree', 'bst'),
            (r'stack|push|pop', 'stack'),
            (r'queue|enqueue|dequeue', 'queue'),

            # Math / Geometry
            (r'sine|wave', 'sine'),
            (r'pythagoras', 'pythagoras'),
            (r'vector.*add', 'vector'),
            (r'vector.*sub', 'vec_sub'),
            (r'dot\s*product', 'dot_product'),
            (r'cross\s*product', 'cross_product'),
            (r'matrix', 'matrix'),
            (r'geometry|polygon', 'geometry'),
            (r'fourier', 'fourier'),

            # Calculus / Algebra
            (r'quadratic|roots', 'quadratic'),
            (r'derivative|derivation', 'derivation'),
            (r'limit', 'limit'),
            (r'integral', 'integral'),
            (r'chain\s*rule', 'chain_rule'),
            (r'algebra|expansion', 'algebra'),

            # Recursion / DP
            (r'fibonacci', 'fibonacci'),
            (r'knapsack', 'knapsack'),
            (r'lcs|longest\s*common', 'lcs'),
            (r'edit\s*distance|levenshtein', 'edit_distance'),
            (r'max\s*subarray|kadane', 'max_subarray'),

            # Graph / Backtracking
            (r'bellman-?ford', 'bellman_ford'),
            (r'floyd-?warshall', 'floyd_warshall'),
            (r'a\*|a\s*star', 'astar'),
            (r'n-?queens', 'nqueens'),
            (r'kruskal', 'kruskal_mst'),
            (r'prim', 'prim_mst'),
            (r'mst|spanning\s*tree', 'kruskal_mst'), # Default to Kruskal

            # Science / Physics
            (r'solar|planet', 'solar'),
            (r'atom|electron', 'atom'),
            (r'dna|helix', 'dna'),
            (r'bernoulli|lift|airfoil', 'bernoulli'),
            (r'star|life\s*cycle', 'life_cycle_of_star'),
            (r'water', 'water_cycle'),
            (r'photosynthesis', 'photosynthesis'),
            (r'mitosis', 'mitosis'),
            (r'electrolysis', 'electrolysis'),

            # General Charts
            (r'graph|plot|chart', 'graph'),
            (r'pie', 'pie'),
            (r'bar', 'bar_race'),
            (r'scatter', 'scatter'),
            (r'sphere|circle', 'sphere'),
        ]

        # Advanced topic mappings for generator
        self.advanced_topics = {
            "star": "life_cycle_of_star",
            "solar system": "solar",
            "water cycle": "water_cycle",
            "carbon": "carbon_cycle",
            "nitrogen": "nitrogen_cycle",
            "photosynthesis": "photosynthesis",
            "respiration": "respiration",
            "digestive": "digestive_system",
            "heart": "human_heart",
            "nervous": "nervous_system",
            "reflection": "reflection_refraction",
            "refraction": "reflection_refraction",
            "sound": "sound_propagation",
            "electricity": "electricity_basics",
            "ohm": "ohm",
            "newton": "newton",
            "friction": "friction",
            "work": "work_energy",
            "pressure": "force_and_pressure",
            "states of matter": "states_of_matter",
            "solid": "states_of_matter",
            "liquid": "states_of_matter",
            "gas": "states_of_matter",
            "global warming": "global_warming",
            "greenhouse": "greenhouse_effect",
            "capillary": "capillary_action"
        }

    def parse(self, text):
        """
        Parses the natural language text and returns a dictionary with:
        - template_key: str (The internal ID for the template)
        - difficulty: str ('beginner', 'advanced', 'kids')
        - visualization_type: str ('animation', 'code', 'graph')
        - original_query: str
        """
        text_lower = text.lower()
        
        # 1. Detect Difficulty
        difficulty = 'beginner'
        if 'advanced' in text_lower or 'expert' in text_lower or 'complex' in text_lower:
            difficulty = 'advanced'
        elif 'kid' in text_lower or 'child' in text_lower or 'simple' in text_lower or 'easy' in text_lower:
            difficulty = 'kids'

        # 2. Detect Visualization Type
        vis_type = 'animation'
        if 'code' in text_lower:
            vis_type = 'code'
        elif 'graph' in text_lower or 'plot' in text_lower:
            vis_type = 'graph'

        # 3. Detect Template Key
        matched_key = None
        
        # Check standard patterns first
        for pattern, key in self.patterns:
            if re.search(pattern, text_lower):
                matched_key = key
                break
        
        # Fallback: Check advanced topic strict matching if no pattern matched
        if not matched_key:
            for keyword, topic_key in self.advanced_topics.items():
                if keyword in text_lower:
                    # In app.py this triggers the dynamic generator
                    # We will return a special prefix to indicate dynamic generation needed
                    matched_key = f"dynamic:{topic_key}"
                    break

        return {
            "template_key": matched_key,
            "difficulty": difficulty,
            "visualization_type": vis_type,
            "original_query": text
        }
