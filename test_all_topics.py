import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000/generate/scenes"

topics = [
    "triangle", "square", "pentagon", "hexagon", "polygon 8",
    "atom 1", "element 6",
    "graph sin(x)", "plot quadratic", "graph linear",
    "Newton's Laws", "Friction", "Work Energy Principle", 
    "Solar System", "Life Cycle of Star",
    "Carbon Cycle", "Nitrogen Cycle", 
    "Greenhouse Effect", "Global Warming", 
    "Water Cycle",
    "Photosynthesis", "Respiration", 
    "Digestive System", "Human Heart", "Nervous System",
    "Electricity Basics", "Ohm's Law", 
    "Reflection Refraction", "Sound Propagation",
    "States of Matter", "Force and Pressure",
    "Capillary Action",
    "Schrodinger Equation", "Heisenberg Uncertainty",
    "Doppler Effect", "Wave Equation", "Gravitation", "Time Dilation",
    "Bubble sort", "Selection sort", "Merge sort", 
    "Binary search", "BFS Graph", 
    "Stack operations", "Queue operations",
    "Matrix multiplication 3x3", "Determinant", "Gradient Descent", 
    "Fourier Transform", "Riemann Sum", "Taylor Series", 
    "Chain Rule", "Integral", "Limit", "Derivation", 
    "Vector addition", "Vector subtraction", 
    "Cross product", "Dot product",
    "Pie chart", "Bar race", "Scatter plot",
    "DNA Helix", "Mitosis",
    "Electrolysis",
    "Full course"
]

passed = 0
failed = 0

with open("test_results_clean.txt", "w", encoding="utf-8") as f:
    f.write(f"Testing {len(topics)} topics...\n\n")
    
    for topic in topics:
        try:
            response = requests.post(BASE_URL, json={"description": topic})
            if response.status_code == 200:
                data = response.json()
                if "objects" in data and "actions" in data:
                    f.write(f"[PASS] {topic}\n")
                    passed += 1
                else:
                    f.write(f"[FAIL] {topic} - Missing objects/actions\n")
                    failed += 1
            else:
                f.write(f"[FAIL] {topic} - Status {response.status_code}\n")
                failed += 1
        except Exception as e:
            f.write(f"[ERROR] {topic} - {str(e)}\n")
            failed += 1

    f.write(f"\nSummary: {passed} Passed, {failed} Failed\n")

print("Done.")
