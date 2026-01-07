import os
import json
import re
from template_generator import GENERATED_TEMPLATES
from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
from intent_parser import RuleBasedIntentParser

intent_parser = RuleBasedIntentParser()

app = Flask(__name__, static_folder='public', static_url_path='')
CORS(app)

# --- 1. TEMPLATE LIBRARY (Advanced) ---

TEMPLATE_BUBBLE_SORT = {
    "sceneId": "bubble_sort",
    "width": 800,
    "height": 450,
    "duration": 12,
    "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                swap(arr[j], arr[j+1])",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Bubble Sort: [5, 3, 8, 1, 4]", "font": "bold 28px Arial", "color": "#89b4fa"}},
        
        # Bars (Modern Flat Colors)
        {"id": "bar1", "type": "bar", "props": {"x": 200, "y": 350, "width": 40, "height": 150, "color": "#f38ba8", "text": "5"}}, # Red
        {"id": "bar2", "type": "bar", "props": {"x": 260, "y": 350, "width": 40, "height": 90, "color": "#fab387", "text": "3"}},  # Orange
        {"id": "bar3", "type": "bar", "props": {"x": 320, "y": 350, "width": 40, "height": 240, "color": "#a6e3a1", "text": "8"}}, # Green
        {"id": "bar4", "type": "bar", "props": {"x": 380, "y": 350, "width": 40, "height": 30, "color": "#89b4fa", "text": "1"}},  # Blue
        {"id": "bar5", "type": "bar", "props": {"x": 440, "y": 350, "width": 40, "height": 120, "color": "#cba6f7", "text": "4"}}, # Purple
        
        # Comparison Indicator
        {"id": "comp_marker", "type": "rect", "props": {"x": 200, "y": 360, "width": 100, "height": 5, "color": "#f9e2af", "opacity": 0}},
        
        # Status
        {"id": "status", "type": "text", "props": {"x": 400, "y": 100, "text": "Starting sort...", "font": "20px monospace", "color": "#cdd6f4"}}
    ],
    "actions": [
        # Pass 1: 5 vs 3
        {"id": "mark1", "objectId": "comp_marker", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}, "narrative": "Compare 5 and 3. 5 > 3, so swap."},
        {"id": "swap1_a", "objectId": "bar1", "type": "translate", "start": 1, "end": 2, "params": {"to": {"x": 260, "y": 350}}},
        {"id": "swap1_b", "objectId": "bar2", "type": "translate", "start": 1, "end": 2, "params": {"to": {"x": 200, "y": 350}}},
        
        # Pass 1: 5 vs 8
        {"id": "move_mark2", "objectId": "comp_marker", "type": "translate", "start": 2.5, "end": 3, "params": {"to": {"x": 260, "y": 360}}, "narrative": "Compare 5 and 8. 5 < 8, no swap."},
        
        # Pass 1: 8 vs 1
        {"id": "move_mark3", "objectId": "comp_marker", "type": "translate", "start": 3.5, "end": 4, "params": {"to": {"x": 320, "y": 360}}, "narrative": "Compare 8 and 1. 8 > 1, swap."},
        {"id": "swap2_a", "objectId": "bar3", "type": "translate", "start": 4, "end": 5, "params": {"to": {"x": 380, "y": 350}}},
        {"id": "swap2_b", "objectId": "bar4", "type": "translate", "start": 4, "end": 5, "params": {"to": {"x": 320, "y": 350}}},
        
        # Pass 1: 8 vs 4

        {"id": "move_mark4", "objectId": "comp_marker", "type": "translate", "start": 5.5, "end": 6, "params": {"to": {"x": 380, "y": 360}}, "narrative": "Compare 8 and 4. 8 > 4, swap."},
        {"id": "swap3_a", "objectId": "bar3", "type": "translate", "start": 6, "end": 7, "params": {"to": {"x": 440, "y": 350}}},
        {"id": "swap3_b", "objectId": "bar5", "type": "translate", "start": 6, "end": 7, "params": {"to": {"x": 380, "y": 350}}},
        
        # 8 Sorted
        {"id": "sorted_8", "objectId": "bar3", "type": "fade", "start": 7, "end": 7.5, "params": {"opacity": 0.5}, "narrative": "8 is now in its correct sorted position."},
        
        # Pass 2: 3 vs 5 (No swap)
        {"id": "move_mark5", "objectId": "comp_marker", "type": "translate", "start": 8, "end": 8.5, "params": {"to": {"x": 200, "y": 360}}, "narrative": "Next pass. 3 < 5, ok."},
        
        # Pass 2: 5 vs 1 (Swap)
        {"id": "move_mark6", "objectId": "comp_marker", "type": "translate", "start": 9, "end": 9.5, "params": {"to": {"x": 260, "y": 360}}, "narrative": "5 > 1, swap."},
        {"id": "swap4_a", "objectId": "bar1", "type": "translate", "start": 9.5, "end": 10.5, "params": {"to": {"x": 320, "y": 350}}},
        {"id": "swap4_b", "objectId": "bar4", "type": "translate", "start": 9.5, "end": 10.5, "params": {"to": {"x": 260, "y": 350}}},
        
        # Done
        {"id": "finish", "objectId": "status", "type": "fade", "start": 11, "end": 12, "params": {"opacity": 1}, "narrative": "The array is becoming sorted."}
    ]
}

TEMPLATE_BERNOULLI = {
    "sceneId": "bernoulli_principle",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "P + 0.5 * rho * v^2 + rho * g * h = Constant",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#13111C"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Bernoulli's Principle", "font": "bold 32px Inter", "color": "#ffffff"}},
        
        # Flowchart Nodes
        {"id": "node1", "type": "rect", "props": {"x": 50, "y": 120, "width": 200, "height": 80, "color": "#1E1C29", "text": "Fluid Velocity ↑"}},
        {"id": "node2", "type": "rect", "props": {"x": 300, "y": 120, "width": 200, "height": 80, "color": "#1E1C29", "text": "Pressure ↓"}},
        {"id": "node3", "type": "rect", "props": {"x": 550, "y": 120, "width": 200, "height": 80, "color": "#1E1C29", "text": "Lift Force ↑"}},

        # Arrows
        {"id": "arrow1", "type": "arrow", "props": {"points": [250, 160], "width": 4, "color": "#00d2ff"}},
        {"id": "arrow2", "type": "arrow", "props": {"points": [500, 160], "width": 4, "color": "#00d2ff"}},

        # Image (Airfoil Diagram)
        {"id": "img_wing", "type": "image", "props": {"x": 200, "y": 250, "width": 400, "height": 150, "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Airfoil_lift_minus_drag.svg/800px-Airfoil_lift_minus_drag.svg.png"}},
        
        # Labels
        {"id": "label_app", "type": "text", "props": {"x": 400, "y": 420, "text": "Application: Airfoil Lift", "font": "italic 18px Inter", "color": "#89b4fa"}},
    ],
    "actions": [
        {"id": "anim1", "objectId": "node1", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "According to Bernoulli, as fluid velocity increases..."},
        {"id": "anim2", "objectId": "arrow1", "type": "fade", "start": 1.5, "end": 2, "params": {"opacity": 1}},
        {"id": "anim3", "objectId": "node2", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "The pressure within that fluid decreases."},
        {"id": "anim4", "objectId": "arrow2", "type": "fade", "start": 3, "end": 3.5, "params": {"opacity": 1}},
        {"id": "anim5", "objectId": "node3", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 1}, "narrative": "This pressure difference creates an upward lift force."},
        {"id": "anim6", "objectId": "img_wing", "type": "scale", "start": 5, "end": 6, "params": {"scale": 1.05}, "narrative": "This is the fundamental principle behind how airplane wings generate lift."}
    ]
}

TEMPLATE_SINE_WAVE = {
    "sceneId": "sine_wave",
    "width": 800,
    "height": 450,
    "duration": 6,
    "code": "import numpy as np\nimport matplotlib.pyplot as plt\n\nx = np.linspace(0, 2*np.pi, 100)\ny = np.sin(x)\nplt.plot(x, y)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#ffffff"}},
        {"id": "axis", "type": "axis", "props": {"x": 50, "y": 225, "width": 700, "height": 200, "color": "#ccc"}},
        {"id": "sine_path", "type": "path", "props": {"d": "M 50 225 Q 137.5 25 225 225 T 400 225 T 575 225 T 750 225", "color": "#3498db", "width": 3}},
        {"id": "dot", "type": "circle", "props": {"x": 50, "y": 225, "r": 8, "color": "#e74c3c"}},
        {"id": "label_max", "type": "text", "props": {"x": 225, "y": 20, "text": "Max (Amplitude)", "font": "16px Arial", "color": "#e74c3c", "opacity": 0}},
        {"id": "label_min", "type": "text", "props": {"x": 400, "y": 430, "text": "Min (Amplitude)", "font": "16px Arial", "color": "#e74c3c", "opacity": 0}}
    ],
    "actions": [
        {"id": "move_dot", "objectId": "dot", "type": "followPath", "start": 0, "end": 6, "params": {"pathId": "sine_path", "easing": "linear"}, "narrative": "A point moves along the sine curve, representing the phase."},
        {"id": "show_max", "objectId": "label_max", "type": "fade", "start": 1.5, "end": 2, "params": {"opacity": 1}, "narrative": "Here we reach the maximum amplitude."},
        {"id": "show_min", "objectId": "label_min", "type": "fade", "start": 3, "end": 3.5, "params": {"opacity": 1}, "narrative": "And here is the minimum amplitude."}
    ]
}

TEMPLATE_PYTHAGORAS = {
    "sceneId": "pythagoras",
    "width": 800,
    "height": 450,
    "duration": 7,
    "code": "a = 3\nb = 4\nc = sqrt(a**2 + b**2)\n# Visual proof by rearrangement",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#ffffff"}},
        {"id": "triangle", "type": "path", "props": {"d": "M 350 250 L 450 250 L 350 150 Z", "color": "#333", "width": 2}},
        {"id": "sq_a", "type": "rect", "props": {"x": 250, "y": 150, "width": 100, "height": 100, "color": "#e74c3c"}},
        {"id": "sq_b", "type": "rect", "props": {"x": 350, "y": 250, "width": 100, "height": 100, "color": "#3498db"}},
        {"id": "sq_c", "type": "rect", "props": {"x": 350, "y": 150, "width": 141.4, "height": 141.4, "color": "#2ecc71", "rotation": -45, "opacity": 0}}
    ],
    "actions": [
        {"id": "show_c", "objectId": "sq_c", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 0.5}, "narrative": "Consider a right triangle. The square of the hypotenuse..."},
        {"id": "move_a", "objectId": "sq_a", "type": "translate", "start": 3, "end": 5, "params": {"to": {"x": 350, "y": 150}}},
        {"id": "scale_a", "objectId": "sq_a", "type": "scale", "start": 3, "end": 5, "params": {"scale": 0}},
        {"id": "move_b", "objectId": "sq_b", "type": "translate", "start": 3, "end": 5, "params": {"to": {"x": 350, "y": 150}}},
        {"id": "scale_b", "objectId": "sq_b", "type": "scale", "start": 3, "end": 5, "params": {"scale": 0}},
        {"id": "grow_c", "objectId": "sq_c", "type": "fade", "start": 3, "end": 5, "params": {"opacity": 1}, "narrative": "...is equal to the sum of the squares of the other two sides."}
    ]
}

TEMPLATE_VECTOR_ADD = {
    "sceneId": "vector_addition",
    "width": 800,
    "height": 450,
    "duration": 5,
    "code": "vec_a = np.array([2, 1])\nvec_b = np.array([1, 2])\nvec_sum = vec_a + vec_b",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#ffffff"}},
        {"id": "grid", "type": "axis", "props": {"x": 50, "y": 400, "width": 700, "height": 350, "color": "#eee"}},
        {"id": "vec_a", "type": "arrow", "props": {"x": 100, "y": 350, "width": 4, "color": "#3498db", "points": [100, 350, 300, 250]}},
        {"id": "vec_b", "type": "arrow", "props": {"x": 100, "y": 350, "width": 4, "color": "#2ecc71", "points": [100, 350, 200, 150]}},
        {"id": "vec_sum", "type": "arrow", "props": {"x": 100, "y": 350, "width": 4, "color": "#e74c3c", "points": [100, 350, 400, 50], "opacity": 0}}
    ],
    "actions": [
        {"id": "move_b", "objectId": "vec_b", "type": "translate", "start": 1, "end": 3, "params": {"to": {"x": 300, "y": 250}}, "narrative": "To add vectors, we place the tail of Vector B at the head of Vector A."},
        {"id": "draw_sum", "objectId": "vec_sum", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 1}, "narrative": "The resultant vector goes from the start of A to the end of B."}
    ]
}

TEMPLATE_SPHERE = {
    "sceneId": "sphere_expansion",
    "width": 800,
    "height": 450,
    "duration": 5,
    "code": "radius = 10\nwhile radius < 150:\n    radius += 1\n    draw_sphere(radius)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#111"}},
        {"id": "circle", "type": "sphere", "props": {"x": 400, "y": 225, "r": 10, "color": "#3498db", "color2": "#2980b9"}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 400, "text": "Expanding to Sphere", "font": "20px Arial", "color": "#fff", "opacity": 0}}
    ],
    "actions": [
        {"id": "expand", "objectId": "circle", "type": "scale", "start": 0.5, "end": 3.5, "params": {"scale": 15}, "narrative": "A 2D circle expands uniformly..."},
        {"id": "show_label", "objectId": "label", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 1}, "narrative": "...creating the illusion of a 3D sphere using radial gradients."}
    ]
}

