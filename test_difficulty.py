from template_generator import generate_algo_template

def test_difficulty():
    levels = ["kids", "beginner", "advanced"]
    for lvl in levels:
        print(f"\n--- Testing Difficulty: {lvl} ---")
        try:
            res = generate_algo_template(0, difficulty=lvl)
            code = res['code']
            actions = res['actions']
            
            print(f"Code Snippet:\n{code[:80]}...")
            
            # Check for specific difficulty markers
            if lvl == "kids":
                if "Bubble Pop" not in code: print("FAIL: Kids code missing 'Bubble Pop'")
                # Check narrative
                pop_action = next((a for a in actions if "Pop" in str(a.get('narrative', ''))), None)
                if pop_action: print(f"PASS: found narrative '{pop_action['narrative']}'")
                else: print("WARN: No 'Pop' narrative found")
                
            elif lvl == "advanced":
                if "Time Complexity" not in code: print("FAIL: Advanced code missing complexity")
                else: print("PASS: Advanced code correct")

            print(f"PASS: generated {len(actions)} actions")
            
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    test_difficulty()
