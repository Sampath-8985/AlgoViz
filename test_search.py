from template_generator import generate_search_template

def test_search():
    levels = ["kids", "beginner", "advanced"]
    for lvl in levels:
        print(f"\n--- Testing Search Difficulty: {lvl} ---")
        try:
            res = generate_search_template(0, difficulty=lvl)
            code = res['code']
            actions = res['actions']
            
            print(f"Code Snippet:\n{code[:80]}...")
            
            if lvl == "kids":
                if "Cut the list" not in code: print("FAIL: Kids code incorrect")
                else: print("PASS: Kids code matches")
            elif lvl == "advanced":
                if "Time Complexity" not in code: print("FAIL: Advanced code incorrect")
                else: print("PASS: Advanced code matches")
                
            # Check for pointers
            pts = [o for o in res['objects'] if "ptr" in o['id']]
            if len(pts) >= 2: print(f"PASS: found {len(pts)} pointers")
            else: print(f"FAIL: only found {len(pts)} pointers")
            
            # Check for comparison actions
            comps = [a for a in actions if "Look" in str(a.get('narrative','')) or "Calculate" in str(a.get('narrative',''))]
            if comps: print(f"PASS: found Comparison narratives ({len(comps)})")
            
            # Check code highlighting
            highlights = [a for a in actions if 'codeLine' in a]
            if highlights: print(f"PASS: found {len(highlights)} code highlights")
            else: print("WARN: no code highlights found")

        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    test_search()