TEMPLATE_MATRIX = {
    "sceneId": "matrix_mult",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "A = [[1, 2], [3, 4]]\nB = [[5, 6], [7, 8]]\nC = np.dot(A, B)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#fff"}},
        # Matrix A
        {"id": "a_bracket_l", "type": "text", "props": {"x": 100, "y": 200, "text": "[", "font": "60px Arial", "color": "#333"}},
        {"id": "a11", "type": "text", "props": {"x": 120, "y": 180, "text": "1", "font": "24px Arial", "color": "#333"}},
        {"id": "a12", "type": "text", "props": {"x": 160, "y": 180, "text": "2", "font": "24px Arial", "color": "#333"}},
        {"id": "a21", "type": "text", "props": {"x": 120, "y": 220, "text": "3", "font": "24px Arial", "color": "#333"}},
        {"id": "a22", "type": "text", "props": {"x": 160, "y": 220, "text": "4", "font": "24px Arial", "color": "#333"}},
        {"id": "a_bracket_r", "type": "text", "props": {"x": 180, "y": 200, "text": "]", "font": "60px Arial", "color": "#333"}},
        
        # Matrix B
        {"id": "b_bracket_l", "type": "text", "props": {"x": 220, "y": 200, "text": "[", "font": "60px Arial", "color": "#333"}},
        {"id": "b11", "type": "text", "props": {"x": 240, "y": 180, "text": "5", "font": "24px Arial", "color": "#333"}},
        {"id": "b12", "type": "text", "props": {"x": 280, "y": 180, "text": "6", "font": "24px Arial", "color": "#333"}},
        {"id": "b21", "type": "text", "props": {"x": 240, "y": 220, "text": "7", "font": "24px Arial", "color": "#333"}},
        {"id": "b22", "type": "text", "props": {"x": 280, "y": 220, "text": "8", "font": "24px Arial", "color": "#333"}},
        {"id": "b_bracket_r", "type": "text", "props": {"x": 300, "y": 200, "text": "]", "font": "60px Arial", "color": "#333"}},
        
        # Equals
        {"id": "eq", "type": "text", "props": {"x": 340, "y": 200, "text": "=", "font": "30px Arial", "color": "#333"}},
        
        # Result C
        {"id": "c_bracket_l", "type": "text", "props": {"x": 380, "y": 200, "text": "[", "font": "60px Arial", "color": "#333"}},
        {"id": "c11", "type": "text", "props": {"x": 400, "y": 180, "text": "19", "font": "24px Arial", "color": "#e74c3c", "opacity": 0}}, # 1*5 + 2*7 = 5+14=19
        {"id": "c_bracket_r", "type": "text", "props": {"x": 440, "y": 200, "text": "]", "font": "60px Arial", "color": "#333"}},
        
        # Highlight Box (Row A)
        {"id": "hl_row_a", "type": "rect", "props": {"x": 115, "y": 160, "width": 60, "height": 30, "color": "rgba(52, 152, 219, 0.3)", "opacity": 0}},
        # Highlight Box (Col B)
        {"id": "hl_col_b", "type": "rect", "props": {"x": 235, "y": 160, "width": 30, "height": 80, "color": "rgba(46, 204, 113, 0.3)", "opacity": 0}},
        
        # Calculation Text
        {"id": "calc_text", "type": "text", "props": {"x": 400, "y": 300, "text": "1*5 + 2*7 = 19", "font": "20px Arial", "color": "#333", "opacity": 0}}
    ],
    "actions": [
        {"id": "show_hl_a", "objectId": "hl_row_a", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "Take the first row of Matrix A..."},
        {"id": "show_hl_b", "objectId": "hl_col_b", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "...and the first column of Matrix B."},
        {"id": "show_calc", "objectId": "calc_text", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Multiply corresponding elements and sum them up: 1 times 5 plus 2 times 7."},
        {"id": "show_res", "objectId": "c11", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}, "narrative": "The result, 19, goes into the first cell of the result matrix."}
    ]
}

TEMPLATE_GEOMETRY_SHAPES = {
    "sceneId": "geometry_shapes",
    "width": 800,
    "height": 450,
    "duration": 12,
    "code": "# Visualizing Regular Polygons\nshapes = ['Triangle', 'Square', 'Pentagon', 'Hexagon']\nfor shape in shapes:\n    draw(shape)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#f0f0f0"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Regular Polygons", "font": "30px Arial", "color": "#333"}},
        {"id": "triangle", "type": "path", "props": {"d": "M 400 150 L 486 300 L 314 300 Z", "color": "#e74c3c", "width": 3, "opacity": 0}},
        {"id": "square", "type": "rect", "props": {"x": 325, "y": 150, "width": 150, "height": 150, "color": "#3498db", "opacity": 0}},
        {"id": "pentagon", "type": "path", "props": {"d": "M 400 130 L 542 233 L 488 398 L 312 398 L 258 233 Z", "color": "#2ecc71", "width": 3, "opacity": 0}},
        {"id": "hexagon", "type": "path", "props": {"d": "M 400 150 L 475 193 L 475 279 L 400 322 L 325 279 L 325 193 Z", "color": "#9b59b6", "width": 3, "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 400, "text": "", "font": "24px Arial", "color": "#555"}}
    ],
    "actions": [
        {"id": "show_tri", "objectId": "triangle", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "A Triangle has 3 sides."},
        {"id": "hide_tri", "objectId": "triangle", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 0}},
        {"id": "show_sq", "objectId": "square", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}, "narrative": "A Square has 4 equal sides."},
        {"id": "hide_sq", "objectId": "square", "type": "fade", "start": 6, "end": 7, "params": {"opacity": 0}},
        {"id": "show_pent", "objectId": "pentagon", "type": "fade", "start": 7, "end": 8, "params": {"opacity": 1}, "narrative": "A Pentagon has 5 sides."},
        {"id": "hide_pent", "objectId": "pentagon", "type": "fade", "start": 9, "end": 10, "params": {"opacity": 0}},
        {"id": "show_hex", "objectId": "hexagon", "type": "fade", "start": 10, "end": 11, "params": {"opacity": 1}, "narrative": "A Hexagon has 6 sides."}
    ]
}

TEMPLATE_DERIVATION = {
    "sceneId": "derivation_calc",
    "width": 800,
    "height": 450,
    "duration": 12,
    "code": "f(x) = x^2\n# Definition of Derivative\nf'(x) = lim(h->0) [(x+h)^2 - x^2] / h\n# Expand (x+h)^2\n      = lim(h->0) [x^2 + 2xh + h^2 - x^2] / h\n# Cancel x^2\n      = lim(h->0) [2xh + h^2] / h\n# Divide by h\n      = 2x + h  (as h->0)\n      = 2x",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 40, "text": "Derivative of f(x) = x²", "font": "bold 28px Arial", "color": "#89b4fa"}},
        
        # Equations
        {"id": "eq1", "type": "text", "props": {"x": 50, "y": 100, "text": "f(x) = x²", "font": "24px monospace", "color": "#cdd6f4", "opacity": 0}},
        {"id": "eq2", "type": "text", "props": {"x": 50, "y": 150, "text": "f'(x) = lim(h→0) [ (x+h)² - x² ] / h", "font": "24px monospace", "color": "#cdd6f4", "opacity": 0}},
        {"id": "eq3", "type": "text", "props": {"x": 135, "y": 200, "text": "= lim(h→0) [ x² + 2xh + h² - x² ] / h", "font": "24px monospace", "color": "#cdd6f4", "opacity": 0}},
        {"id": "eq4", "type": "text", "props": {"x": 135, "y": 250, "text": "= lim(h→0) [ 2xh + h² ] / h", "font": "24px monospace", "color": "#cdd6f4", "opacity": 0}},
        {"id": "eq5", "type": "text", "props": {"x": 135, "y": 300, "text": "= 2x + h", "font": "24px monospace", "color": "#cdd6f4", "opacity": 0}},
        {"id": "eq6", "type": "text", "props": {"x": 135, "y": 350, "text": "= 2x", "font": "bold 32px monospace", "color": "#a6e3a1", "opacity": 0}},

        # Annotations / Highlights
        {"id": "strike1", "type": "rect", "props": {"x": 320, "y": 192, "width": 30, "height": 2, "color": "#f38ba8", "opacity": 0}}, # Strike x^2
        {"id": "strike2", "type": "rect", "props": {"x": 530, "y": 192, "width": 40, "height": 2, "color": "#f38ba8", "opacity": 0}}, # Strike -x^2
        
        {"id": "highlight_box", "type": "rect", "props": {"x": 40, "y": 80, "width": 720, "height": 40, "color": "rgba(255, 255, 255, 0.1)", "opacity": 0}}
    ],
    "actions": [
        # Step 1: Intro
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0, "end": 1, "params": {"opacity": 1}},
        {"id": "show_eq1", "objectId": "eq1", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "Let's find the derivative of x squared."},
        {"id": "hl_1", "objectId": "highlight_box", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}},

        # Step 2: Definition
        {"id": "show_eq2", "objectId": "eq2", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "Using the limit definition of the derivative..."},
        {"id": "move_hl_2", "objectId": "highlight_box", "type": "translate", "start": 2, "end": 3, "params": {"to": {"x": 40, "y": 130}}},

        # Step 3: Expansion
        {"id": "show_eq3", "objectId": "eq3", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}, "narrative": "We expand the term (x + h) squared."},
        {"id": "move_hl_3", "objectId": "highlight_box", "type": "translate", "start": 4, "end": 5, "params": {"to": {"x": 40, "y": 180}}},

        # Step 4: Cancellation
        {"id": "strike_x2", "objectId": "strike1", "type": "fade", "start": 5.5, "end": 6, "params": {"opacity": 1}, "narrative": "Notice that x squared and negative x squared cancel out."},
        {"id": "strike_nx2", "objectId": "strike2", "type": "fade", "start": 5.5, "end": 6, "params": {"opacity": 1}},
        
        # Step 5: Simplify
        {"id": "show_eq4", "objectId": "eq4", "type": "fade", "start": 7, "end": 8, "params": {"opacity": 1}, "narrative": "This leaves us with 2xh plus h squared, all over h."},
        {"id": "move_hl_4", "objectId": "highlight_box", "type": "translate", "start": 7, "end": 8, "params": {"to": {"x": 40, "y": 230}}},

        # Step 6: Divide
        {"id": "show_eq5", "objectId": "eq5", "type": "fade", "start": 9, "end": 10, "params": {"opacity": 1}, "narrative": "Dividing by h gives 2x plus h."},
        {"id": "move_hl_5", "objectId": "highlight_box", "type": "translate", "start": 9, "end": 10, "params": {"to": {"x": 40, "y": 280}}},

        # Step 7: Limit
        {"id": "show_eq6", "objectId": "eq6", "type": "fade", "start": 10.5, "end": 11.5, "params": {"opacity": 1}, "narrative": "Finally, as h approaches 0, the term h vanishes, leaving 2x."},
        {"id": "move_hl_6", "objectId": "highlight_box", "type": "translate", "start": 10.5, "end": 11.5, "params": {"to": {"x": 40, "y": 330}}}
    ]
}

