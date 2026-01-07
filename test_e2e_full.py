import requests
import json

BASE_URL = "http://localhost:5001/generate/scenes"

TEST_CASES = [
    {"prompt": "Show me bubble sort for kids", "expected_key": "sort_bubble", "difficulty": "kids"},
    {"prompt": "Visualize selection sort advanced", "expected_key": "sort_selection", "difficulty": "advanced"},
    {"prompt": "Binary search beginner", "expected_key": "search_binary", "difficulty": "beginner"},
    # Fallback/Edge cases
    {"prompt": "Graph x squared", "expected_key": "graph", "vis_type": "graph"},
    {"prompt": "Show DNA helix", "expected_key": "dna", "vis_type": "animation"}
]

def run_tests():
    print(f"Running E2E Validation against {BASE_URL}...\n")
    failed = 0
    passed = 0
    
    for tc in TEST_CASES:
        payload = {"description": tc["prompt"]}
        print(f"TESTING: '{tc['prompt']}'")
        
        try:
            resp = requests.post(BASE_URL, json=payload)
            if resp.status_code != 200:
                print(f"  FAIL: Status Code {resp.status_code}")
                failed += 1
                continue
                
            data = resp.json()
            scene_id = data.get("sceneId", "")
            
            # Check Scene ID prefix
            if tc.get("expected_key") and tc["expected_key"] not in scene_id:
                print(f"  FAIL: Expected ID containing '{tc['expected_key']}', got '{scene_id}'")
                failed += 1
                continue
                
            # Check difficulty indicators in narrative/code if applicable
            if "difficulty" in tc:
                code = data.get("code", "")
                narratives = " ".join([a.get("narrative", "") for a in data.get("actions", [])])
                
                if tc["difficulty"] == "kids":
                    if "Pop!" not in code and "Cut the list" not in code and "Pick the smallest" not in code:
                         print("  WARN: 'kids' keywords not found in code")
                elif tc["difficulty"] == "advanced":
                    if "Time Complexity" not in code:
                         print("  WARN: 'advanced' complexity note not found in code")

            print("  PASS")
            passed += 1
            
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
            
    print(f"\nRESULTS: {passed} PASSED, {failed} FAILED")

if __name__ == "__main__":
    run_tests()
