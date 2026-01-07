from intent_parser import RuleBasedIntentParser

parser = RuleBasedIntentParser()

def test(query):
    result = parser.parse(query)
    print(f"Query: '{query}' -> Key: {result['template_key']} (Diff: {result['difficulty']})")

print("--- Testing Intent Parser ---")
test("Show me bubble sort")
test("Binary search algo")
test("Plot a sine wave")
test("Explain BFS like I'm 5")
test("Advanced matrix multiplication")
test("Show me bernoulli principle")
test("vector addition")