TEMPLATE_GRAPH_PLOT = {
    "sceneId": "graph_plot",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "import matplotlib.pyplot as plt\nimport numpy as np\n\n# Advanced Plotting\nx = np.linspace(0, 10, 100)\ny = np.sin(x) + x/2\nplt.style.use('dark_background')\nplt.plot(x, y, color='cyan')",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        # Grid
        {"id": "grid", "type": "path", "props": {"d": "M 50 100 L 750 100 M 50 200 L 750 200 M 50 300 L 750 300 M 150 50 L 150 400 M 350 50 L 350 400 M 550 50 L 550 400", "color": "#333", "width": 1, "opacity": 0}},
        # Axis
        {"id": "axis_main", "type": "axis", "props": {"x": 50, "y": 400, "width": 700, "height": 350, "color": "#ccc", "opacity": 0}},
        # Labels
        {"id": "title", "type": "text", "props": {"x": 400, "y": 40, "text": "Growth Projection 2025", "font": "bold 24px Arial", "color": "#fff", "opacity": 0}},
        {"id": "label_x", "type": "text", "props": {"x": 400, "y": 440, "text": "Time (Quarters)", "font": "16px Arial", "color": "#aaa", "opacity": 0}},
        # Data Line
        {"id": "trend_line", "type": "path", "props": {"d": "M 50 350 L 150 300 L 250 320 L 350 200 L 450 150 L 550 180 L 650 100 L 750 50", "color": "#00d2ff", "width": 3, "opacity": 0}},
        # Data Points
        {"id": "p1", "type": "circle", "props": {"x": 50, "y": 350, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "p2", "type": "circle", "props": {"x": 150, "y": 300, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "p3", "type": "circle", "props": {"x": 250, "y": 320, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "p4", "type": "circle", "props": {"x": 350, "y": 200, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "p5", "type": "circle", "props": {"x": 450, "y": 150, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "p6", "type": "circle", "props": {"x": 550, "y": 180, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "p7", "type": "circle", "props": {"x": 650, "y": 100, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "p8", "type": "circle", "props": {"x": 750, "y": 50, "r": 5, "color": "#fff", "opacity": 0}},
        # Scanner
        {"id": "scanner", "type": "rect", "props": {"x": 50, "y": 50, "width": 2, "height": 350, "color": "rgba(255, 255, 255, 0.3)", "opacity": 0}},
        {"id": "scanner_val", "type": "text", "props": {"x": 60, "y": 60, "text": "Peak", "font": "14px Arial", "color": "#00d2ff", "opacity": 0}}
    ],
    "actions": [
        {"id": "bg_anim", "objectId": "axis_main", "type": "fade", "start": 0, "end": 1, "params": {"opacity": 1}, "narrative": "Setting up the coordinate system."},
        {"id": "grid_anim", "objectId": "grid", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 0.5}},
        {"id": "text_anim", "objectId": "title", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}},
        {"id": "text_anim2", "objectId": "label_x", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}},
        
        # Plot Points
        {"id": "p1_s", "objectId": "p1", "type": "scale", "start": 2, "end": 2.2, "params": {"scale": 1.5}, "narrative": "Plotting data points..."},
        {"id": "p1_f", "objectId": "p1", "type": "fade", "start": 2, "end": 2.1, "params": {"opacity": 1}},
        {"id": "p2_f", "objectId": "p2", "type": "fade", "start": 2.1, "end": 2.2, "params": {"opacity": 1}},
        {"id": "p3_f", "objectId": "p3", "type": "fade", "start": 2.2, "end": 2.3, "params": {"opacity": 1}},
        {"id": "p4_f", "objectId": "p4", "type": "fade", "start": 2.3, "end": 2.4, "params": {"opacity": 1}},
        {"id": "p5_f", "objectId": "p5", "type": "fade", "start": 2.4, "end": 2.5, "params": {"opacity": 1}},
        {"id": "p6_f", "objectId": "p6", "type": "fade", "start": 2.5, "end": 2.6, "params": {"opacity": 1}},
        {"id": "p7_f", "objectId": "p7", "type": "fade", "start": 2.6, "end": 2.7, "params": {"opacity": 1}},
        {"id": "p8_f", "objectId": "p8", "type": "fade", "start": 2.7, "end": 2.8, "params": {"opacity": 1}},
        
        # Connect Line
        {"id": "draw_line", "objectId": "trend_line", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Interpolating the trend line."},
        
        # Scanner Animation
        {"id": "scan_start", "objectId": "scanner", "type": "fade", "start": 4.5, "end": 5, "params": {"opacity": 1}, "narrative": "Analyzing peak performance periods."},
        {"id": "scan_move", "objectId": "scanner", "type": "translate", "start": 5, "end": 8, "params": {"to": {"x": 750, "y": 50}}},
        {"id": "scan_val_in", "objectId": "scanner_val", "type": "fade", "start": 7, "end": 7.5, "params": {"opacity": 1}},
        {"id": "scan_val_move", "objectId": "scanner_val", "type": "translate", "start": 5, "end": 8, "params": {"to": {"x": 760, "y": 60}}}
    ]
}

TEMPLATE_ALGO_BINARY = {
    "sceneId": "binary_search",
    "width": 800,
    "height": 450,
    "duration": 14,
    "code": "def binary_search(arr, target):\n    low, high = 0, len(arr)-1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Binary Search: Find 42", "font": "bold 28px Arial", "color": "#89b4fa"}},
        
        # Array Elements (Bars + Text)
        # Using a loop-like structure for definition would be cleaner but hardcoded for template simplicity
        # Indices: 0 to 8. Values: 10, 25, 32, 42, 55, 68, 71, 89, 94
        {"id": "b0", "type": "rect", "props": {"x": 50, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t0", "type": "text", "props": {"x": 80, "y": 235, "text": "10", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b1", "type": "rect", "props": {"x": 120, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t1", "type": "text", "props": {"x": 150, "y": 235, "text": "25", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b2", "type": "rect", "props": {"x": 190, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t2", "type": "text", "props": {"x": 220, "y": 235, "text": "32", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b3", "type": "rect", "props": {"x": 260, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t3", "type": "text", "props": {"x": 290, "y": 235, "text": "42", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b4", "type": "rect", "props": {"x": 330, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t4", "type": "text", "props": {"x": 360, "y": 235, "text": "55", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b5", "type": "rect", "props": {"x": 400, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t5", "type": "text", "props": {"x": 430, "y": 235, "text": "68", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b6", "type": "rect", "props": {"x": 470, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t6", "type": "text", "props": {"x": 500, "y": 235, "text": "71", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b7", "type": "rect", "props": {"x": 540, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t7", "type": "text", "props": {"x": 570, "y": 235, "text": "89", "font": "20px Arial", "color": "#cdd6f4"}},
        
        {"id": "b8", "type": "rect", "props": {"x": 610, "y": 200, "width": 60, "height": 60, "color": "#313244", "opacity": 1}},
        {"id": "t8", "type": "text", "props": {"x": 640, "y": 235, "text": "94", "font": "20px Arial", "color": "#cdd6f4"}},

        # Pointers
        {"id": "ptr_low", "type": "text", "props": {"x": 80, "y": 300, "text": "L", "font": "bold 24px Arial", "color": "#fab387", "opacity": 0}},
        {"id": "ptr_high", "type": "text", "props": {"x": 640, "y": 300, "text": "H", "font": "bold 24px Arial", "color": "#fab387", "opacity": 0}},
        {"id": "ptr_mid", "type": "text", "props": {"x": 360, "y": 160, "text": "M", "font": "bold 24px Arial", "color": "#f9e2af", "opacity": 0}},
        
        # Status Text
        {"id": "status", "type": "text", "props": {"x": 400, "y": 400, "text": "Initializing...", "font": "20px monospace", "color": "#a6adc8"}}
    ],
    "actions": [
        # Step 1: Init
        {"id": "show_ptrs", "objectId": "ptr_low", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "Set Low to 0 and High to 8."},
        {"id": "show_ptr_h", "objectId": "ptr_high", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}},
        
        # Step 2: First Mid
        {"id": "calc_mid1", "objectId": "ptr_mid", "type": "fade", "start": 2, "end": 2.5, "params": {"opacity": 1}, "narrative": "Calculate Mid: (0 + 8) / 2 = 4. Value is 55."},
        {"id": "hl_mid1", "objectId": "b4", "type": "fade", "start": 2, "end": 2.5, "params": {"color": "#f9e2af"}}, # Highlight Mid
        
        # Step 3: Compare
        {"id": "comp1", "objectId": "status", "type": "fade", "start": 3, "end": 3.5, "params": {"opacity": 0}, "narrative": "55 > 42. Target is in the left half."},
        # Hack to update text: fade out old, fade in new (not supported by engine yet, so we just narrate and move pointers)
        
        # Step 4: Move High
        {"id": "move_high", "objectId": "ptr_high", "type": "translate", "start": 4, "end": 5, "params": {"to": {"x": 290, "y": 300}}, "narrative": "Set High to Mid - 1 (Index 3)."},
        {"id": "dim_right", "objectId": "b4", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.3, "color": "#313244"}}, # Dim processed
        {"id": "dim_right5", "objectId": "b5", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.3}},
        {"id": "dim_right6", "objectId": "b6", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.3}},
        {"id": "dim_right7", "objectId": "b7", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.3}},
        {"id": "dim_right8", "objectId": "b8", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.3}},

        # Step 5: Second Mid
        {"id": "move_mid2", "objectId": "ptr_mid", "type": "translate", "start": 6, "end": 7, "params": {"to": {"x": 150, "y": 160}}, "narrative": "New Mid: (0 + 3) // 2 = 1. Value is 25."},
        {"id": "hl_mid2", "objectId": "b1", "type": "fade", "start": 6, "end": 7, "params": {"color": "#f9e2af"}},
        
        # Step 6: Compare
        {"id": "comp2", "objectId": "status", "type": "fade", "start": 7.5, "end": 8, "params": {"opacity": 1}, "narrative": "25 < 42. Target is in the right half."},
        
        # Step 7: Move Low
        {"id": "move_low", "objectId": "ptr_low", "type": "translate", "start": 8.5, "end": 9.5, "params": {"to": {"x": 220, "y": 300}}, "narrative": "Set Low to Mid + 1 (Index 2)."},
        {"id": "dim_left0", "objectId": "b0", "type": "fade", "start": 8.5, "end": 9.5, "params": {"opacity": 0.3}},
        {"id": "dim_left1", "objectId": "b1", "type": "fade", "start": 8.5, "end": 9.5, "params": {"opacity": 0.3, "color": "#313244"}},

        # Step 8: Third Mid
        {"id": "move_mid3", "objectId": "ptr_mid", "type": "translate", "start": 10, "end": 11, "params": {"to": {"x": 220, "y": 160}}, "narrative": "New Mid: (2 + 3) // 2 = 2. Value is 32."},
         {"id": "hl_mid3", "objectId": "b2", "type": "fade", "start": 10, "end": 11, "params": {"color": "#f9e2af"}},
         
        # Step 9: Compare & Move Low
        {"id": "comp3", "objectId": "status", "type": "fade", "start": 11.5, "end": 12, "params": {"opacity": 1}, "narrative": "32 < 42. Move Low to 3."},
        {"id": "move_low2", "objectId": "ptr_low", "type": "translate", "start": 12, "end": 12.5, "params": {"to": {"x": 290, "y": 300}}},
        {"id": "dim_left2", "objectId": "b2", "type": "fade", "start": 12, "end": 12.5, "params": {"opacity": 0.3, "color": "#313244"}},
        
        # Step 10: Found
        {"id": "move_mid4", "objectId": "ptr_mid", "type": "translate", "start": 12.5, "end": 13, "params": {"to": {"x": 290, "y": 160}}, "narrative": "New Mid is 3. Value is 42. Match found!"},
        {"id": "found_anim", "objectId": "b3", "type": "fade", "start": 13, "end": 14, "params": {"color": "#a6e3a1"}}, # Green
        {"id": "found_text", "objectId": "t3", "type": "scale", "start": 13, "end": 14, "params": {"scale": 1.5}}
    ]
}

TEMPLATE_ATOM = {
    "sceneId": "atom_model",
    "width": 800,
    "height": 450,
    "duration": 6,
    "code": "# Bohr Model\n# Electrons orbit the nucleus",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#111"}},
        {"id": "nucleus", "type": "circle", "props": {"x": 400, "y": 225, "r": 20, "color": "#e74c3c"}},
        {"id": "orbit1", "type": "path", "props": {"d": "M 400 225 m -100, 0 a 100,100 0 1,0 200,0 a 100,100 0 1,0 -200,0", "color": "#555", "width": 1}},
        {"id": "electron1", "type": "circle", "props": {"x": 300, "y": 225, "r": 8, "color": "#3498db"}},
        {"id": "orbit2", "type": "path", "props": {"d": "M 400 225 m -160, 0 a 160,160 0 1,0 320,0 a 160,160 0 1,0 -320,0", "color": "#555", "width": 1}},
        {"id": "electron2", "type": "circle", "props": {"x": 560, "y": 225, "r": 8, "color": "#3498db"}}
    ],
    "actions": [
        {"id": "move_e1", "objectId": "electron1", "type": "followPath", "start": 0, "end": 6, "params": {"pathId": "orbit1"}, "narrative": "Electrons orbit the nucleus in specific energy levels."},
        {"id": "move_e2", "objectId": "electron2", "type": "followPath", "start": 0, "end": 6, "params": {"pathId": "orbit2"}}
    ]
}

TEMPLATE_ALGO_BFS = {
    "sceneId": "bfs_graph",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "queue = [Start]\nvisited = {Start}\nwhile queue:\n    node = queue.pop(0)\n    for neighbor in node.neighbors:\n        if neighbor not in visited:\n            visited.add(neighbor)\n            queue.append(neighbor)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "BFS Graph Traversal", "font": "bold 28px Arial", "color": "#89b4fa"}},
        
        # Edges (Draw first so they are behind nodes)
        {"id": "e1", "type": "path", "props": {"d": "M 400 100 L 300 200", "color": "#45475a", "width": 4}},
        {"id": "e2", "type": "path", "props": {"d": "M 400 100 L 500 200", "color": "#45475a", "width": 4}},
        {"id": "e3", "type": "path", "props": {"d": "M 300 200 L 200 300", "color": "#45475a", "width": 4}},
        {"id": "e4", "type": "path", "props": {"d": "M 300 200 L 350 300", "color": "#45475a", "width": 4}},
        {"id": "e5", "type": "path", "props": {"d": "M 500 200 L 450 300", "color": "#45475a", "width": 4}},
        {"id": "e6", "type": "path", "props": {"d": "M 500 200 L 600 300", "color": "#45475a", "width": 4}},
        
        # Nodes
        {"id": "n1", "type": "circle", "props": {"x": 400, "y": 100, "r": 25, "color": "#313244"}}, # Root
        {"id": "t1", "type": "text", "props": {"x": 400, "y": 108, "text": "A", "font": "bold 20px Arial", "color": "#fff"}},
        
        {"id": "n2", "type": "circle", "props": {"x": 300, "y": 200, "r": 25, "color": "#313244"}},
        {"id": "t2", "type": "text", "props": {"x": 300, "y": 208, "text": "B", "font": "bold 20px Arial", "color": "#fff"}},
        
        {"id": "n3", "type": "circle", "props": {"x": 500, "y": 200, "r": 25, "color": "#313244"}},
        {"id": "t3", "type": "text", "props": {"x": 500, "y": 208, "text": "C", "font": "bold 20px Arial", "color": "#fff"}},
        
        {"id": "n4", "type": "circle", "props": {"x": 200, "y": 300, "r": 25, "color": "#313244"}},
        {"id": "t4", "type": "text", "props": {"x": 200, "y": 308, "text": "D", "font": "bold 20px Arial", "color": "#fff"}},
        
        {"id": "n5", "type": "circle", "props": {"x": 350, "y": 300, "r": 25, "color": "#313244"}},
        {"id": "t5", "type": "text", "props": {"x": 350, "y": 308, "text": "E", "font": "bold 20px Arial", "color": "#fff"}},
        
        {"id": "n6", "type": "circle", "props": {"x": 450, "y": 300, "r": 25, "color": "#313244"}},
        {"id": "t6", "type": "text", "props": {"x": 450, "y": 308, "text": "F", "font": "bold 20px Arial", "color": "#fff"}},
        
        {"id": "n7", "type": "circle", "props": {"x": 600, "y": 300, "r": 25, "color": "#313244"}},
        {"id": "t7", "type": "text", "props": {"x": 600, "y": 308, "text": "G", "font": "bold 20px Arial", "color": "#fff"}},

        # Queue Visualization
        {"id": "q_box", "type": "rect", "props": {"x": 50, "y": 380, "width": 700, "height": 50, "color": "#313244"}},
        {"id": "q_label", "type": "text", "props": {"x": 50, "y": 370, "text": "Queue:", "font": "16px Arial", "color": "#aaa"}},
        {"id": "q_text", "type": "text", "props": {"x": 70, "y": 412, "text": "", "font": "20px monospace", "color": "#f9e2af"}}
    ],
    "actions": [
        # Start
        {"id": "visit_a", "objectId": "n1", "type": "fade", "start": 0.5, "end": 1, "params": {"color": "#a6e3a1"}, "narrative": "Start at Node A. Add to Queue."},
        {"id": "q_a", "objectId": "q_text", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}}, # Hack: can't change text content dynamically yet
        
        # Visit Neighbors of A
        {"id": "visit_b", "objectId": "n2", "type": "fade", "start": 2, "end": 2.5, "params": {"color": "#fab387"}, "narrative": "Visit neighbors B and C."},
        {"id": "visit_c", "objectId": "n3", "type": "fade", "start": 2.5, "end": 3, "params": {"color": "#fab387"}},
        
        # Process B
        {"id": "proc_b", "objectId": "n2", "type": "fade", "start": 4, "end": 4.5, "params": {"color": "#a6e3a1"}, "narrative": "Process B. Visit neighbors D and E."},
        {"id": "visit_d", "objectId": "n4", "type": "fade", "start": 5, "end": 5.5, "params": {"color": "#fab387"}},
        {"id": "visit_e", "objectId": "n5", "type": "fade", "start": 5.5, "end": 6, "params": {"color": "#fab387"}},
        
        # Process C
        {"id": "proc_c", "objectId": "n3", "type": "fade", "start": 7, "end": 7.5, "params": {"color": "#a6e3a1"}, "narrative": "Process C. Visit neighbors F and G."},
        {"id": "visit_f", "objectId": "n6", "type": "fade", "start": 8, "end": 8.5, "params": {"color": "#fab387"}},
        {"id": "visit_g", "objectId": "n7", "type": "fade", "start": 8.5, "end": 9, "params": {"color": "#fab387"}},
        
        # Finish
        {"id": "finish", "objectId": "n4", "type": "fade", "start": 9.5, "end": 10, "params": {"color": "#a6e3a1"}, "narrative": "All nodes visited level by level."},
        {"id": "finish5", "objectId": "n5", "type": "fade", "start": 9.5, "end": 10, "params": {"color": "#a6e3a1"}},
        {"id": "finish6", "objectId": "n6", "type": "fade", "start": 9.5, "end": 10, "params": {"color": "#a6e3a1"}},
        {"id": "finish7", "objectId": "n7", "type": "fade", "start": 9.5, "end": 10, "params": {"color": "#a6e3a1"}}
    ]
}

TEMPLATE_BUBBLE_SORT = {
    "sceneId": "bubble_sort",
    "width": 800,
    "height": 450,
    "duration": 20,
    "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                swap(arr[j], arr[j+1])",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Bubble Sort: [5, 3, 8, 1, 4]", "font": "bold 28px Arial", "color": "#89b4fa"}},
        
        # Bars
        {"id": "bar1", "type": "bar", "props": {"x": 200, "y": 350, "width": 40, "height": 150, "color": "#f38ba8", "text": "5"}},
        {"id": "bar2", "type": "bar", "props": {"x": 260, "y": 350, "width": 40, "height": 90, "color": "#fab387", "text": "3"}},
        {"id": "bar3", "type": "bar", "props": {"x": 320, "y": 350, "width": 40, "height": 240, "color": "#a6e3a1", "text": "8"}},
        {"id": "bar4", "type": "bar", "props": {"x": 380, "y": 350, "width": 40, "height": 30, "color": "#89b4fa", "text": "1"}},
        {"id": "bar5", "type": "bar", "props": {"x": 440, "y": 350, "width": 40, "height": 120, "color": "#cba6f7", "text": "4"}},
        
        {"id": "comp_marker", "type": "rect", "props": {"x": 200, "y": 360, "width": 100, "height": 5, "color": "#f9e2af", "opacity": 0}}
    ],
    "actions": [
        # --- PASS 1 ---
        # 5 vs 3
        {"id": "p1_1", "objectId": "comp_marker", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}, "narrative": "Pass 1. Compare 5 and 3. Swap."},
        {"id": "p1_1_s1", "objectId": "bar1", "type": "translate", "start": 1, "end": 1.5, "params": {"to": {"x": 260, "y": 350}}},
        {"id": "p1_1_s2", "objectId": "bar2", "type": "translate", "start": 1, "end": 1.5, "params": {"to": {"x": 200, "y": 350}}},
        
        # 5 vs 8
        {"id": "p1_2", "objectId": "comp_marker", "type": "translate", "start": 2, "end": 2.5, "params": {"to": {"x": 260, "y": 360}}, "narrative": "Compare 5 and 8. No swap."},
        
        # 8 vs 1
        {"id": "p1_3", "objectId": "comp_marker", "type": "translate", "start": 3, "end": 3.5, "params": {"to": {"x": 320, "y": 360}}, "narrative": "Compare 8 and 1. Swap."},
        {"id": "p1_3_s1", "objectId": "bar3", "type": "translate", "start": 3.5, "end": 4, "params": {"to": {"x": 380, "y": 350}}},
        {"id": "p1_3_s2", "objectId": "bar4", "type": "translate", "start": 3.5, "end": 4, "params": {"to": {"x": 320, "y": 350}}},
        
        # 8 vs 4
        {"id": "p1_4", "objectId": "comp_marker", "type": "translate", "start": 4.5, "end": 5, "params": {"to": {"x": 380, "y": 360}}, "narrative": "Compare 8 and 4. Swap."},
        {"id": "p1_4_s1", "objectId": "bar3", "type": "translate", "start": 5, "end": 5.5, "params": {"to": {"x": 440, "y": 350}}},
        {"id": "p1_4_s2", "objectId": "bar5", "type": "translate", "start": 5, "end": 5.5, "params": {"to": {"x": 380, "y": 350}}},
        
        {"id": "p1_done", "objectId": "bar3", "type": "fade", "start": 5.5, "end": 6, "params": {"opacity": 0.5}, "narrative": "8 is sorted."},

        # --- PASS 2 ---
        # 3 vs 5
        {"id": "p2_1", "objectId": "comp_marker", "type": "translate", "start": 6.5, "end": 7, "params": {"to": {"x": 200, "y": 360}}, "narrative": "Pass 2. Compare 3 and 5. No swap."},
        
        # 5 vs 1
        {"id": "p2_2", "objectId": "comp_marker", "type": "translate", "start": 7.5, "end": 8, "params": {"to": {"x": 260, "y": 360}}, "narrative": "Compare 5 and 1. Swap."},
        {"id": "p2_2_s1", "objectId": "bar1", "type": "translate", "start": 8, "end": 8.5, "params": {"to": {"x": 320, "y": 350}}},
        {"id": "p2_2_s2", "objectId": "bar4", "type": "translate", "start": 8, "end": 8.5, "params": {"to": {"x": 260, "y": 350}}},
        
        # 5 vs 4
        {"id": "p2_3", "objectId": "comp_marker", "type": "translate", "start": 9, "end": 9.5, "params": {"to": {"x": 320, "y": 360}}, "narrative": "Compare 5 and 4. Swap."},
        {"id": "p2_3_s1", "objectId": "bar1", "type": "translate", "start": 9.5, "end": 10, "params": {"to": {"x": 380, "y": 350}}},
        {"id": "p2_3_s2", "objectId": "bar5", "type": "translate", "start": 9.5, "end": 10, "params": {"to": {"x": 320, "y": 350}}},
        
        {"id": "p2_done", "objectId": "bar1", "type": "fade", "start": 10, "end": 10.5, "params": {"opacity": 0.5}, "narrative": "5 is sorted."},

        # --- PASS 3 ---
        # 3 vs 1
        {"id": "p3_1", "objectId": "comp_marker", "type": "translate", "start": 11, "end": 11.5, "params": {"to": {"x": 200, "y": 360}}, "narrative": "Pass 3. Compare 3 and 1. Swap."},
        {"id": "p3_1_s1", "objectId": "bar2", "type": "translate", "start": 11.5, "end": 12, "params": {"to": {"x": 260, "y": 350}}},
        {"id": "p3_1_s2", "objectId": "bar4", "type": "translate", "start": 11.5, "end": 12, "params": {"to": {"x": 200, "y": 350}}},
        
        # 3 vs 4
        {"id": "p3_2", "objectId": "comp_marker", "type": "translate", "start": 12.5, "end": 13, "params": {"to": {"x": 260, "y": 360}}, "narrative": "Compare 3 and 4. No swap."},
        
        {"id": "p3_done", "objectId": "bar5", "type": "fade", "start": 13, "end": 13.5, "params": {"opacity": 0.5}, "narrative": "4 is sorted."},

        # --- PASS 4 ---
        # 1 vs 3
        {"id": "p4_1", "objectId": "comp_marker", "type": "translate", "start": 14, "end": 14.5, "params": {"to": {"x": 200, "y": 360}}, "narrative": "Pass 4. Compare 1 and 3. No swap."},
        
        {"id": "p4_done", "objectId": "bar2", "type": "fade", "start": 14.5, "end": 15, "params": {"opacity": 0.5}, "narrative": "3 is sorted."},
        {"id": "p5_done", "objectId": "bar4", "type": "fade", "start": 15, "end": 15.5, "params": {"opacity": 0.5}, "narrative": "1 is sorted. Done!"},
        
        {"id": "hide_marker", "objectId": "comp_marker", "type": "fade", "start": 16, "end": 16.5, "params": {"opacity": 0}}
    ]
}

TEMPLATE_SELECTION_SORT = {
    "sceneId": "selection_sort",
    "width": 800,
    "height": 450,
    "duration": 20,
    "code": "def selection_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i+1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Selection Sort: [5, 3, 8, 1, 4]", "font": "bold 28px Arial", "color": "#89b4fa"}},
        
        # Bars
        {"id": "bar0", "type": "bar", "props": {"x": 200, "y": 350, "width": 40, "height": 150, "color": "#f38ba8", "text": "5"}},
        {"id": "bar1", "type": "bar", "props": {"x": 260, "y": 350, "width": 40, "height": 90, "color": "#fab387", "text": "3"}},
        {"id": "bar2", "type": "bar", "props": {"x": 320, "y": 350, "width": 40, "height": 240, "color": "#a6e3a1", "text": "8"}},
        {"id": "bar3", "type": "bar", "props": {"x": 380, "y": 350, "width": 40, "height": 30, "color": "#89b4fa", "text": "1"}},
        {"id": "bar4", "type": "bar", "props": {"x": 440, "y": 350, "width": 40, "height": 120, "color": "#cba6f7", "text": "4"}},
        
        # Indicators
        {"id": "min_marker", "type": "text", "props": {"x": 200, "y": 380, "text": "Min", "font": "bold 16px Arial", "color": "#f9e2af", "opacity": 0}},
        {"id": "scan_marker", "type": "rect", "props": {"x": 200, "y": 360, "width": 40, "height": 5, "color": "#fff", "opacity": 0}}
    ],
    "actions": [
        # --- PASS 0 (Find min for index 0) ---
        {"id": "p0_start", "objectId": "min_marker", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}, "narrative": "Pass 0. Assume 5 is min."},
        {"id": "p0_scan1", "objectId": "scan_marker", "type": "translate", "start": 1, "end": 1.5, "params": {"to": {"x": 260, "y": 360}}, "narrative": "Check 3. 3 < 5, new min."},
        {"id": "p0_upd1", "objectId": "min_marker", "type": "translate", "start": 1.5, "end": 2, "params": {"to": {"x": 260, "y": 380}}},
        
        {"id": "p0_scan2", "objectId": "scan_marker", "type": "translate", "start": 2, "end": 2.5, "params": {"to": {"x": 320, "y": 360}}, "narrative": "Check 8. Ignore."},
        
        {"id": "p0_scan3", "objectId": "scan_marker", "type": "translate", "start": 2.5, "end": 3, "params": {"to": {"x": 380, "y": 360}}, "narrative": "Check 1. 1 < 3, new min."},
        {"id": "p0_upd2", "objectId": "min_marker", "type": "translate", "start": 3, "end": 3.5, "params": {"to": {"x": 380, "y": 380}}},
        
        {"id": "p0_scan4", "objectId": "scan_marker", "type": "translate", "start": 3.5, "end": 4, "params": {"to": {"x": 440, "y": 360}}, "narrative": "Check 4. Ignore."},
        
        {"id": "p0_swap", "objectId": "bar0", "type": "translate", "start": 4.5, "end": 5.5, "params": {"to": {"x": 380, "y": 350}}, "narrative": "Swap 1 and 5. 1 is sorted."},
        {"id": "p0_swap_b", "objectId": "bar3", "type": "translate", "start": 4.5, "end": 5.5, "params": {"to": {"x": 200, "y": 350}}},
        {"id": "p0_done", "objectId": "bar3", "type": "fade", "start": 5.5, "end": 6, "params": {"opacity": 0.5}}, # 1 (bar3) is now at pos 0

        # --- PASS 1 (Find min for index 1) ---
        {"id": "p1_start", "objectId": "min_marker", "type": "translate", "start": 6, "end": 6.5, "params": {"to": {"x": 260, "y": 380}}, "narrative": "Pass 1. Assume 3 is min."},
        {"id": "p1_scan1", "objectId": "scan_marker", "type": "translate", "start": 6.5, "end": 7, "params": {"to": {"x": 320, "y": 360}}, "narrative": "Check 8. Ignore."},
        {"id": "p1_scan2", "objectId": "scan_marker", "type": "translate", "start": 7, "end": 7.5, "params": {"to": {"x": 380, "y": 360}}, "narrative": "Check 5. Ignore."},
        {"id": "p1_scan3", "objectId": "scan_marker", "type": "translate", "start": 7.5, "end": 8, "params": {"to": {"x": 440, "y": 360}}, "narrative": "Check 4. Ignore."},
        
        {"id": "p1_done", "objectId": "bar1", "type": "fade", "start": 8.5, "end": 9, "params": {"opacity": 0.5}, "narrative": "3 is already in place."},

        # --- PASS 2 (Find min for index 2) ---
        {"id": "p2_start", "objectId": "min_marker", "type": "translate", "start": 9, "end": 9.5, "params": {"to": {"x": 320, "y": 380}}, "narrative": "Pass 2. Assume 8 is min."},
        {"id": "p2_scan1", "objectId": "scan_marker", "type": "translate", "start": 9.5, "end": 10, "params": {"to": {"x": 380, "y": 360}}, "narrative": "Check 5. 5 < 8, new min."},
        {"id": "p2_upd1", "objectId": "min_marker", "type": "translate", "start": 10, "end": 10.5, "params": {"to": {"x": 380, "y": 380}}},
        
        {"id": "p2_scan2", "objectId": "scan_marker", "type": "translate", "start": 10.5, "end": 11, "params": {"to": {"x": 440, "y": 360}}, "narrative": "Check 4. 4 < 5, new min."},
        {"id": "p2_upd2", "objectId": "min_marker", "type": "translate", "start": 11, "end": 11.5, "params": {"to": {"x": 440, "y": 380}}},
        
        {"id": "p2_swap", "objectId": "bar2", "type": "translate", "start": 12, "end": 13, "params": {"to": {"x": 440, "y": 350}}, "narrative": "Swap 4 and 8. 4 is sorted."},
        {"id": "p2_swap_b", "objectId": "bar4", "type": "translate", "start": 12, "end": 13, "params": {"to": {"x": 320, "y": 350}}},
        {"id": "p2_done", "objectId": "bar4", "type": "fade", "start": 13, "end": 13.5, "params": {"opacity": 0.5}}, # 4 (bar4) is now at pos 2

        # --- PASS 3 (Find min for index 3) ---
        {"id": "p3_start", "objectId": "min_marker", "type": "translate", "start": 13.5, "end": 14, "params": {"to": {"x": 380, "y": 380}}, "narrative": "Pass 3. Assume 5 is min."},
        {"id": "p3_scan1", "objectId": "scan_marker", "type": "translate", "start": 14, "end": 14.5, "params": {"to": {"x": 440, "y": 360}}, "narrative": "Check 8. Ignore."},
        
        {"id": "p3_done", "objectId": "bar0", "type": "fade", "start": 15, "end": 15.5, "params": {"opacity": 0.5}, "narrative": "5 is sorted."},
        {"id": "p4_done", "objectId": "bar2", "type": "fade", "start": 15.5, "end": 16, "params": {"opacity": 0.5}, "narrative": "8 is sorted. Done!"},
        
        {"id": "hide_min", "objectId": "min_marker", "type": "fade", "start": 16, "end": 16.5, "params": {"opacity": 0}},
        {"id": "hide_scan", "objectId": "scan_marker", "type": "fade", "start": 16, "end": 16.5, "params": {"opacity": 0}}
    ]
}

TEMPLATE_SOLAR_SYSTEM = {
    "sceneId": "solar_system",
    "width": 800,
    "height": 450,
    "duration": 12,
    "code": "# Solar System Simulation\n# Planets orbit the Sun\n# Mercury (Fast), Venus, Earth, Mars (Slow)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#000000"}},
        {"id": "sun", "type": "sphere", "props": {"x": 400, "y": 225, "r": 30, "color": "#f1c40f", "color2": "#e67e22"}},
        
        # Orbits (Visual lines)
        {"id": "orbit_mercury_vis", "type": "path", "props": {"d": "M 400 225 m -50, 0 a 50,50 0 1,0 100,0 a 50,50 0 1,0 -100,0", "color": "#333", "width": 1}},
        {"id": "orbit_venus_vis", "type": "path", "props": {"d": "M 400 225 m -80, 0 a 80,80 0 1,0 160,0 a 80,80 0 1,0 -160,0", "color": "#333", "width": 1}},
        {"id": "orbit_earth_vis", "type": "path", "props": {"d": "M 400 225 m -110, 0 a 110,110 0 1,0 220,0 a 110,110 0 1,0 -220,0", "color": "#333", "width": 1}},
        {"id": "orbit_mars_vis", "type": "path", "props": {"d": "M 400 225 m -140, 0 a 140,140 0 1,0 280,0 a 140,140 0 1,0 -280,0", "color": "#333", "width": 1}},

        # Motion Paths (Hidden logic for animation - Multi-loop for speed)
        # Mercury: 4 loops
        {"id": "orbit_mercury", "type": "path", "props": {"d": "M 400 225 m -50, 0 a 50,50 0 1,0 100,0 a 50,50 0 1,0 -100,0 a 50,50 0 1,0 100,0 a 50,50 0 1,0 -100,0 a 50,50 0 1,0 100,0 a 50,50 0 1,0 -100,0 a 50,50 0 1,0 100,0 a 50,50 0 1,0 -100,0", "color": "none", "width": 0, "opacity": 0}},
        # Venus: 2 loops
        {"id": "orbit_venus", "type": "path", "props": {"d": "M 400 225 m -80, 0 a 80,80 0 1,0 160,0 a 80,80 0 1,0 -160,0 a 80,80 0 1,0 160,0 a 80,80 0 1,0 -160,0", "color": "none", "width": 0, "opacity": 0}},
        # Earth: 1 loop
        {"id": "orbit_earth", "type": "path", "props": {"d": "M 400 225 m -110, 0 a 110,110 0 1,0 220,0 a 110,110 0 1,0 -220,0", "color": "none", "width": 0, "opacity": 0}},
        # Mars: 1 loop (but we will animate it slower effectively by using full duration for 1 loop vs others)
        # Actually, to make it slower than Earth, Earth should do e.g. 2 loops and Mars 1 loop? 
        # Let's stick to: Mercury=4, Venus=2, Earth=1.2, Mars=0.8?
        # Simplified: Mercury=4, Venus=2, Earth=1, Mars=0.5 (half circle)
        {"id": "orbit_mars", "type": "path", "props": {"d": "M 400 225 m -140, 0 a 140,140 0 1,0 280,0", "color": "none", "width": 0, "opacity": 0}},
        
        # Planets
        {"id": "mercury", "type": "sphere", "props": {"x": 350, "y": 225, "r": 6, "color": "#bdc3c7", "color2": "#95a5a6"}},
        {"id": "venus", "type": "sphere", "props": {"x": 320, "y": 225, "r": 10, "color": "#e67e22", "color2": "#d35400"}},
        {"id": "earth", "type": "sphere", "props": {"x": 290, "y": 225, "r": 11, "color": "#3498db", "color2": "#2980b9"}},
        {"id": "mars", "type": "sphere", "props": {"x": 260, "y": 225, "r": 8, "color": "#c0392b", "color2": "#e74c3c"}},
        
        {"id": "label", "type": "text", "props": {"x": 400, "y": 420, "text": "The Solar System", "font": "24px Arial", "color": "#fff", "opacity": 0}}
    ],
    "actions": [
        {"id": "anim_mercury", "objectId": "mercury", "type": "followPath", "start": 0, "end": 12, "params": {"pathId": "orbit_mercury"}},
        {"id": "anim_venus", "objectId": "venus", "type": "followPath", "start": 0, "end": 12, "params": {"pathId": "orbit_venus"}},
        {"id": "anim_earth", "objectId": "earth", "type": "followPath", "start": 0, "end": 12, "params": {"pathId": "orbit_earth"}},
        {"id": "anim_mars", "objectId": "mars", "type": "followPath", "start": 0, "end": 12, "params": {"pathId": "orbit_mars"}},
        {"id": "show_label", "objectId": "label", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}}
    ]
}

TEMPLATE_DNA = {
    "sceneId": "dna_helix",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "# DNA Double Helix\n# Genetic information storage",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#101020"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "DNA Double Helix", "font": "bold 28px Arial", "color": "#a29bfe"}},
        
        # Strand 1
        {"id": "strand1", "type": "path", "props": {"d": "M 50 225 Q 150 100 250 225 T 450 225 T 650 225", "color": "#e84393", "width": 5}},
        # Strand 2 (Phase shifted)
        {"id": "strand2", "type": "path", "props": {"d": "M 50 225 Q 150 350 250 225 T 450 225 T 650 225", "color": "#0984e3", "width": 5}},
        
        # Base Pairs
        {"id": "bp1", "type": "rect", "props": {"x": 150, "y": 160, "width": 4, "height": 130, "color": "#fff", "opacity": 0}},
        {"id": "bp2", "type": "rect", "props": {"x": 350, "y": 160, "width": 4, "height": 130, "color": "#fff", "opacity": 0}},
        {"id": "bp3", "type": "rect", "props": {"x": 550, "y": 160, "width": 4, "height": 130, "color": "#fff", "opacity": 0}}
    ],
    "actions": [
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0, "end": 1, "params": {"opacity": 1}},
        {"id": "reveal_s1", "objectId": "strand1", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "DNA consists of two strands forming a double helix."},
        {"id": "reveal_s2", "objectId": "strand2", "type": "fade", "start": 1.5, "end": 2.5, "params": {"opacity": 1}},
        {"id": "reveal_bp1", "objectId": "bp1", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 0.3}, "narrative": "Connected by base pairs."},
        {"id": "reveal_bp2", "objectId": "bp2", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 0.3}},
        {"id": "reveal_bp3", "objectId": "bp3", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.3}}
    ]
}

TEMPLATE_QUADRATIC = {
    "sceneId": "quadratic_roots",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "y = x^2 - 4\n# Roots at x = -2, x = 2",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "grid", "type": "axis", "props": {"x": 400, "y": 225, "width": 300, "height": 300, "color": "#45475a"}}, 
        {"id": "curve", "type": "path", "props": {"d": "M 240 25 Q 400 545 560 25", "color": "#f38ba8", "width": 3, "opacity": 0}},
        {"id": "root1", "type": "circle", "props": {"x": 320, "y": 225, "r": 6, "color": "#a6e3a1", "opacity": 0}},
        {"id": "root2", "type": "circle", "props": {"x": 480, "y": 225, "r": 6, "color": "#a6e3a1", "opacity": 0}},
        {"id": "eq", "type": "text", "props": {"x": 600, "y": 100, "text": "y = x² - 4", "font": "24px monospace", "color": "#f38ba8", "opacity": 0}},
        {"id": "roots_txt", "type": "text", "props": {"x": 600, "y": 140, "text": "Roots: x = ±2", "font": "20px monospace", "color": "#a6e3a1", "opacity": 0}}
    ],
    "actions": [
        {"id": "draw_curve", "objectId": "curve", "type": "fade", "start": 0.5, "end": 2, "params": {"opacity": 1}, "narrative": "Graph of y equals x squared minus 4."},
        {"id": "show_eq", "objectId": "eq", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}},
        {"id": "show_roots", "objectId": "root1", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "The curve intersects the x-axis at -2 and 2."},
        {"id": "show_roots2", "objectId": "root2", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}},
        {"id": "txt_roots", "objectId": "roots_txt", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}}
    ]
}

TEMPLATE_DOT_PRODUCT = {
    "sceneId": "dot_product",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "A . B = |A||B|cos(θ)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#ffffff"}},
        {"id": "vec_a", "type": "arrow", "props": {"x": 100, "y": 350, "width": 4, "color": "#3498db", "points": [100, 350, 400, 350]}},
        {"id": "vec_b", "type": "arrow", "props": {"x": 100, "y": 350, "width": 4, "color": "#e74c3c", "points": [100, 350, 250, 200]}},
        {"id": "proj_line", "type": "path", "props": {"d": "M 250 200 L 250 350", "color": "#999", "width": 2, "opacity": 0}},
        {"id": "proj_vec", "type": "rect", "props": {"x": 100, "y": 352, "width": 150, "height": 4, "color": "#f1c40f", "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 100, "text": "Dot Product = Projection * Base", "font": "24px Arial", "color": "#333", "opacity": 0}}
    ],
    "actions": [
        {"id": "show_proj", "objectId": "proj_line", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "Project Vector B onto Vector A."},
        {"id": "highlight_proj", "objectId": "proj_vec", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "The yellow segment is the projection."},
        {"id": "show_text", "objectId": "label", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}}
    ]
}

TEMPLATE_PIE_CHART = {
    "sceneId": "pie_chart",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "data = [30, 50, 20]",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Market Share", "font": "bold 28px Arial", "color": "#cdd6f4"}},
        {"id": "slice1", "type": "path", "props": {"d": "M 400 250 L 400 100 A 150 150 0 0 1 400 400 Z", "color": "#f38ba8", "opacity": 0}},
        {"id": "slice2", "type": "path", "props": {"d": "M 400 250 L 400 400 A 150 150 0 0 1 257 297 Z", "color": "#89b4fa", "opacity": 0}},
        {"id": "slice3", "type": "path", "props": {"d": "M 400 250 L 257 297 A 150 150 0 0 1 400 100 Z", "color": "#a6e3a1", "opacity": 0}},
        {"id": "legend1", "type": "text", "props": {"x": 600, "y": 200, "text": "Product A: 50%", "font": "20px Arial", "color": "#f38ba8", "opacity": 0}},
        {"id": "legend2", "type": "text", "props": {"x": 600, "y": 240, "text": "Product B: 30%", "font": "20px Arial", "color": "#89b4fa", "opacity": 0}},
        {"id": "legend3", "type": "text", "props": {"x": 600, "y": 280, "text": "Product C: 20%", "font": "20px Arial", "color": "#a6e3a1", "opacity": 0}}
    ],
    "actions": [
        {"id": "s1", "objectId": "slice1", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "Product A dominates with 50%."},
        {"id": "l1", "objectId": "legend1", "type": "fade", "start": 1, "end": 1.5, "params": {"opacity": 1}},
        {"id": "s2", "objectId": "slice2", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "Product B follows with 30%."},
        {"id": "l2", "objectId": "legend2", "type": "fade", "start": 2.5, "end": 3, "params": {"opacity": 1}},
        {"id": "s3", "objectId": "slice3", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 1}, "narrative": "Product C has 20%."},
        {"id": "l3", "objectId": "legend3", "type": "fade", "start": 4, "end": 4.5, "params": {"opacity": 1}}
    ]
}

TEMPLATE_ALGEBRA = {
    "sceneId": "algebra_sq",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "(a + b)^2 = a^2 + 2ab + b^2",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#ffffff"}},
        {"id": "sq_a", "type": "rect", "props": {"x": 300, "y": 100, "width": 100, "height": 100, "color": "#3498db", "opacity": 0}},
        {"id": "rect_ab1", "type": "rect", "props": {"x": 400, "y": 100, "width": 50, "height": 100, "color": "#e74c3c", "opacity": 0}},
        {"id": "rect_ab2", "type": "rect", "props": {"x": 300, "y": 200, "width": 100, "height": 50, "color": "#e74c3c", "opacity": 0}},
        {"id": "sq_b", "type": "rect", "props": {"x": 400, "y": 200, "width": 50, "height": 50, "color": "#f1c40f", "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 375, "y": 300, "text": "(a + b)² = a² + 2ab + b²", "font": "24px Arial", "color": "#333", "opacity": 0}}
    ],
    "actions": [
        {"id": "show_a", "objectId": "sq_a", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "This is a squared."},
        {"id": "show_ab", "objectId": "rect_ab1", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "Add a times b."},
        {"id": "show_ab2", "objectId": "rect_ab2", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Add another a times b."},
        {"id": "show_b", "objectId": "sq_b", "type": "fade", "start": 4.5, "end": 5.5, "params": {"opacity": 1}, "narrative": "Finally, add b squared."},
        {"id": "show_eq", "objectId": "label", "type": "fade", "start": 6, "end": 7, "params": {"opacity": 1}}
    ]
}

TEMPLATE_STACK = {
    "sceneId": "stack_ops",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "stack = []\nstack.push(1)\nstack.push(2)\nstack.pop()",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "container", "type": "axis", "props": {"x": 350, "y": 150, "width": 100, "height": 200, "color": "#cdd6f4"}},
        {"id": "item1", "type": "rect", "props": {"x": 360, "y": 50, "width": 80, "height": 40, "color": "#f38ba8", "opacity": 0}},
        {"id": "item2", "type": "rect", "props": {"x": 360, "y": 50, "width": 80, "height": 40, "color": "#89b4fa", "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 400, "text": "Stack Operations", "font": "24px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "push1_appear", "objectId": "item1", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}, "narrative": "Push element 1."},
        {"id": "push1_move", "objectId": "item1", "type": "translate", "start": 1, "end": 2, "params": {"to": {"x": 360, "y": 300}}},
        {"id": "push2_appear", "objectId": "item2", "type": "fade", "start": 2.5, "end": 3, "params": {"opacity": 1}, "narrative": "Push element 2."},
        {"id": "push2_move", "objectId": "item2", "type": "translate", "start": 3, "end": 4, "params": {"to": {"x": 360, "y": 250}}},
        {"id": "pop2_move", "objectId": "item2", "type": "translate", "start": 5, "end": 6, "params": {"to": {"x": 360, "y": 50}}, "narrative": "Pop element 2 (LIFO)."},
        {"id": "pop2_fade", "objectId": "item2", "type": "fade", "start": 6, "end": 6.5, "params": {"opacity": 0}}
    ]
}

TEMPLATE_PHOTOSYNTHESIS = {
    "sceneId": "photosynthesis",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "6CO2 + 6H2O + Light -> C6H12O6 + 6O2",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#87CEEB"}},
        {"id": "sun", "type": "circle", "props": {"x": 100, "y": 80, "r": 40, "color": "#f1c40f"}},
        {"id": "plant", "type": "rect", "props": {"x": 350, "y": 250, "width": 100, "height": 200, "color": "#2ecc71"}},
        {"id": "leaf", "type": "circle", "props": {"x": 400, "y": 250, "r": 60, "color": "#27ae60"}},
        {"id": "arrow_light", "type": "arrow", "props": {"x": 140, "y": 100, "width": 3, "color": "#f1c40f", "points": [140, 100, 350, 250], "opacity": 0}},
        {"id": "txt_co2", "type": "text", "props": {"x": 250, "y": 300, "text": "CO2", "font": "20px Arial", "color": "#333", "opacity": 0}},
        {"id": "txt_h2o", "type": "text", "props": {"x": 400, "y": 440, "text": "H2O", "font": "20px Arial", "color": "#0000ff", "opacity": 0}},
        {"id": "txt_o2", "type": "text", "props": {"x": 550, "y": 250, "text": "O2", "font": "20px Arial", "color": "#333", "opacity": 0}},
        {"id": "txt_sugar", "type": "text", "props": {"x": 400, "y": 350, "text": "Sugar", "font": "20px Arial", "color": "#fff", "opacity": 0}}
    ],
    "actions": [
        {"id": "light", "objectId": "arrow_light", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "Sunlight provides energy."},
        {"id": "co2", "objectId": "txt_co2", "type": "translate", "start": 2, "end": 3, "params": {"to": {"x": 350, "y": 280}}, "narrative": "Carbon dioxide enters from the air."},
        {"id": "show_co2", "objectId": "txt_co2", "type": "fade", "start": 2, "end": 2.5, "params": {"opacity": 1}},
        {"id": "h2o", "objectId": "txt_h2o", "type": "translate", "start": 3.5, "end": 4.5, "params": {"to": {"x": 400, "y": 380}}, "narrative": "Water is absorbed by roots."},
        {"id": "show_h2o", "objectId": "txt_h2o", "type": "fade", "start": 3.5, "end": 4, "params": {"opacity": 1}},
        {"id": "o2", "objectId": "txt_o2", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}, "narrative": "Oxygen is released."},
        {"id": "sugar", "objectId": "txt_sugar", "type": "fade", "start": 6.5, "end": 7.5, "params": {"opacity": 1}, "narrative": "Glucose (sugar) is produced."}
    ]
}

TEMPLATE_LIMIT = {
    "sceneId": "limit_calc",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "f(x) = sin(x) / x\nlim(x->0) f(x) = 1",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "axis", "type": "axis", "props": {"x": 50, "y": 225, "width": 700, "height": 400, "color": "#45475a"}},
        {"id": "curve", "type": "path", "props": {"d": "M 50 400 Q 200 400 400 50 Q 600 400 750 400", "color": "#f38ba8", "width": 3}}, 
        {"id": "hole", "type": "circle", "props": {"x": 400, "y": 50, "r": 6, "color": "#1e1e2e", "color2": "#f38ba8"}}, 
        {"id": "point_l", "type": "circle", "props": {"x": 100, "y": 350, "r": 6, "color": "#89b4fa", "opacity": 0}},
        {"id": "point_r", "type": "circle", "props": {"x": 700, "y": 350, "r": 6, "color": "#89b4fa", "opacity": 0}},
        {"id": "val_txt", "type": "text", "props": {"x": 450, "y": 50, "text": "y -> 1", "font": "20px monospace", "color": "#fff", "opacity": 0}}
    ],
    "actions": [
        {"id": "show_pts", "objectId": "point_l", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}, "narrative": "Consider points approaching x=0 from both sides."},
        {"id": "show_pts2", "objectId": "point_r", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}},
        {"id": "move_l", "objectId": "point_l", "type": "translate", "start": 1, "end": 4, "params": {"to": {"x": 390, "y": 55}}},
        {"id": "move_r", "objectId": "point_r", "type": "translate", "start": 1, "end": 4, "params": {"to": {"x": 410, "y": 55}}},
        {"id": "show_lim", "objectId": "val_txt", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}, "narrative": "As x approaches 0, the value approaches 1."}
    ]
}

TEMPLATE_CROSS_PRODUCT = {
    "sceneId": "cross_product",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "C = A x B\n# C is perpendicular to A and B",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#fff"}},
        {"id": "vec_a", "type": "arrow", "props": {"x": 400, "y": 300, "width": 5, "color": "#e74c3c", "points": [400, 300, 550, 350]}}, 
        {"id": "vec_b", "type": "arrow", "props": {"x": 400, "y": 300, "width": 5, "color": "#3498db", "points": [400, 300, 300, 400]}}, 
        {"id": "vec_c", "type": "arrow", "props": {"x": 400, "y": 300, "width": 5, "color": "#2ecc71", "points": [400, 300, 400, 300], "opacity": 0}}, 
        {"id": "label", "type": "text", "props": {"x": 420, "y": 150, "text": "C = A x B", "font": "24px Arial", "color": "#2ecc71", "opacity": 0}}
    ],
    "actions": [
        {"id": "grow_c", "objectId": "vec_c", "type": "translate", "start": 1, "end": 3, "params": {"to": {"points": [400, 300, 400, 100]}}, "narrative": "The cross product vector is perpendicular to the plane of A and B."}, 
        {"id": "show_lbl", "objectId": "label", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}}
    ]
}

TEMPLATE_BAR_RACE = {
    "sceneId": "bar_race",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "# Dynamic Data Visualization\n# Values change over time",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "axis", "type": "axis", "props": {"x": 100, "y": 400, "width": 600, "height": 350, "color": "#cdd6f4"}},
        {"id": "bar1", "type": "bar", "props": {"x": 150, "y": 400, "width": 50, "height": 100, "color": "#f38ba8", "text": "A"}},
        {"id": "bar2", "type": "bar", "props": {"x": 250, "y": 400, "width": 50, "height": 200, "color": "#fab387", "text": "B"}},
        {"id": "bar3", "type": "bar", "props": {"x": 350, "y": 400, "width": 50, "height": 150, "color": "#a6e3a1", "text": "C"}},
        {"id": "bar4", "type": "bar", "props": {"x": 450, "y": 400, "width": 50, "height": 50, "color": "#89b4fa", "text": "D"}},
        {"id": "year", "type": "text", "props": {"x": 650, "y": 100, "text": "2020", "font": "bold 40px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "y1", "objectId": "year", "type": "fade", "start": 0, "end": 0.1, "params": {"opacity": 1}},
        {"id": "grow1", "objectId": "bar1", "type": "scale", "start": 1, "end": 3, "params": {"scale": 2.5}, "narrative": "Over time, category A grows rapidly."}, 
        {"id": "shrink2", "objectId": "bar2", "type": "scale", "start": 1, "end": 3, "params": {"scale": 0.8}}, 
        {"id": "grow4", "objectId": "bar4", "type": "scale", "start": 1, "end": 3, "params": {"scale": 4}}, 
        {"id": "hide_2020", "objectId": "year", "type": "fade", "start": 2.8, "end": 3, "params": {"opacity": 0}},
        {"id": "grow1_2", "objectId": "bar1", "type": "scale", "start": 4, "end": 6, "params": {"scale": 1.2}}, 
        {"id": "grow3", "objectId": "bar3", "type": "scale", "start": 4, "end": 6, "params": {"scale": 2}}, 
    ]
}

TEMPLATE_INTEGRAL = {
    "sceneId": "integral_riemann",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "Area = Integral(f(x) dx)\n# Approximated by Riemann Sums",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#fff"}},
        {"id": "curve", "type": "path", "props": {"d": "M 100 350 Q 250 50 400 350", "color": "#333", "width": 2}},
        {"id": "r1", "type": "rect", "props": {"x": 100, "y": 350, "width": 60, "height": 100, "color": "rgba(52, 152, 219, 0.5)", "opacity": 0}},
        {"id": "r2", "type": "rect", "props": {"x": 160, "y": 350, "width": 60, "height": 180, "color": "rgba(52, 152, 219, 0.5)", "opacity": 0}},
        {"id": "r3", "type": "rect", "props": {"x": 220, "y": 350, "width": 60, "height": 220, "color": "rgba(52, 152, 219, 0.5)", "opacity": 0}},
        {"id": "r4", "type": "rect", "props": {"x": 280, "y": 350, "width": 60, "height": 180, "color": "rgba(52, 152, 219, 0.5)", "opacity": 0}},
        {"id": "r5", "type": "rect", "props": {"x": 340, "y": 350, "width": 60, "height": 100, "color": "rgba(52, 152, 219, 0.5)", "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 250, "y": 400, "text": "Area ≈ Sum(Rectangles)", "font": "20px Arial", "color": "#333"}}
    ],
    "actions": [
        {"id": "show_r1", "objectId": "r1", "type": "fade", "start": 1, "end": 1.5, "params": {"opacity": 1}, "narrative": "We can approximate the area under the curve..."},
        {"id": "show_r2", "objectId": "r2", "type": "fade", "start": 1.5, "end": 2, "params": {"opacity": 1}},
        {"id": "show_r3", "objectId": "r3", "type": "fade", "start": 2, "end": 2.5, "params": {"opacity": 1}, "narrative": "...by summing the areas of these rectangles."},
        {"id": "show_r4", "objectId": "r4", "type": "fade", "start": 2.5, "end": 3, "params": {"opacity": 1}},
        {"id": "show_r5", "objectId": "r5", "type": "fade", "start": 3, "end": 3.5, "params": {"opacity": 1}}
    ]
}

TEMPLATE_QUEUE = {
    "sceneId": "queue_ops",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "queue = []\nqueue.enqueue(1)\nqueue.enqueue(2)\nqueue.dequeue()",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "top_line", "type": "rect", "props": {"x": 100, "y": 180, "width": 600, "height": 2, "color": "#cdd6f4"}},
        {"id": "bot_line", "type": "rect", "props": {"x": 100, "y": 270, "width": 600, "height": 2, "color": "#cdd6f4"}},
        {"id": "item1", "type": "rect", "props": {"x": 750, "y": 200, "width": 50, "height": 50, "color": "#a6e3a1", "opacity": 0}},
        {"id": "item2", "type": "rect", "props": {"x": 750, "y": 200, "width": 50, "height": 50, "color": "#f9e2af", "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 100, "text": "Queue (FIFO)", "font": "24px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "enq1_show", "objectId": "item1", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}, "narrative": "Enqueue 1. Enters from the rear."},
        {"id": "enq1_move", "objectId": "item1", "type": "translate", "start": 1, "end": 2.5, "params": {"to": {"x": 150, "y": 200}}}, 
        {"id": "enq2_show", "objectId": "item2", "type": "fade", "start": 3, "end": 3.5, "params": {"opacity": 1}, "narrative": "Enqueue 2."},
        {"id": "enq2_move", "objectId": "item2", "type": "translate", "start": 3.5, "end": 5, "params": {"to": {"x": 210, "y": 200}}}, 
        {"id": "deq1_move", "objectId": "item1", "type": "translate", "start": 6, "end": 7, "params": {"to": {"x": 50, "y": 200}}, "narrative": "Dequeue. Element 1 leaves from the front."},
        {"id": "deq1_fade", "objectId": "item1", "type": "fade", "start": 7, "end": 7.5, "params": {"opacity": 0}},
        {"id": "shift2", "objectId": "item2", "type": "translate", "start": 7.5, "end": 8.5, "params": {"to": {"x": 150, "y": 200}}, "narrative": "Remaining elements shift forward."}
    ]
}

TEMPLATE_WATER_CYCLE = {
    "sceneId": "water_cycle",
    "width": 800,
    "height": 450,
    "duration": 12,
    "code": "Cycle: Evaporation -> Condensation -> Precipitation",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#87CEEB"}},
        {"id": "ocean", "type": "rect", "props": {"x": 0, "y": 350, "width": 800, "height": 100, "color": "#2980b9"}},
        {"id": "sun", "type": "circle", "props": {"x": 700, "y": 80, "r": 50, "color": "#f1c40f"}},
        {"id": "vapor1", "type": "circle", "props": {"x": 200, "y": 350, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "vapor2", "type": "circle", "props": {"x": 250, "y": 360, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "vapor3", "type": "circle", "props": {"x": 300, "y": 350, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "cloud", "type": "circle", "props": {"x": 250, "y": 100, "r": 40, "color": "#fff", "opacity": 0}},
        {"id": "cloud2", "type": "circle", "props": {"x": 290, "y": 100, "r": 50, "color": "#fff", "opacity": 0}},
        {"id": "rain1", "type": "rect", "props": {"x": 250, "y": 150, "width": 2, "height": 10, "color": "#0000ff", "opacity": 0}},
        {"id": "rain2", "type": "rect", "props": {"x": 280, "y": 160, "width": 2, "height": 10, "color": "#0000ff", "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 50, "text": "The Water Cycle", "font": "24px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "evap1", "objectId": "vapor1", "type": "translate", "start": 1, "end": 4, "params": {"to": {"x": 200, "y": 150}}, "narrative": "Evaporation: Water turns into vapor due to heat."},
        {"id": "evap1_show", "objectId": "vapor1", "type": "fade", "start": 1, "end": 1.5, "params": {"opacity": 0.5}},
        {"id": "evap2", "objectId": "vapor2", "type": "translate", "start": 1.5, "end": 4.5, "params": {"to": {"x": 250, "y": 150}}},
        {"id": "evap2_show", "objectId": "vapor2", "type": "fade", "start": 1.5, "end": 2, "params": {"opacity": 0.5}},
        {"id": "condense", "objectId": "cloud", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.9}, "narrative": "Condensation: Vapor cools to form clouds."},
        {"id": "condense2", "objectId": "cloud2", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0.9}},
        {"id": "precip1", "objectId": "rain1", "type": "translate", "start": 6, "end": 8, "params": {"to": {"x": 250, "y": 350}}, "narrative": "Precipitation: Water falls back as rain."},
        {"id": "precip1_show", "objectId": "rain1", "type": "fade", "start": 6, "end": 6.5, "params": {"opacity": 1}},
        {"id": "precip2", "objectId": "rain2", "type": "translate", "start": 6.5, "end": 8.5, "params": {"to": {"x": 280, "y": 350}}},
        {"id": "precip2_show", "objectId": "rain2", "type": "fade", "start": 6.5, "end": 7, "params": {"opacity": 1}}
    ]
}

TEMPLATE_FOURIER = {
    "sceneId": "fourier_series",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "f(t) = sin(t) + 1/3 sin(3t) + ...",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "c1", "type": "circle", "props": {"x": 200, "y": 225, "r": 80, "color": "none", "color2": "#45475a"}}, # Orbit 1
        {"id": "l1", "type": "path", "props": {"d": "M 200 225 L 280 225", "color": "#f38ba8", "width": 2}}, # Radius 1
        {"id": "c2", "type": "circle", "props": {"x": 280, "y": 225, "r": 30, "color": "none", "color2": "#45475a"}}, # Orbit 2
        {"id": "l2", "type": "path", "props": {"d": "M 280 225 L 310 225", "color": "#89b4fa", "width": 2}}, # Radius 2
        {"id": "wave", "type": "path", "props": {"d": "M 400 225 Q 500 100 600 225 T 800 225", "color": "#a6e3a1", "width": 3, "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 400, "text": "Fourier Series: Sum of Circles", "font": "24px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "rot1", "objectId": "l1", "type": "rotate", "start": 0, "end": 10, "params": {"angle": 360}},
        {"id": "rot2", "objectId": "l2", "type": "rotate", "start": 0, "end": 10, "params": {"angle": 1080}}, # 3x speed
        {"id": "draw_wave", "objectId": "wave", "type": "fade", "start": 2, "end": 4, "params": {"opacity": 1}, "narrative": "Complex waves are sums of simple rotating vectors."}
    ]
}

TEMPLATE_VEC_SUB = {
    "sceneId": "vec_sub",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "R = A - B = A + (-B)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#fff"}},
        {"id": "vec_a", "type": "arrow", "props": {"x": 100, "y": 300, "width": 4, "color": "#3498db", "points": [100, 300, 300, 300]}},
        {"id": "vec_b", "type": "arrow", "props": {"x": 100, "y": 300, "width": 4, "color": "#e74c3c", "points": [100, 300, 200, 150]}},
        {"id": "vec_neg_b", "type": "arrow", "props": {"x": 300, "y": 300, "width": 4, "color": "#e74c3c", "points": [300, 300, 200, 450], "opacity": 0}}, # -B at tip of A
        {"id": "vec_r", "type": "arrow", "props": {"x": 100, "y": 300, "width": 4, "color": "#2ecc71", "points": [100, 300, 200, 450], "opacity": 0}},
        {"id": "label", "type": "text", "props": {"x": 400, "y": 50, "text": "Vector Subtraction", "font": "24px Arial", "color": "#333"}}
    ],
    "actions": [
        {"id": "show_neg", "objectId": "vec_neg_b", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "To subtract B, add negative B to the tip of A."},
        {"id": "show_res", "objectId": "vec_r", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}, "narrative": "The result is the vector from start to end."}
    ]
}

TEMPLATE_SCATTER = {
    "sceneId": "scatter_plot",
    "width": 800,
    "height": 450,
    "duration": 8,
    "code": "y = mx + c + noise",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "axis", "type": "axis", "props": {"x": 50, "y": 400, "width": 700, "height": 350, "color": "#cdd6f4"}},
        {"id": "p1", "type": "circle", "props": {"x": 100, "y": 350, "r": 4, "color": "#f38ba8", "opacity": 0}},
        {"id": "p2", "type": "circle", "props": {"x": 200, "y": 300, "r": 4, "color": "#f38ba8", "opacity": 0}},
        {"id": "p3", "type": "circle", "props": {"x": 300, "y": 280, "r": 4, "color": "#f38ba8", "opacity": 0}},
        {"id": "p4", "type": "circle", "props": {"x": 400, "y": 200, "r": 4, "color": "#f38ba8", "opacity": 0}},
        {"id": "p5", "type": "circle", "props": {"x": 500, "y": 150, "r": 4, "color": "#f38ba8", "opacity": 0}},
        {"id": "line", "type": "path", "props": {"d": "M 50 380 L 550 120", "color": "#a6e3a1", "width": 2, "opacity": 0}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Linear Regression", "font": "24px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "pts", "objectId": "p1", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}, "narrative": "Plotting data points..."},
        {"id": "pts2", "objectId": "p2", "type": "fade", "start": 0.8, "end": 1.3, "params": {"opacity": 1}},
        {"id": "pts3", "objectId": "p3", "type": "fade", "start": 1.1, "end": 1.6, "params": {"opacity": 1}},
        {"id": "pts4", "objectId": "p4", "type": "fade", "start": 1.4, "end": 1.9, "params": {"opacity": 1}},
        {"id": "pts5", "objectId": "p5", "type": "fade", "start": 1.7, "end": 2.2, "params": {"opacity": 1}},
        {"id": "fit", "objectId": "line", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Finding the line of best fit."}
    ]
}

TEMPLATE_CHAIN_RULE = {
    "sceneId": "chain_rule",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "d/dx f(g(x)) = f'(g(x)) * g'(x)",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#ffffff"}},
        {"id": "l1", "type": "text", "props": {"x": 400, "y": 150, "text": "d/dx f(g(x))", "font": "bold 32px Arial", "color": "#333", "opacity": 0}},
        {"id": "l2", "type": "text", "props": {"x": 400, "y": 250, "text": "= f'(g(x)) * g'(x)", "font": "bold 32px Arial", "color": "#e74c3c", "opacity": 0}},
        {"id": "note", "type": "text", "props": {"x": 400, "y": 350, "text": "Outer derivative times Inner derivative", "font": "20px Arial", "color": "#555", "opacity": 0}}
    ],
    "actions": [
        {"id": "s1", "objectId": "l1", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "Derivative of a composite function."},
        {"id": "s2", "objectId": "l2", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Apply the Chain Rule."},
        {"id": "s3", "objectId": "note", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}, "narrative": "Differentiate the outer, then multiply by the inner derivative."}
    ]
}

TEMPLATE_MERGE_SORT = {
    "sceneId": "merge_sort",
    "width": 800,
    "height": 450,
    "duration": 12,
    "code": "merge_sort([4, 2, 3, 1])",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "b1", "type": "bar", "props": {"x": 250, "y": 200, "width": 40, "height": 100, "color": "#f38ba8", "text": "4"}},
        {"id": "b2", "type": "bar", "props": {"x": 310, "y": 200, "width": 40, "height": 50, "color": "#fab387", "text": "2"}},
        {"id": "b3", "type": "bar", "props": {"x": 370, "y": 200, "width": 40, "height": 75, "color": "#a6e3a1", "text": "3"}},
        {"id": "b4", "type": "bar", "props": {"x": 430, "y": 200, "width": 40, "height": 25, "color": "#89b4fa", "text": "1"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Merge Sort", "font": "24px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "split", "objectId": "b1", "type": "translate", "start": 1, "end": 2, "params": {"to": {"x": 200, "y": 200}}, "narrative": "Divide into halves."},
        {"id": "split2", "objectId": "b2", "type": "translate", "start": 1, "end": 2, "params": {"to": {"x": 260, "y": 200}}},
        {"id": "split3", "objectId": "b3", "type": "translate", "start": 1, "end": 2, "params": {"to": {"x": 420, "y": 200}}},
        {"id": "split4", "objectId": "b4", "type": "translate", "start": 1, "end": 2, "params": {"to": {"x": 480, "y": 200}}},
        
        {"id": "swap1", "objectId": "b1", "type": "translate", "start": 3, "end": 4, "params": {"to": {"x": 260, "y": 200}}, "narrative": "Sort and merge sub-arrays."},
        {"id": "swap2", "objectId": "b2", "type": "translate", "start": 3, "end": 4, "params": {"to": {"x": 200, "y": 200}}},
        {"id": "swap3", "objectId": "b3", "type": "translate", "start": 3, "end": 4, "params": {"to": {"x": 480, "y": 200}}},
        {"id": "swap4", "objectId": "b4", "type": "translate", "start": 3, "end": 4, "params": {"to": {"x": 420, "y": 200}}},
        
        {"id": "merge_all", "objectId": "b4", "type": "translate", "start": 5, "end": 6, "params": {"to": {"x": 250, "y": 200}}, "narrative": "Merge final sorted array."},
        {"id": "merge_all2", "objectId": "b2", "type": "translate", "start": 5, "end": 6, "params": {"to": {"x": 310, "y": 200}}},
        {"id": "merge_all3", "objectId": "b3", "type": "translate", "start": 5, "end": 6, "params": {"to": {"x": 370, "y": 200}}},
        {"id": "merge_all4", "objectId": "b1", "type": "translate", "start": 5, "end": 6, "params": {"to": {"x": 430, "y": 200}}}
    ]
}

TEMPLATE_MITOSIS = {
    "sceneId": "mitosis",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "Cell Division",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#101020"}},
        {"id": "cell", "type": "circle", "props": {"x": 400, "y": 225, "r": 100, "color": "#e84393"}},
        {"id": "chrom1", "type": "rect", "props": {"x": 380, "y": 200, "width": 10, "height": 50, "color": "#fff"}},
        {"id": "chrom2", "type": "rect", "props": {"x": 410, "y": 200, "width": 10, "height": 50, "color": "#fff"}},
        {"id": "cell2", "type": "circle", "props": {"x": 400, "y": 225, "r": 100, "color": "#e84393", "opacity": 0}}
    ],
    "actions": [
        {"id": "dup", "objectId": "chrom1", "type": "scale", "start": 1, "end": 2, "params": {"scale": 1.2}, "narrative": "Chromosomes duplicate."},
        {"id": "sep", "objectId": "chrom1", "type": "translate", "start": 3, "end": 4, "params": {"to": {"x": 350, "y": 200}}, "narrative": "Chromosomes separate to poles."},
        {"id": "sep2", "objectId": "chrom2", "type": "translate", "start": 3, "end": 4, "params": {"to": {"x": 450, "y": 200}}},
        {"id": "split", "objectId": "cell", "type": "translate", "start": 5, "end": 7, "params": {"to": {"x": 300, "y": 225}}, "narrative": "Cell divides into two."},
        {"id": "split2", "objectId": "cell2", "type": "fade", "start": 5, "end": 5.1, "params": {"opacity": 1}},
        {"id": "split2_mv", "objectId": "cell2", "type": "translate", "start": 5.1, "end": 7, "params": {"to": {"x": 500, "y": 225}}}
    ]
}

TEMPLATE_ELECTROLYSIS = {
    "sceneId": "electrolysis",
    "width": 800,
    "height": 450,
    "duration": 10,
    "code": "2H2O(l) -> 2H2(g) + O2(g)\n# Electrolysis of Water",
    "objects": [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "beaker", "type": "rect", "props": {"x": 300, "y": 200, "width": 200, "height": 200, "color": "rgba(52, 152, 219, 0.3)"}},
        {"id": "water", "type": "rect", "props": {"x": 310, "y": 250, "width": 180, "height": 140, "color": "rgba(52, 152, 219, 0.6)"}},
        {"id": "anode", "type": "rect", "props": {"x": 350, "y": 180, "width": 20, "height": 150, "color": "#95a5a6"}},
        {"id": "cathode", "type": "rect", "props": {"x": 430, "y": 180, "width": 20, "height": 150, "color": "#95a5a6"}},
        {"id": "battery", "type": "rect", "props": {"x": 380, "y": 100, "width": 40, "height": 20, "color": "#f1c40f"}},
        {"id": "wire1", "type": "path", "props": {"d": "M 360 180 L 360 110 L 380 110", "color": "#fff", "width": 2}},
        {"id": "wire2", "type": "path", "props": {"d": "M 440 180 L 440 110 L 420 110", "color": "#fff", "width": 2}},
        {"id": "h2_bubble", "type": "circle", "props": {"x": 440, "y": 300, "r": 5, "color": "#fff", "opacity": 0}},
        {"id": "o2_bubble", "type": "circle", "props": {"x": 360, "y": 300, "r": 8, "color": "#fff", "opacity": 0}},
        {"id": "eq", "type": "text", "props": {"x": 400, "y": 50, "text": "2H2O -> 2H2 + O2", "font": "24px Arial", "color": "#fff"}}
    ],
    "actions": [
        {"id": "start", "objectId": "battery", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "Electric current is passed through water."},
        {"id": "bubble_h2", "objectId": "h2_bubble", "type": "translate", "start": 2, "end": 5, "params": {"to": {"x": 440, "y": 200}}, "narrative": "Hydrogen gas forms at the cathode (negative)."},
        {"id": "show_h2", "objectId": "h2_bubble", "type": "fade", "start": 2, "end": 2.5, "params": {"opacity": 1}},
        {"id": "bubble_o2", "objectId": "o2_bubble", "type": "translate", "start": 2, "end": 5, "params": {"to": {"x": 360, "y": 200}}, "narrative": "Oxygen gas forms at the anode (positive)."},
        {"id": "show_o2", "objectId": "o2_bubble", "type": "fade", "start": 2, "end": 2.5, "params": {"opacity": 1}},
        {"id": "ratio", "objectId": "eq", "type": "fade", "start": 6, "end": 7, "params": {"opacity": 1}, "narrative": "The volume of Hydrogen is twice that of Oxygen."}
    ]
}

TEMPLATES = {
    "bubble": TEMPLATE_BUBBLE_SORT,
    "selection": TEMPLATE_SELECTION_SORT,
    "sine": TEMPLATE_SINE_WAVE,
    "pythagoras": TEMPLATE_PYTHAGORAS,
    "vector": TEMPLATE_VECTOR_ADD,
    "sphere": TEMPLATE_SPHERE,
    "matrix": TEMPLATE_MATRIX,
    "geometry": TEMPLATE_GEOMETRY_SHAPES,
    "derivation": TEMPLATE_DERIVATION,
    "graph": TEMPLATE_GRAPH_PLOT,
    "binary": TEMPLATE_ALGO_BINARY,
    "atom": TEMPLATE_ATOM,
    "bfs": TEMPLATE_ALGO_BFS,
    "solar": TEMPLATE_SOLAR_SYSTEM,
    "dna": TEMPLATE_DNA,
    "quadratic": TEMPLATE_QUADRATIC,
    "dot_product": TEMPLATE_DOT_PRODUCT,
    "pie": TEMPLATE_PIE_CHART,
    "algebra": TEMPLATE_ALGEBRA,
    "stack": TEMPLATE_STACK,
    "photosynthesis": TEMPLATE_PHOTOSYNTHESIS,
    "limit": TEMPLATE_LIMIT,
    "cross_product": TEMPLATE_CROSS_PRODUCT,
    "bar_race": TEMPLATE_BAR_RACE,
    "integral": TEMPLATE_INTEGRAL,
    "queue": TEMPLATE_QUEUE,
    "water_cycle": TEMPLATE_WATER_CYCLE,
    "fourier": TEMPLATE_FOURIER,
    "vec_sub": TEMPLATE_VEC_SUB,
    "scatter": TEMPLATE_SCATTER,
    "chain_rule": TEMPLATE_CHAIN_RULE,
    "merge_sort": TEMPLATE_MERGE_SORT,
    "mitosis": TEMPLATE_MITOSIS,
    "mitosis": TEMPLATE_MITOSIS,
    "mitosis": TEMPLATE_MITOSIS,
    "electrolysis": TEMPLATE_ELECTROLYSIS,
    "bernoulli": TEMPLATE_BERNOULLI
}


# Merge Generated Templates
TEMPLATES.update(GENERATED_TEMPLATES)

# --- 2. ROUTES ---

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

@app.route('/')
def home():
    return send_from_directory('public', 'home.html')

@app.route('/login')
def login():
    return send_from_directory('public', 'login.html')

@app.route('/signup')
def signup():
    return send_from_directory('public', 'signup.html')
    
@app.route('/gallery')
def gallery():
    return send_from_directory('public', 'gallery.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('public', 'dashboard.html')

@app.route('/app')
def app_page():
    return send_from_directory('public', 'app.html')

@app.route('/tutorial')
def tutorial_page():
    return send_from_directory('public', 'tutorial.html')

@app.route('/auth/google')
def google_auth():
    # Placeholder for Google Auth - redirects to dashboard for demo
    return redirect('/dashboard')

@app.route('/generate/scenes', methods=['POST'])
def generate_scenes():
    data = request.json
    description = data.get('description', '').lower()
    options = data.get('options', {})
    language = options.get('language', 'python')
    level = options.get('level', 'beginner')
    
    # Rule-based Parser
    
    # Rule-based Parser (Updated)
    
    # 0. Full Course Check
    if 'full length' in description or 'full video' in description or 'all topics' in description or 'full course' in description:
        import template_generator
        return jsonify(template_generator.generate_full_course_template())

    # 1. Specific Dynamic Handlers (Regex)
    
    # Geometry: "5-gon", "polygon 5"
    poly_match = re.search(r'(\d+)[ -]gon|polygon (\d+)', description)
    if poly_match:
        n = int(poly_match.group(1) or poly_match.group(2))
        key = f"poly_{n}"
        if key in TEMPLATES: return jsonify(TEMPLATES[key])
    if 'triangle' in description: return jsonify(TEMPLATES.get('poly_3', TEMPLATE_PYTHAGORAS))
    if 'square' in description: return jsonify(TEMPLATES.get('poly_4', TEMPLATE_GEOMETRY_SHAPES))
    if 'pentagon' in description: return jsonify(TEMPLATES.get('poly_5', TEMPLATE_GEOMETRY_SHAPES))
    if 'hexagon' in description: return jsonify(TEMPLATES.get('poly_6', TEMPLATE_GEOMETRY_SHAPES))
    
    # Atoms: "atom 6", "element 1"
    atom_match = re.search(r'atom (\d+)|element (\d+)', description)
    if atom_match:
        n = int(atom_match.group(1) or atom_match.group(2))
        key = f"atom_{n}"
        if key in TEMPLATES: return jsonify(TEMPLATES[key])

    # Matrix Operations - Dynamic
    matrix_match = re.search(r'(\d+)[\*x](\d+)', description)
    if matrix_match and ('matrix' in description or 'multiplication' in description):
        rows = min(int(matrix_match.group(1)), 6)
        cols = min(int(matrix_match.group(2)), 6)
        op = "mult"
        if "exponentiation" in description or "power" in description: op = "exp"
        elif "add" in description or "sum" in description: op = "add"
        import template_generator
        return jsonify(template_generator.generate_matrix_template(rows, cols, op))

    # 2. General Intent Parsing
    intent = intent_parser.parse(description)
    key = intent['template_key']
    difficulty = intent.get('difficulty', 'beginner')

    if key:
        if key == "bubble":
            import template_generator
            import random
            return jsonify(template_generator.generate_algo_template(random.randint(0, 99), difficulty=level, language=language))
            
        if key == "binary":
            import template_generator
            import random
            return jsonify(template_generator.generate_search_template(random.randint(0, 99), difficulty=level, language=language))
            
        if key == "selection":
            import template_generator
            import random
            return jsonify(template_generator.generate_algo_template(random.randint(0, 99), difficulty=level, language=language, algo_type="selection"))
        
        if key == "quicksort": # Assuming intent parser might give this
            import template_generator
            import random
            return jsonify(template_generator.generate_quicksort_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "merge_sort":
            import template_generator
            import random
            return jsonify(template_generator.generate_mergesort_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "dfs":
            import template_generator
            import random
            return jsonify(template_generator.generate_dfs_bfs_template(random.randint(0, 99), algo_type="dfs", difficulty=level, language=language))

        if key == "bfs":
            import template_generator
            import random
            return jsonify(template_generator.generate_dfs_bfs_template(random.randint(0, 99), algo_type="bfs", difficulty=level, language=language))

        if key == "bellman_ford":
            import template_generator
            import random
            return jsonify(template_generator.generate_bellman_ford_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "floyd_warshall":
            import template_generator
            import random
            return jsonify(template_generator.generate_floyd_warshall_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "bst":
            import template_generator
            import random
            return jsonify(template_generator.generate_bst_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "linked_list":
            import template_generator
            import random
            return jsonify(template_generator.generate_linked_list_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "stack":
            import template_generator
            import random
            return jsonify(template_generator.generate_stack_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "queue":
            import template_generator
            import random
            return jsonify(template_generator.generate_queue_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "radix_sort":
            import template_generator
            import random
            return jsonify(template_generator.generate_radix_sort_template(random.randint(0, 99), difficulty=level, language=language))

        if key == "astar":
            import template_generator
            import random
            return jsonify(template_generator.generate_astar_template(random.randint(0, 99), difficulty=level, language=language))

        # --- Phase 1 Algorithms ---
        if key == "fibonacci":
            import template_generator
            return jsonify(template_generator.generate_fibonacci_template(0, difficulty=level, language=language))
            
        if key == "counting_sort":
            import template_generator
            return jsonify(template_generator.generate_counting_sort_template(0, difficulty=level, language=language))
            
        if key == "bucket_sort":
            import template_generator
            return jsonify(template_generator.generate_bucket_sort_template(0, difficulty=level, language=language))
            
        if key == "knapsack":
            import template_generator
            return jsonify(template_generator.generate_knapsack_template(0, difficulty=level, language=language))
            
        if key == "lcs":
            import template_generator
            return jsonify(template_generator.generate_lcs_template(0, difficulty=level, language=language))
            
        if key == "edit_distance":
            import template_generator
            return jsonify(template_generator.generate_edit_distance_template(0, difficulty=level, language=language))
            
        if key == "nqueens":
            import template_generator
            n_val = 4 # Default to 4-queens
            if "5" in description: n_val = 5
            return jsonify(template_generator.generate_nqueens_template(0, n=n_val, difficulty=level, language=language))
            
        if key == "kruskal_mst":
            import template_generator
            return jsonify(template_generator.generate_kruskal_mst_template(0, difficulty=level, language=language))
            
        if key == "prim_mst":
            import template_generator
            return jsonify(template_generator.generate_prim_mst_template(0, difficulty=level, language=language))
            
        if key == "max_subarray":
            import template_generator
            return jsonify(template_generator.generate_max_subarray_template(0, difficulty=level, language=language))

        # Dynamic Advanced Topics
        if key.startswith("dynamic:"):
            topic = key.split(":")[1]
            import template_generator
            if topic == "quicksort":
                return jsonify(template_generator.generate_quicksort_template(random.randint(0, 99), difficulty=level, language=language))
            if topic == "dijkstra":
                return jsonify(template_generator.generate_graph_algo_template(random.randint(0, 99), algo="dijkstra", difficulty=level, language=language))
            return jsonify(template_generator.generate_advanced_math_template(topic))
        
        # Static Templates - Check if template supports difficulty levels
        # If it does, regenerate dynamically; otherwise return static version
        if key in TEMPLATES:
            # Map of template keys to their dynamic generator functions
            # These algorithms support difficulty levels and should be regenerated
            dynamic_generators = {
                'sort_bubble': lambda: template_generator.generate_algo_template(random.randint(0, 99), difficulty=level, language=language, algo_type='bubble'),
                'sort_selection': lambda: template_generator.generate_algo_template(random.randint(0, 99), difficulty=level, language=language, algo_type='selection'),
                'search_binary': lambda: template_generator.generate_search_template(random.randint(0, 99), difficulty=level, language=language),
                'sort_quick': lambda: template_generator.generate_quicksort_template(random.randint(0, 99), difficulty=level, language=language),
                'sort_merge': lambda: template_generator.generate_mergesort_template(random.randint(0, 99), difficulty=level, language=language),
                'graph_dfs': lambda: template_generator.generate_dfs_bfs_template(random.randint(0, 99), algo_type='dfs', difficulty=level, language=language),
                'graph_bfs': lambda: template_generator.generate_dfs_bfs_template(random.randint(0, 99), algo_type='bfs', difficulty=level, language=language),
                'graph_bellman_ford': lambda: template_generator.generate_bellman_ford_template(random.randint(0, 99), difficulty=level, language=language),
                'graph_floyd_warshall': lambda: template_generator.generate_floyd_warshall_template(random.randint(0, 99), difficulty=level, language=language),
                'ds_bst': lambda: template_generator.generate_bst_template(random.randint(0, 99), difficulty=level, language=language),
                'ds_linked_list': lambda: template_generator.generate_linked_list_template(random.randint(0, 99), difficulty=level, language=language),
                'ds_stack': lambda: template_generator.generate_stack_template(random.randint(0, 99), difficulty=level, language=language),
                'ds_queue': lambda: template_generator.generate_queue_template(random.randint(0, 99), difficulty=level, language=language),
                'sort_radix': lambda: template_generator.generate_radix_sort_template(random.randint(0, 99), difficulty=level, language=language),
                'search_astar': lambda: template_generator.generate_astar_template(random.randint(0, 99), difficulty=level, language=language),
            }
            
            # If this template supports dynamic generation, regenerate it
            if key in dynamic_generators:
                import template_generator
                import random
                return jsonify(dynamic_generators[key]())
            
            # Otherwise, return the static template
            return jsonify(TEMPLATES[key])

    # 3. Fallback / Advanced Formula Search (Legacy support)
    def normalize(s): 
        s = s.replace('ö', 'o').replace('ä', 'a').replace('ü', 'u').replace('é', 'e')
        return re.sub(r'[^a-z0-9]', '', s.lower())
    
    norm_desc = normalize(description)
    for t_key in TEMPLATES:
        if t_key.startswith('formula_'):
            raw_name = t_key.replace('formula_', '').replace('_', ' ')
            if normalize(raw_name) in norm_desc:
                return jsonify(TEMPLATES[t_key])

    # Error / Suggestion
    return jsonify({
        "error": "Could not parse description",
        "suggestedPrompt": "Try: 'Bubble sort', 'Solar system', 'DNA Helix', 'BFS Graph', 'Binary search', 'Atom model', 'Quadratic roots', 'Dot product', 'Pie chart', 'Photosynthesis', 'Calculus Limit', 'Matrix 3x3', 'Polygon 5'",
        "exampleSceneSchema": TEMPLATE_BUBBLE_SORT
    }), 400

@app.route('/render/video', methods=['POST'])
def render_video():
    return jsonify({
        "status": "not_implemented",
        "instructions": "Use Puppeteer + ffmpeg in production. This endpoint is a placeholder."
    })

@app.route('/templates', methods=['GET'])
def get_templates():
    # Return keys only to avoid massive payload
    return jsonify(list(TEMPLATES.keys()))

@app.route('/api/library', methods=['GET'])
def get_library():
    # Sort library by domain then name
    sorted_lib = sorted(LIBRARY, key=lambda x: (x['domain'], x['name']))
    return jsonify(sorted_lib)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, port=port, host='0.0.0.0')
