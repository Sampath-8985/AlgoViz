import random
import math
import re
from code_generator import CodeGenerator

def generate_polygon_template(n_sides):
    """Generates a premium template for a regular polygon with n_sides."""
    scene_id = f"poly_{n_sides}"
    angle_step = 2 * math.pi / n_sides
    points = []
    radius = 150
    center_x, center_y = 400, 225
    
    # Calculate vertices
    vertices = []
    for i in range(n_sides):
        angle = i * angle_step - math.pi / 2 # Start from top
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        vertices.append((x, y))
        points.append(f"{x:.1f} {y:.1f}")
    
    path_d = "M " + " L ".join(points) + " Z"
    color = random.choice(["#e74c3c", "#3498db", "#2ecc71", "#9b59b6", "#f1c40f", "#e67e22"])
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "grid", "type": "path", "props": {"d": "M 400 0 L 400 450 M 0 225 L 800 225", "color": "#313244", "width": 2}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": f"Regular {n_sides}-gon", "font": "bold 32px Inter", "color": "#89b4fa", "opacity": 0}},
        {"id": "poly", "type": "path", "props": {"d": path_d, "color": color, "width": 4, "opacity": 0}},
        {"id": "info", "type": "text", "props": {"x": 400, "y": 400, "text": f"Interior Angle: {((n_sides-2)*180)/n_sides:.1f}°", "font": "20px monospace", "color": "#cdd6f4", "opacity": 0}}
    ]
    
    actions = [
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}},
        {"id": "draw_poly", "objectId": "poly", "type": "fade", "start": 1.5, "end": 3.0, "params": {"opacity": 1}, "narrative": f"Constructing a regular polygon with {n_sides} equal sides."},
        {"id": "pulse_poly", "objectId": "poly", "type": "scale", "start": 3.0, "end": 3.5, "params": {"scale": 1.05}},
        {"id": "pulse_poly_back", "objectId": "poly", "type": "scale", "start": 3.5, "end": 4.0, "params": {"scale": 1.0}},
        {"id": "show_info", "objectId": "info", "type": "fade", "start": 4.5, "end": 5.5, "params": {"opacity": 1}, "narrative": f"Each interior angle measures {((n_sides-2)*180)/n_sides:.1f} degrees."}
    ]
    
    # Add vertices dots
    for i, (vx, vy) in enumerate(vertices):
        vid = f"v{i}"
        objects.append({"id": vid, "type": "circle", "props": {"x": vx, "y": vy, "r": 6, "color": "#fff", "opacity": 0}})
        actions.append({"id": f"show_{vid}", "objectId": vid, "type": "fade", "start": 1.5 + (i/n_sides), "end": 2.0 + (i/n_sides), "params": {"opacity": 1}})

    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": 7,
        "code": f"# Regular Polygon\n# Sides: {n_sides}\n# Angle: {360/n_sides:.1f}",
        "objects": objects,
        "actions": actions
    }

def get_formula_simulation(name):
    """Returns extra objects and actions for specific physics simulations."""
    objects = []
    actions = []
    
    if "Time Dilation" in name:
        # Two clocks
        objects.append({"id": "clock1", "type": "circle", "props": {"x": 200, "y": 300, "r": 40, "color": "#89b4fa", "opacity": 0}})
        objects.append({"id": "hand1", "type": "rect", "props": {"x": 200, "y": 300, "width": 2, "height": 35, "color": "#fff", "opacity": 0}})
        objects.append({"id": "label1", "type": "text", "props": {"x": 200, "y": 360, "text": "Stationary", "font": "16px Arial", "color": "#89b4fa", "opacity": 0}})
        
        objects.append({"id": "clock2", "type": "circle", "props": {"x": 600, "y": 300, "r": 40, "color": "#f38ba8", "opacity": 0}})
        objects.append({"id": "hand2", "type": "rect", "props": {"x": 600, "y": 300, "width": 2, "height": 35, "color": "#fff", "opacity": 0}})
        objects.append({"id": "label2", "type": "text", "props": {"x": 600, "y": 360, "text": "Moving (v=0.9c)", "font": "16px Arial", "color": "#f38ba8", "opacity": 0}})
        
        # Show clocks
        actions.append({"id": "show_c1", "objectId": "clock1", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "show_h1", "objectId": "hand1", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "show_l1", "objectId": "label1", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "show_c2", "objectId": "clock2", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "show_h2", "objectId": "hand2", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "show_l2", "objectId": "label2", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        
        # Animate hands (rotation) - simulated by just narrative for now as engine might not support continuous rotation easily without loop
        # But we can try multiple rotate steps
        for i in range(4):
            t = 6 + i
            actions.append({"id": f"rot1_{i}", "objectId": "hand1", "type": "rotate", "start": t, "end": t+1, "params": {"angle": 90}}) # Fast
            actions.append({"id": f"rot2_{i}", "objectId": "hand2", "type": "rotate", "start": t, "end": t+1, "params": {"angle": 30}}) # Slow (dilated)
            
    elif "Gravitation" in name or "Orbit" in name:
        # Two planets
        objects.append({"id": "p1", "type": "circle", "props": {"x": 200, "y": 300, "r": 30, "color": "#3498db", "opacity": 0}})
        objects.append({"id": "p2", "type": "circle", "props": {"x": 600, "y": 300, "r": 30, "color": "#e74c3c", "opacity": 0}})
        
        actions.append({"id": "show_p", "objectId": "p1", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "show_p2", "objectId": "p2", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        
        # Move together
        actions.append({"id": "attract1", "objectId": "p1", "type": "translate", "start": 6, "end": 9, "params": {"to": {"x": 350, "y": 300}}})
        actions.append({"id": "attract2", "objectId": "p2", "type": "translate", "start": 6, "end": 9, "params": {"to": {"x": 450, "y": 300}}, "narrative": "Masses attract each other with a force proportional to product of masses."})

    elif "Wave Equation" in name:
        # Moving Sine Wave
        path_d = "M 0 300 Q 100 200 200 300 T 400 300 T 600 300 T 800 300"
        objects.append({"id": "wave", "type": "path", "props": {"d": path_d, "color": "#a6e3a1", "width": 3, "opacity": 0}})
        actions.append({"id": "show_w", "objectId": "wave", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        # Simulate propagation by shifting path? Hard without re-calc. 
        # Let's just fade in a second shifted wave
        path_d2 = "M 0 300 Q 100 400 200 300 T 400 300 T 600 300 T 800 300" # Inverted/Shifted
        objects.append({"id": "wave2", "type": "path", "props": {"d": path_d2, "color": "#fab387", "width": 3, "opacity": 0}})
        actions.append({"id": "pulse_w", "objectId": "wave2", "type": "fade", "start": 6, "end": 7, "params": {"opacity": 1}})
        actions.append({"id": "hide_w", "objectId": "wave", "type": "fade", "start": 6, "end": 7, "params": {"opacity": 0}})
        actions.append({"id": "pulse_w2", "objectId": "wave", "type": "fade", "start": 7, "end": 8, "params": {"opacity": 1}})
        actions.append({"id": "hide_w2", "objectId": "wave2", "type": "fade", "start": 7, "end": 8, "params": {"opacity": 0}})

    elif "Doppler Effect" in name:
        # Moving source
        objects.append({"id": "source", "type": "circle", "props": {"x": 100, "y": 300, "r": 10, "color": "#fff", "opacity": 0}})
        actions.append({"id": "show_s", "objectId": "source", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "move_s", "objectId": "source", "type": "translate", "start": 6, "end": 10, "params": {"to": {"x": 700, "y": 300}}})
        
        # Emitted waves (static for simplicity but positioned)
        for i in range(5):
            x = 100 + i * 100
            r = 20 + i * 10
            # As source moves right, waves bunch up on right? 
            # Actually let's just show circles appearing behind it
            wid = f"w_{i}"
            objects.append({"id": wid, "type": "circle", "props": {"x": x, "y": 300, "r": 5, "color": "#3498db", "opacity": 0, "width": 2}})
            actions.append({"id": f"emit_{i}", "objectId": wid, "type": "fade", "start": 6 + i*0.5, "end": 6.5 + i*0.5, "params": {"opacity": 1}})
            actions.append({"id": f"grow_{i}", "objectId": wid, "type": "scale", "start": 6.5 + i*0.5, "end": 10, "params": {"scale": 5}})

    elif "Schrodinger Equation" in name:
        # Wave packet simulation
        # Create a wave packet shape
        points = []
        for x in range(0, 801, 10):
            # Gaussian envelope * Sine wave
            env = math.exp(-((x-200)/100)**2)
            y = 225 - 100 * env * math.sin(x/20)
            points.append(f"{x} {y:.1f}")
        
        path_d = "M " + " L ".join(points)
        
        objects.append({"id": "psi", "type": "path", "props": {"d": path_d, "color": "#a6e3a1", "width": 3, "opacity": 0}})
        objects.append({"id": "barrier", "type": "rect", "props": {"x": 600, "y": 100, "width": 20, "height": 250, "color": "#f38ba8", "opacity": 0.5}})
        
        actions.append({"id": "show_psi", "objectId": "psi", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}, "narrative": "The wave function Ψ describes the quantum state."})
        
        # Simulate movement and spreading
        # We'll just translate it for now, but ideally we'd morph the path. 
        # Let's try a simple translation to the barrier
        actions.append({"id": "move_psi", "objectId": "psi", "type": "translate", "start": 6, "end": 9, "params": {"to": {"x": 400, "y": 0}}, "narrative": "It evolves over time according to the Hamiltonian."})
        
    elif "Heisenberg Uncertainty" in name:
        # Narrow position -> Wide momentum
        objects.append({"id": "particle", "type": "circle", "props": {"x": 400, "y": 225, "r": 5, "color": "#fff", "opacity": 0}})
        objects.append({"id": "wave_pos", "type": "path", "props": {"d": "M 380 225 Q 400 100 420 225", "color": "#89b4fa", "width": 2, "opacity": 0}})
        objects.append({"id": "wave_mom", "type": "path", "props": {"d": "M 200 225 Q 300 150 400 225 T 600 225 T 800 225", "color": "#f38ba8", "width": 2, "opacity": 0}})
        
        actions.append({"id": "show_p", "objectId": "particle", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}})
        actions.append({"id": "show_pos", "objectId": "wave_pos", "type": "fade", "start": 6, "end": 7, "params": {"opacity": 1}, "narrative": "Precise position (Δx small)..."})
        actions.append({"id": "hide_pos", "objectId": "wave_pos", "type": "fade", "start": 8, "end": 9, "params": {"opacity": 0}})
        actions.append({"id": "show_mom", "objectId": "wave_mom", "type": "fade", "start": 9, "end": 10, "params": {"opacity": 1}, "narrative": "...means uncertain momentum (Δp large)."})

    elif "Newton's Laws" in name:
        # 1. Inertia (Ball stays) 2. F=ma (Ball accelerates) 3. Action/Reaction (Collision)
        objects.append({"id": "floor", "type": "rect", "props": {"x": 0, "y": 350, "width": 800, "height": 100, "color": "#313244"}})
        objects.append({"id": "ball", "type": "circle", "props": {"x": 100, "y": 325, "r": 25, "color": "#e74c3c"}})
        
        actions.append({"id": "rest", "objectId": "ball", "type": "scale", "start": 0, "end": 2, "params": {"scale": 1}, "narrative": "Law 1: An object at rest stays at rest."})
        actions.append({"id": "push", "objectId": "ball", "type": "translate", "start": 2, "end": 5, "params": {"to": {"x": 700, "y": 325}}, "narrative": "Law 2: Force equals mass times acceleration (F=ma)."})
        
        objects.append({"id": "wall", "type": "rect", "props": {"x": 750, "y": 250, "width": 50, "height": 150, "color": "#89b4fa"}})
        actions.append({"id": "bounce", "objectId": "ball", "type": "translate", "start": 5, "end": 7, "params": {"to": {"x": 400, "y": 325}}, "narrative": "Law 3: For every action, there is an equal and opposite reaction."})

    elif "Friction" in name:
        objects.append({"id": "floor", "type": "rect", "props": {"x": 0, "y": 350, "width": 800, "height": 100, "color": "#585b70"}})
        objects.append({"id": "block", "type": "rect", "props": {"x": 50, "y": 300, "width": 50, "height": 50, "color": "#f9e2af"}})
        
        actions.append({"id": "slide", "objectId": "block", "type": "translate", "start": 1, "end": 3, "params": {"to": {"x": 400, "y": 300}}, "narrative": "Applying force to overcome static friction."})
        actions.append({"id": "slow", "objectId": "block", "type": "translate", "start": 3, "end": 6, "params": {"to": {"x": 600, "y": 300}}, "narrative": "Kinetic friction opposes motion, eventually stopping the object."})

    elif "Work Energy Principle" in name:
        objects.append({"id": "ramp", "type": "path", "props": {"d": "M 0 100 L 400 350 L 800 350", "color": "#fff", "width": 2}})
        objects.append({"id": "box", "type": "rect", "props": {"x": 20, "y": 80, "width": 30, "height": 30, "color": "#a6e3a1"}})
        
        actions.append({"id": "fall", "objectId": "box", "type": "translate", "start": 1, "end": 4, "params": {"to": {"x": 400, "y": 330}}, "narrative": "Gravity does work, converting Potential Energy to Kinetic Energy."})
        actions.append({"id": "slide", "objectId": "box", "type": "translate", "start": 4, "end": 7, "params": {"to": {"x": 700, "y": 330}}, "narrative": "Friction does negative work, reducing Kinetic Energy."})

    elif "Force and Pressure" in name:
        objects.append({"id": "piston_cyl", "type": "rect", "props": {"x": 300, "y": 200, "width": 200, "height": 200, "color": "#313244", "opacity": 0.5}})
        objects.append({"id": "piston", "type": "rect", "props": {"x": 300, "y": 200, "width": 200, "height": 20, "color": "#fab387"}})
        objects.append({"id": "gas", "type": "rect", "props": {"x": 300, "y": 220, "width": 200, "height": 180, "color": "#89b4fa", "opacity": 0.3}})
        
        actions.append({"id": "compress", "objectId": "piston", "type": "translate", "start": 2, "end": 5, "params": {"to": {"x": 300, "y": 300}}, "narrative": "Applying Force over Area increases Pressure."})
        actions.append({"id": "compress_gas", "objectId": "gas", "type": "scale", "start": 2, "end": 5, "params": {"scale": 0.5}, "narrative": "Volume decreases, Pressure increases."}) # Note: Scale might need origin fix, but illustrative

    elif "Sound Propagation" in name:
        # Particles vibrating
        for i in range(20):
            x = 50 + i * 35
            pid = f"p{i}"
            objects.append({"id": pid, "type": "circle", "props": {"x": x, "y": 225, "r": 5, "color": "#fff"}})
            # Wave motion: each particle moves back and forth with phase delay
            actions.append({"id": f"vib_{i}", "objectId": pid, "type": "translate", "start": 1 + i*0.1, "end": 2 + i*0.1, "params": {"to": {"x": x+10, "y": 225}}, "narrative": "Particles vibrate longitudinally."})
            actions.append({"id": f"vib_back_{i}", "objectId": pid, "type": "translate", "start": 2 + i*0.1, "end": 3 + i*0.1, "params": {"to": {"x": x, "y": 225}}})

    elif "Reflection Refraction" in name:
        objects.append({"id": "medium", "type": "rect", "props": {"x": 0, "y": 225, "width": 800, "height": 225, "color": "#89b4fa", "opacity": 0.3}})
        objects.append({"id": "ray_in", "type": "arrow", "props": {"x": 0, "y": 0, "width": 4, "color": "#f1c40f", "points": [100, 50, 400, 225]}})
        objects.append({"id": "ray_ref", "type": "arrow", "props": {"x": 400, "y": 225, "width": 4, "color": "#f1c40f", "points": [400, 225, 700, 50], "opacity": 0}})
        objects.append({"id": "ray_trans", "type": "arrow", "props": {"x": 400, "y": 225, "width": 4, "color": "#f1c40f", "points": [400, 225, 600, 400], "opacity": 0}})
        
        actions.append({"id": "show_in", "objectId": "ray_in", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "Incident ray hits the interface."})
        actions.append({"id": "show_ref", "objectId": "ray_ref", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "Reflection: Angle of incidence equals angle of reflection."})
        actions.append({"id": "show_trans", "objectId": "ray_trans", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Refraction: Light bends towards normal in denser medium."})

    elif "Electricity Basics" in name or "Ohm" in name:
        objects.append({"id": "wire", "type": "path", "props": {"d": "M 100 100 L 700 100 L 700 350 L 100 350 Z", "color": "#f1c40f", "width": 4}})
        objects.append({"id": "battery", "type": "rect", "props": {"x": 50, "y": 180, "width": 100, "height": 90, "color": "#333"}})
        objects.append({"id": "bulb", "type": "circle", "props": {"x": 700, "y": 225, "r": 30, "color": "#555"}})
        
        actions.append({"id": "light_on", "objectId": "bulb", "type": "fade", "start": 2, "end": 3, "params": {"color": "#f1c40f"}, "narrative": "Voltage drives current through the circuit."}) # Note: fade param color might not work in engine, usually opacity. Assuming engine handles props update or we use opacity overlay.
        objects.append({"id": "bulb_lit", "type": "circle", "props": {"x": 700, "y": 225, "r": 30, "color": "#f1c40f", "opacity": 0}})
        actions.append({"id": "show_lit", "objectId": "bulb_lit", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}})
        
        # Electrons
        for i in range(5):
            eid = f"e{i}"
            objects.append({"id": eid, "type": "circle", "props": {"x": 100 + i*100, "y": 100, "r": 5, "color": "#3498db"}})
            actions.append({"id": f"move_{eid}", "objectId": eid, "type": "translate", "start": 1, "end": 5, "params": {"to": {"x": 700, "y": 100}}, "narrative": "Electrons flow from negative to positive."})

    elif "Solar System" in name:
        objects.append({"id": "sun", "type": "circle", "props": {"x": 400, "y": 225, "r": 40, "color": "#f1c40f"}})
        planets = [("mercury", 10, "#bdc3c7", 60), ("venus", 15, "#e67e22", 90), ("earth", 16, "#3498db", 130), ("mars", 12, "#c0392b", 170)]
        
        for pname, r, col, dist in planets:
            objects.append({"id": f"orbit_{pname}", "type": "circle", "props": {"x": 400, "y": 225, "r": dist, "color": "#444", "width": 1, "opacity": 0.5}}) # Orbit path
            objects.append({"id": pname, "type": "circle", "props": {"x": 400 + dist, "y": 225, "r": r, "color": col}})
            
            # Simple orbit animation (translate in square path as approx or rotate if engine supported)
            # Using translate for 4 points
            actions.append({"id": f"orbit_{pname}_1", "objectId": pname, "type": "translate", "start": 0, "end": 2, "params": {"to": {"x": 400, "y": 225 + dist}}})
            actions.append({"id": f"orbit_{pname}_2", "objectId": pname, "type": "translate", "start": 2, "end": 4, "params": {"to": {"x": 400 - dist, "y": 225}}})
            actions.append({"id": f"orbit_{pname}_3", "objectId": pname, "type": "translate", "start": 4, "end": 6, "params": {"to": {"x": 400, "y": 225 - dist}}})
            actions.append({"id": f"orbit_{pname}_4", "objectId": pname, "type": "translate", "start": 6, "end": 8, "params": {"to": {"x": 400 + dist, "y": 225}}})

    elif "Life Cycle of Star" in name:
        objects.append({"id": "star", "type": "circle", "props": {"x": 400, "y": 225, "r": 10, "color": "#fff", "opacity": 0}})
        
        actions.append({"id": "nebula", "objectId": "star", "type": "fade", "start": 0, "end": 2, "params": {"opacity": 0.5}, "narrative": "Nebula: Cloud of gas and dust."})
        actions.append({"id": "main_seq", "objectId": "star", "type": "scale", "start": 2, "end": 4, "params": {"scale": 5}, "narrative": "Main Sequence: Fusion of Hydrogen."})
        actions.append({"id": "color_change", "objectId": "star", "type": "fade", "start": 4, "end": 5, "params": {"color": "#e74c3c"}, "narrative": "Red Giant: Expansion and cooling."}) # Note: color param might need engine support
        # Using separate object for Red Giant color if needed, but let's assume overlay
        objects.append({"id": "red_giant", "type": "circle", "props": {"x": 400, "y": 225, "r": 50, "color": "#e74c3c", "opacity": 0}})
        actions.append({"id": "show_rg", "objectId": "red_giant", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}})
        actions.append({"id": "hide_star", "objectId": "star", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 0}})
        
        actions.append({"id": "supernova", "objectId": "red_giant", "type": "scale", "start": 6, "end": 7, "params": {"scale": 2}, "narrative": "Supernova: Explosive death."})
        actions.append({"id": "remnant", "objectId": "red_giant", "type": "scale", "start": 7, "end": 8, "params": {"scale": 0.1}, "narrative": "Remnant: Neutron Star or Black Hole."})

    elif "Water Cycle" in name:
        objects.append({"id": "water", "type": "rect", "props": {"x": 0, "y": 350, "width": 800, "height": 100, "color": "#3498db"}})
        objects.append({"id": "sun", "type": "circle", "props": {"x": 700, "y": 50, "r": 40, "color": "#f1c40f"}})
        objects.append({"id": "cloud", "type": "circle", "props": {"x": 200, "y": 100, "r": 40, "color": "#fff", "opacity": 0}})
        
        actions.append({"id": "evap", "objectId": "water", "type": "translate", "start": 1, "end": 3, "params": {"to": {"y": 360}}, "narrative": "Evaporation: Water turns to vapor."}) # Subtle move
        # Vapor particles
        for i in range(5):
            vid = f"v{i}"
            objects.append({"id": vid, "type": "circle", "props": {"x": 100 + i*50, "y": 350, "r": 5, "color": "#fff", "opacity": 0}})
            actions.append({"id": f"rise_{vid}", "objectId": vid, "type": "translate", "start": 1, "end": 3, "params": {"to": {"x": 200, "y": 100}}, "narrative": ""})
            actions.append({"id": f"show_{vid}", "objectId": vid, "type": "fade", "start": 1, "end": 2, "params": {"opacity": 0.5}})
            
        actions.append({"id": "condense", "objectId": "cloud", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Condensation: Vapor forms clouds."})
        
        # Rain
        for i in range(5):
            rid = f"r{i}"
            objects.append({"id": rid, "type": "rect", "props": {"x": 180 + i*10, "y": 140, "width": 2, "height": 10, "color": "#3498db", "opacity": 0}})
            actions.append({"id": f"rain_{rid}", "objectId": rid, "type": "translate", "start": 4 + i*0.2, "end": 5 + i*0.2, "params": {"to": {"x": 180 + i*10, "y": 350}}, "narrative": "Precipitation: Water falls back."})
            actions.append({"id": f"show_r_{rid}", "objectId": rid, "type": "fade", "start": 4 + i*0.2, "end": 4.5 + i*0.2, "params": {"opacity": 1}})

    elif "Carbon Cycle" in name or "Nitrogen Cycle" in name:
        # Simple flow
        objects.append({"id": "atmos", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 100, "color": "#89b4fa", "opacity": 0.3}})
        objects.append({"id": "ground", "type": "rect", "props": {"x": 0, "y": 350, "width": 800, "height": 100, "color": "#a6e3a1"}})
        objects.append({"id": "plant", "type": "rect", "props": {"x": 100, "y": 250, "width": 50, "height": 100, "color": "#2ecc71"}})
        objects.append({"id": "animal", "type": "rect", "props": {"x": 300, "y": 300, "width": 50, "height": 50, "color": "#e74c3c"}})
        
        # Arrows
        objects.append({"id": "a1", "type": "arrow", "props": {"x": 0, "y": 0, "width": 4, "color": "#fff", "points": [400, 50, 125, 250], "opacity": 0}}) # Atmos -> Plant
        objects.append({"id": "a2", "type": "arrow", "props": {"x": 0, "y": 0, "width": 4, "color": "#fff", "points": [150, 300, 300, 325], "opacity": 0}}) # Plant -> Animal
        objects.append({"id": "a3", "type": "arrow", "props": {"x": 0, "y": 0, "width": 4, "color": "#fff", "points": [325, 300, 400, 50], "opacity": 0}}) # Animal -> Atmos
        
        actions.append({"id": "s1", "objectId": "a1", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "Atmosphere to Plants (Photosynthesis/Fixation)."})
        actions.append({"id": "s2", "objectId": "a2", "type": "fade", "start": 3, "end": 4, "params": {"opacity": 1}, "narrative": "Plants to Animals (Consumption)."})
        actions.append({"id": "s3", "objectId": "a3", "type": "fade", "start": 5, "end": 6, "params": {"opacity": 1}, "narrative": "Animals to Atmosphere (Respiration/Decomposition)."})

    elif "Greenhouse Effect" in name or "Global Warming" in name:
        objects.append({"id": "earth", "type": "rect", "props": {"x": 0, "y": 350, "width": 800, "height": 100, "color": "#3498db"}})
        objects.append({"id": "atmos", "type": "rect", "props": {"x": 0, "y": 200, "width": 800, "height": 150, "color": "#fff", "opacity": 0.1}})
        objects.append({"id": "sun", "type": "circle", "props": {"x": 100, "y": 50, "r": 40, "color": "#f1c40f"}})
        
        # Rays
        objects.append({"id": "ray_in", "type": "arrow", "props": {"x": 0, "y": 0, "width": 4, "color": "#f1c40f", "points": [140, 90, 400, 350]}})
        objects.append({"id": "ray_out", "type": "arrow", "props": {"x": 0, "y": 0, "width": 4, "color": "#e74c3c", "points": [400, 350, 600, 100], "opacity": 0}})
        objects.append({"id": "ray_trap", "type": "arrow", "props": {"x": 0, "y": 0, "width": 4, "color": "#e74c3c", "points": [500, 225, 450, 350], "opacity": 0}})
        
        actions.append({"id": "in", "objectId": "ray_in", "type": "fade", "start": 0, "end": 1, "params": {"opacity": 1}, "narrative": "Solar radiation reaches Earth."})
        actions.append({"id": "out", "objectId": "ray_out", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": "Heat radiates back."})
        actions.append({"id": "trap", "objectId": "ray_trap", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}, "narrative": "Greenhouse gases trap heat, warming the planet."})

    elif "Photosynthesis" in name:
        objects.append({"id": "sun", "type": "circle", "props": {"x": 100, "y": 50, "r": 40, "color": "#f1c40f"}})
        objects.append({"id": "leaf", "type": "rect", "props": {"x": 350, "y": 200, "width": 100, "height": 150, "color": "#2ecc71"}})
        
        objects.append({"id": "co2", "type": "text", "props": {"x": 200, "y": 250, "text": "CO2 + H2O", "font": "20px Arial", "color": "#fff", "opacity": 0}})
        objects.append({"id": "o2", "type": "text", "props": {"x": 500, "y": 250, "text": "O2 + Glucose", "font": "20px Arial", "color": "#fff", "opacity": 0}})
        
        actions.append({"id": "input", "objectId": "co2", "type": "translate", "start": 1, "end": 3, "params": {"to": {"x": 350, "y": 250}}, "narrative": "Plants take in Carbon Dioxide and Water."})
        actions.append({"id": "show_in", "objectId": "co2", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}})
        actions.append({"id": "process", "objectId": "leaf", "type": "scale", "start": 3, "end": 4, "params": {"scale": 1.1}, "narrative": "Using Sunlight energy..."})
        actions.append({"id": "output", "objectId": "o2", "type": "translate", "start": 4, "end": 6, "params": {"to": {"x": 600, "y": 250}}, "narrative": "They produce Oxygen and Glucose."})
        actions.append({"id": "show_out", "objectId": "o2", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}})

    elif "Respiration" in name:
        # Reverse of photosynthesis roughly
        objects.append({"id": "cell", "type": "circle", "props": {"x": 400, "y": 225, "r": 80, "color": "#e74c3c", "opacity": 0.5}})
        objects.append({"id": "in", "type": "text", "props": {"x": 200, "y": 225, "text": "O2 + Glucose", "font": "20px Arial", "color": "#fff", "opacity": 0}})
        objects.append({"id": "out", "type": "text", "props": {"x": 400, "y": 225, "text": "Energy + CO2", "font": "20px Arial", "color": "#fff", "opacity": 0}})
        
        actions.append({"id": "enter", "objectId": "in", "type": "translate", "start": 1, "end": 3, "params": {"to": {"x": 400, "y": 225}}, "narrative": "Cells take in Oxygen and Glucose."})
        actions.append({"id": "show_in", "objectId": "in", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}})
        actions.append({"id": "release", "objectId": "out", "type": "translate", "start": 4, "end": 6, "params": {"to": {"x": 600, "y": 225}}, "narrative": "Releasing Energy and Carbon Dioxide."})
        actions.append({"id": "show_out", "objectId": "out", "type": "fade", "start": 4, "end": 5, "params": {"opacity": 1}})

    elif "Digestive System" in name:
        # Tube
        path_d = "M 100 100 L 100 300 Q 100 400 200 400 L 600 400"
        objects.append({"id": "tract", "type": "path", "props": {"d": path_d, "color": "#fab387", "width": 20, "opacity": 0.5}})
        objects.append({"id": "food", "type": "circle", "props": {"x": 100, "y": 80, "r": 8, "color": "#a6e3a1"}})
        
        actions.append({"id": "eat", "objectId": "food", "type": "followPath", "start": 1, "end": 8, "params": {"pathId": "tract", "duration": 7}, "narrative": "Food travels through Esophagus, Stomach, and Intestines."})

    elif "Human Heart" in name:
        # Simple heart shape pumping
        path_d = "M 400 300 C 400 200 300 150 300 250 C 300 350 400 400 400 400 C 400 400 500 350 500 250 C 500 150 400 200 400 300"
        objects.append({"id": "heart", "type": "path", "props": {"d": path_d, "color": "#e74c3c", "width": 0}}) # Filled via CSS? No, path stroke. Let's use thick stroke or fill if supported. Engine supports stroke.
        # Let's use a thick stroke to simulate fill
        objects.append({"id": "heart_fill", "type": "path", "props": {"d": path_d, "color": "#e74c3c", "width": 5}})
        
        actions.append({"id": "beat1", "objectId": "heart_fill", "type": "scale", "start": 1, "end": 1.5, "params": {"scale": 1.1}, "narrative": "Systole: Heart contracts to pump blood."})
        actions.append({"id": "beat2", "objectId": "heart_fill", "type": "scale", "start": 1.5, "end": 2, "params": {"scale": 1.0}, "narrative": "Diastole: Heart relaxes to fill."})
        actions.append({"id": "beat3", "objectId": "heart_fill", "type": "scale", "start": 3, "end": 3.5, "params": {"scale": 1.1}})
        actions.append({"id": "beat4", "objectId": "heart_fill", "type": "scale", "start": 3.5, "end": 4, "params": {"scale": 1.0}})

    elif "Nervous System" in name:
        # Neuron
        objects.append({"id": "soma", "type": "circle", "props": {"x": 100, "y": 225, "r": 20, "color": "#f9e2af"}})
        objects.append({"id": "axon", "type": "rect", "props": {"x": 120, "y": 220, "width": 500, "height": 10, "color": "#f9e2af"}})
        objects.append({"id": "terminal", "type": "circle", "props": {"x": 640, "y": 225, "r": 15, "color": "#f9e2af"}})
        
        objects.append({"id": "signal", "type": "circle", "props": {"x": 100, "y": 225, "r": 5, "color": "#f1c40f", "opacity": 0}})
        
        actions.append({"id": "fire", "objectId": "signal", "type": "fade", "start": 1, "end": 1.5, "params": {"opacity": 1}, "narrative": "Action Potential initiates."})
        actions.append({"id": "travel", "objectId": "signal", "type": "translate", "start": 1.5, "end": 4, "params": {"to": {"x": 640, "y": 225}}, "narrative": "Electrical signal travels down the axon."})

    elif "States of Matter" in name:
        # 3 containers
        for i, state in enumerate(["Solid", "Liquid", "Gas"]):
            x_off = i * 250
            objects.append({"id": f"cont_{i}", "type": "rect", "props": {"x": 50 + x_off, "y": 150, "width": 200, "height": 200, "color": "#313244", "opacity": 0.5}})
            objects.append({"id": f"label_{i}", "type": "text", "props": {"x": 150 + x_off, "y": 380, "text": state, "font": "20px Arial", "color": "#fff"}})
            
            # Particles
            for j in range(9):
                px = 100 + x_off + (j%3)*50
                py = 200 + (j//3)*50
                pid = f"p_{i}_{j}"
                
                if state == "Solid":
                    # Grid, slight vibration
                    objects.append({"id": pid, "type": "circle", "props": {"x": px, "y": py, "r": 10, "color": "#89b4fa"}})
                    actions.append({"id": f"vib_{pid}", "objectId": pid, "type": "scale", "start": 1, "end": 5, "params": {"scale": 1.1}}) # Simulate vib
                elif state == "Liquid":
                    # Bottom, random-ish
                    objects.append({"id": pid, "type": "circle", "props": {"x": px, "y": py + 20, "r": 10, "color": "#89b4fa"}})
                    actions.append({"id": f"flow_{pid}", "objectId": pid, "type": "translate", "start": 1, "end": 5, "params": {"to": {"x": px + random.randint(-10, 10), "y": py + 20}}})
                elif state == "Gas":
                    # Spread out
                    objects.append({"id": pid, "type": "circle", "props": {"x": px, "y": py, "r": 10, "color": "#89b4fa"}})
                    actions.append({"id": f"fly_{pid}", "objectId": pid, "type": "translate", "start": 1, "end": 5, "params": {"to": {"x": px + random.randint(-50, 50), "y": py + random.randint(-50, 50)}}})

    return objects, actions

def generate_formula_template(name, formula_latex, description):
    """Generates a premium template for a mathematical formula."""
    
    # Get base objects
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        # Subtle Grid Background
        {"id": "grid_h", "type": "path", "props": {"d": "M 0 225 L 800 225", "color": "#313244", "width": 2}},
        {"id": "grid_v", "type": "path", "props": {"d": "M 400 0 L 400 450", "color": "#313244", "width": 2}},
        
        {"id": "title", "type": "text", "props": {"x": 400, "y": 100, "text": name, "font": "bold 36px Inter", "color": "#89b4fa", "opacity": 0}},
        
        # Formula with glowing effect container
        {"id": "eq_bg", "type": "rect", "props": {"x": 100, "y": 180, "width": 600, "height": 80, "color": "#313244", "opacity": 0}},
        {"id": "eq", "type": "text", "props": {"x": 400, "y": 230, "text": formula_latex, "font": "42px monospace", "color": "#f38ba8", "opacity": 0}},
        
        {"id": "desc", "type": "text", "props": {"x": 400, "y": 350, "text": description, "font": "20px Inter", "color": "#cdd6f4", "opacity": 0}}
    ]
    
    actions = [
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}},
        {"id": "show_grid", "objectId": "grid_h", "type": "scale", "start": 0, "end": 1, "params": {"scale": 1}}, # Dummy action to ensure render
        
        {"id": "show_eq_bg", "objectId": "eq_bg", "type": "fade", "start": 1.5, "end": 2.5, "params": {"opacity": 0.5}},
        {"id": "show_eq", "objectId": "eq", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": f"The formula for {name} is {formula_latex}."},
        {"id": "pulse_eq", "objectId": "eq", "type": "scale", "start": 3, "end": 3.5, "params": {"scale": 1.1}},
        {"id": "pulse_eq_back", "objectId": "eq", "type": "scale", "start": 3.5, "end": 4, "params": {"scale": 1.0}},
        
        {"id": "show_desc", "objectId": "desc", "type": "translate", "start": 4.5, "end": 5.5, "params": {"to": {"x": 400, "y": 350}}, "narrative": description}, # Fade in by default if opacity 0->1, but let's use fade
        {"id": "fade_desc", "objectId": "desc", "type": "fade", "start": 4.5, "end": 5.5, "params": {"opacity": 1}}
    ]
    
    # Add Simulation if available
    sim_objs, sim_acts = get_formula_simulation(name)
    objects.extend(sim_objs)
    actions.extend(sim_acts)
    
    return {
        "sceneId": f"formula_{name.lower().replace(' ', '_')}",
        "width": 800,
        "height": 450,
        "duration": 10 + (4 if sim_acts else 0), # Extend duration if simulation exists
        "code": f"# {name}\n# {formula_latex}",
        "objects": objects,
        "actions": actions
    }

def generate_vector_template(idx):
    """Generates a random vector addition template."""
    ax, ay = random.randint(50, 200), random.randint(50, 100)
    bx, by = random.randint(50, 200), random.randint(-50, 100)
    start_x, start_y = 100, 300
    
    return {
        "sceneId": f"vector_gen_{idx}",
        "width": 800,
        "height": 450,
        "duration": 6,
        "code": f"A = [{ax}, {ay}], B = [{bx}, {by}]\nC = A + B",
        "objects": [
            {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#fff"}},
            {"id": "vec_a", "type": "arrow", "props": {"x": start_x, "y": start_y, "width": 4, "color": "#3498db", "points": [start_x, start_y, start_x + ax, start_y - ay]}},
            {"id": "vec_b", "type": "arrow", "props": {"x": start_x, "y": start_y, "width": 4, "color": "#e74c3c", "points": [start_x, start_y, start_x + bx, start_y - by]}}, # Initially at origin
            {"id": "vec_c", "type": "arrow", "props": {"x": start_x, "y": start_y, "width": 4, "color": "#2ecc71", "points": [start_x, start_y, start_x + ax + bx, start_y - ay - by], "opacity": 0}}
        ],
        "actions": [
            {"id": "move_b", "objectId": "vec_b", "type": "translate", "start": 1, "end": 3, "params": {"to": {"points": [start_x + ax, start_y - ay, start_x + ax + bx, start_y - ay - by]}}, "narrative": "Head-to-tail method."},
            {"id": "show_c", "objectId": "vec_c", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 1}, "narrative": "The resultant vector."}
        ]
    }

def generate_graph_template(func_name, func_expr):
    """Generates a premium graph plot template."""
    points = []
    scale_x = 40
    scale_y = 40
    center_x, center_y = 400, 225
    
    # Calculate points
    trace_points = []
    for i in range(-100, 101):
        x = i / 10.0
        try:
            y = eval(func_expr, {"x": x, "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, "sqrt": math.sqrt, "log": math.log})
            px = center_x + x * scale_x
            py = center_y - y * scale_y
            if 0 <= px <= 800 and 0 <= py <= 450:
                points.append(f"{px:.1f} {py:.1f}")
                if i % 5 == 0: trace_points.append((px, py)) 
        except:
            pass
            
    path_d = "M " + " L ".join(points) if points else ""
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        # Grid
        {"id": "grid_x", "type": "path", "props": {"d": "M 0 225 L 800 225", "color": "#45475a", "width": 2}},
        {"id": "grid_y", "type": "path", "props": {"d": "M 400 0 L 400 450", "color": "#45475a", "width": 2}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": f"y = {func_name}", "font": "bold 32px monospace", "color": "#89b4fa", "opacity": 0}},
        {"id": "curve", "type": "path", "props": {"d": path_d, "color": "#a6e3a1", "width": 4, "opacity": 0}},
        {"id": "tracer", "type": "circle", "props": {"x": center_x, "y": center_y, "r": 8, "color": "#f9e2af", "opacity": 0}}
    ]
    
    actions = [
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}},
        {"id": "draw_curve", "objectId": "curve", "type": "fade", "start": 1.5, "end": 3.0, "params": {"opacity": 1}, "narrative": f"Plotting the function {func_name}."},
        {"id": "show_tracer", "objectId": "tracer", "type": "fade", "start": 3.0, "end": 3.5, "params": {"opacity": 1}},
    ]
    
    if trace_points:
        start_p = trace_points[0]
        end_p = trace_points[-1]
        
        actions.append({"id": "trace_1", "objectId": "tracer", "type": "translate", "start": 3.5, "end": 4.5, "params": {"to": {"x": start_p[0], "y": start_p[1]}}})
        actions.append({"id": "trace_2", "objectId": "tracer", "type": "translate", "start": 4.5, "end": 6.5, "params": {"to": {"x": end_p[0], "y": end_p[1]}}, "narrative": "Tracing the values across the domain."})

    return {
        "sceneId": f"graph_{func_name}",
        "width": 800,
        "height": 450,
        "duration": 8,
        "code": f"import matplotlib.pyplot as plt\nx = np.linspace(-10, 10, 100)\ny = {func_expr}\nplt.plot(x, y)",
        "objects": objects,
        "actions": actions
    }

def generate_derivation_template(idx):
    """Generates a premium derivation template for x^n."""
    n = idx + 2
    return {
        "sceneId": f"deriv_x{n}",
        "width": 800,
        "height": 450,
        "duration": 8,
        "code": f"d/dx x^{n} = {n}x^{n-1}",
        "objects": [
            {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
            {"id": "grid", "type": "path", "props": {"d": "M 400 0 L 400 450 M 0 225 L 800 225", "color": "#313244", "width": 2}},
            {"id": "title", "type": "text", "props": {"x": 400, "y": 80, "text": "Power Rule Derivation", "font": "bold 32px Inter", "color": "#cdd6f4", "opacity": 0}},
            
            {"id": "l1", "type": "text", "props": {"x": 400, "y": 180, "text": f"f(x) = x^{n}", "font": "36px monospace", "color": "#89b4fa", "opacity": 0}},
            {"id": "arrow", "type": "text", "props": {"x": 400, "y": 240, "text": "↓", "font": "40px Arial", "color": "#fff", "opacity": 0}},
            {"id": "l2", "type": "text", "props": {"x": 400, "y": 300, "text": f"f'(x) = {n}x^{n-1}", "font": "36px monospace", "color": "#a6e3a1", "opacity": 0}}
        ],
        "actions": [
            {"id": "show_title", "objectId": "title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}},
            {"id": "s1", "objectId": "l1", "type": "fade", "start": 1.5, "end": 2.5, "params": {"opacity": 1}, "narrative": f"Consider the function x to the power of {n}."},
            {"id": "show_arrow", "objectId": "arrow", "type": "fade", "start": 3, "end": 3.5, "params": {"opacity": 1}},
            {"id": "s2", "objectId": "l2", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 1}, "narrative": f"Using the power rule, multiply by the exponent {n} and subtract 1 from the power."}
        ]
    }

def generate_atom_template(atomic_number):
    """Generates a premium Bohr model for an element."""
    electrons = atomic_number
    shells = [2, 8, 18, 32]
    config = []
    remaining = electrons
    for cap in shells:
        if remaining <= 0: break
        take = min(remaining, cap)
        config.append(take)
        remaining -= take
        
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#111"}},
        {"id": "nucleus_glow", "type": "circle", "props": {"x": 400, "y": 225, "r": 20, "color": "#e74c3c", "opacity": 0.5}},
        {"id": "nucleus", "type": "circle", "props": {"x": 400, "y": 225, "r": 10, "color": "#fff"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": f"Element {atomic_number}", "font": "bold 32px Inter", "color": "#fff", "opacity": 0}},
        {"id": "config_text", "type": "text", "props": {"x": 400, "y": 420, "text": f"Electron Config: {config}", "font": "20px monospace", "color": "#89b4fa", "opacity": 0}}
    ]
    actions = [
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}},
        {"id": "pulse_nuc", "objectId": "nucleus_glow", "type": "scale", "start": 0, "end": 2, "params": {"scale": 1.2}}, # Repeat?
        {"id": "show_config", "objectId": "config_text", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 1}, "narrative": f"This element has {atomic_number} electrons arranged in shells."}
    ]
    
    for i, count in enumerate(config):
        r = 50 + i * 40
        orbit_id = f"orbit_{i}"
        objects.append({"id": orbit_id, "type": "path", "props": {"d": f"M 400 225 m -{r}, 0 a {r},{r} 0 1,0 {2*r},0 a {r},{r} 0 1,0 -{2*r},0", "color": "#45475a", "width": 1, "opacity": 0}})
        actions.append({"id": f"show_{orbit_id}", "objectId": orbit_id, "type": "fade", "start": 1 + i*0.5, "end": 2 + i*0.5, "params": {"opacity": 0.5}})
        
        for j in range(count):
            e_id = f"e_{i}_{j}"
            # Distribute electrons
            angle = (2 * math.pi / count) * j
            ex = 400 + r * math.cos(angle) # Start pos
            ey = 225 + r * math.sin(angle)
            objects.append({"id": e_id, "type": "circle", "props": {"x": ex, "y": ey, "r": 5, "color": "#3498db", "opacity": 0}})
            actions.append({"id": f"show_{e_id}", "objectId": e_id, "type": "fade", "start": 2 + i*0.5, "end": 2.5 + i*0.5, "params": {"opacity": 1}})
            actions.append({"id": f"move_{e_id}", "objectId": e_id, "type": "followPath", "start": 2.5, "end": 12.5, "params": {"pathId": orbit_id, "duration": 3 + i}})

    return {
        "sceneId": f"atom_{atomic_number}",
        "width": 800,
        "height": 450,
        "duration": 12,
        "code": f"# Element {atomic_number}\n# Electrons: {config}",
        "objects": objects,
        "actions": actions
    }

def generate_algo_template(idx, difficulty="beginner", language="python", algo_type="bubble"):
    """Generates a sorting visualization (Bubble or Selection) with difficulty levels."""
    import random
    
    # 1. Data Setup
    if difficulty == "kids":
       data = [random.randint(1, 10) for _ in range(5)] # Smaller numbers
    else:
       data = [random.randint(10, 99) for _ in range(6)]
       
    n = len(data)
    arr = list(data) # Copy for simulation
    
    scene_id = f"sort_{algo_type}_{idx}"
    
    # 2. Code Content based on Difficulty, Algo, and Language
    code_content = CodeGenerator.get_code(f"{algo_type}_sort", language=language, level=difficulty)
    
    # 3. Base Objects
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": f"{algo_type.title()} Sort", "font": "bold 32px Inter", "color": "#89b4fa", "opacity": 0}},
    ]
    
    bar_width = 50
    gap = 20
    total_w = n * bar_width + (n-1) * gap
    start_x = (800 - total_w) / 2
    
    # Create Bar Objects
    bar_objs = []
    val_objs = []
    for i, val in enumerate(data):
        h = val * 3
        x = start_x + i * (bar_width + gap)
        y = 400 - h
        color = "#f9e2af" if difficulty == "kids" else "#89b4fa"
        
        bid = f"bar_{i}"
        vid = f"val_{i}"
        objects.append({
            "id": bid, 
            "type": "rect", 
            "props": {"x": x, "y": y, "width": bar_width, "height": h, "color": color, "opacity": 0}
        })
        objects.append({
            "id": vid, 
            "type": "text", 
            "props": {"x": x + bar_width/2, "y": y - 10, "text": str(val), "font": "16px monospace", "color": "#fff", "opacity": 0}
        })
        bar_objs.append(bid)
        val_objs.append(vid)

    actions = [
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}}
    ]

    # Show bars
    for i in range(n):
        actions.append({"id": f"show_bar_{i}", "objectId": f"bar_{i}", "type": "fade", "start": 1.0 + i*0.2, "end": 1.5 + i*0.2, "params": {"opacity": 1}})
        actions.append({"id": f"show_val_{i}", "objectId": f"val_{i}", "type": "fade", "start": 1.0 + i*0.2, "end": 1.5 + i*0.2, "params": {"opacity": 1}})

    # 4. Simulation & Animation Generation
    time = 3.0
    step_dur = 2.0 if difficulty == "beginner" else (2.5 if difficulty == "kids" else 1.2)
    
    if algo_type == "bubble":
        # ... (Existing Bubble Logic)
        for i in range(n):
            for j in range(0, n-i-1):
                # Highlight Comparison
                id1, id2 = bar_objs[j], bar_objs[j+1]
                v1, v2 = arr[j], arr[j+1]
                
                # Action: Highlight
                actions.append({
                    "id": f"comp_{i}_{j}",
                    "objectId": id1,
                    "type": "color",
                    "start": time,
                    "end": time + step_dur/2,
                    "params": {"color": "#e74c3c"}, 
                    "narrative": CodeGenerator.get_narrative("compare", v1, v2, language=language, level=difficulty),
                    "codeLine": 5 if difficulty == "beginner" else (2 if difficulty == "kids" else 6)
                })
                actions.append({
                    "id": f"comp_{i}_{j}_2",
                    "objectId": id2,
                    "type": "color",
                    "start": time,
                    "end": time + step_dur/2,
                    "params": {"color": "#e74c3c"}
                })
                
                time += step_dur/2
                
                if v1 > v2:
                    # Swap Logic
                    actions.append({
                        "id": f"swap_narrative_{i}_{j}",
                        "objectId": "title",
                        "type": "wait",
                        "start": time,
                        "end": time + step_dur,
                        "narrative": CodeGenerator.get_narrative("swap", v1, v2, language=language, level=difficulty),
                        "codeLine": 6 if difficulty == "beginner" else (3 if difficulty == "kids" else 7)
                    })
                    
                    # Animate Swap (Positions)
                    x1 = start_x + j * (bar_width + gap)
                    x2 = start_x + (j+1) * (bar_width + gap)
                    
                    actions.append({"id": f"swap_{i}_{j}_1", "objectId": id1, "type": "translate", "start": time, "end": time + step_dur, "params": {"to": {"x": x2}}})
                    actions.append({"id": f"swap_val_{i}_{j}_1", "objectId": val_objs[j], "type": "translate", "start": time, "end": time + step_dur, "params": {"to": {"x": x2 + bar_width/2}}})
                    
                    actions.append({"id": f"swap_{i}_{j}_2", "objectId": id2, "type": "translate", "start": time, "end": time + step_dur, "params": {"to": {"x": x1}}})
                    actions.append({"id": f"swap_val_{i}_{j}_2", "objectId": val_objs[j+1], "type": "translate", "start": time, "end": time + step_dur, "params": {"to": {"x": x1 + bar_width/2}}})
                    
                    # Update logical arrays
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    bar_objs[j], bar_objs[j+1] = bar_objs[j+1], bar_objs[j]
                    val_objs[j], val_objs[j+1] = val_objs[j+1], val_objs[j]
                    
                    time += step_dur
                else:
                    time += step_dur * 0.5
                
                # De-Highlight
                def get_color(idx_pos):
                    return "#f9e2af" if difficulty == "kids" else "#89b4fa"

                actions.append({"id": f"uncomp_{i}_{j}", "objectId": id1, "type": "color", "start": time, "end": time + 0.2, "params": {"color": get_color(j)}})
                actions.append({"id": f"uncomp_{i}_{j}_2", "objectId": id2, "type": "color", "start": time, "end": time + 0.2, "params": {"color": get_color(j+1)}})
                
            # End of pass
            sorted_idx = n - 1 - i
            actions.append({"id": f"sorted_{sorted_idx}", "objectId": bar_objs[sorted_idx], "type": "color", "start": time, "end": time + 0.5, "params": {"color": "#a6e3a1"}, "narrative": f"{arr[sorted_idx]} is now sorted." if difficulty != "kids" else "Sorted!"})
            time += 0.5

    elif algo_type == "selection":
        for i in range(n):
            min_idx = i
            
            # Highlight current start
            actions.append({
                "id": f"sel_start_{i}", 
                "objectId": bar_objs[i], 
                "type": "color", 
                "start": time, 
                "end": time+0.5, 
                "params": {"color": "#fab387"}, 
                "narrative": f"Pick {arr[i]} as initial minimum." if difficulty != "kids" else f"Try {arr[i]}!",
                "codeLine": 4 if difficulty == "beginner" else (1 if difficulty == "kids" else 6)
            })
            time += 0.5
            
            for j in range(i+1, n):
                # Compare arr[j] with arr[min_idx]
                actions.append({
                    "id": f"sel_comp_{i}_{j}", 
                    "objectId": bar_objs[j], 
                    "type": "color", 
                    "start": time, 
                    "end": time+0.5, 
                    "params": {"color": "#e74c3c"}, 
                    "narrative": CodeGenerator.get_narrative("compare", arr[j], arr[min_idx], language=language, level=difficulty), 
                    "codeLine": 6 if difficulty == "beginner" else (1 if difficulty == "kids" else 8)
                })
                
                if arr[j] < arr[min_idx]:
                    # Update min
                    old_min = bar_objs[min_idx]
                    if min_idx != i: # Don't uncolor start yet
                         actions.append({"id": f"unmin_{i}_{j}", "objectId": old_min, "type": "color", "start": time+0.5, "end": time+1, "params": {"color": "#89b4fa"}})
                    
                    min_idx = j
                    actions.append({"id": f"new_min_{i}_{j}", "objectId": bar_objs[min_idx], "type": "color", "start": time+0.5, "end": time+1, "params": {"color": "#fab387"}, "narrative": f"New minimum found: {arr[j]}", "codeLine": 7 if difficulty == "beginner" else (1 if difficulty == "kids" else 9)})
                    time += 1.0
                else:
                    actions.append({"id": f"uncomp_{i}_{j}", "objectId": bar_objs[j], "type": "color", "start": time+0.5, "end": time+1, "params": {"color": "#89b4fa"}})
                    time += 0.5
            
            # Swap if needed
            if min_idx != i:
                actions.append({"id": f"swap_narr_{i}", "objectId": "title", "type": "wait", "start": time, "end": time+1, "narrative": CodeGenerator.get_narrative("swap", arr[i], arr[min_idx], language=language, level=difficulty), "codeLine": 8 if difficulty=="beginner" else 10})
                
                id1, id2 = bar_objs[i], bar_objs[min_idx]
                x1 = start_x + i * (bar_width + gap)
                x2 = start_x + min_idx * (bar_width + gap)
                
                # Animate
                actions.append({"id": f"swap_{i}_pos", "objectId": id1, "type": "translate", "start": time, "end": time+1, "params": {"to": {"x": x2}}})
                actions.append({"id": f"swap_{i}_val", "objectId": val_objs[i], "type": "translate", "start": time, "end": time+1, "params": {"to": {"x": x2 + bar_width/2}}})
                actions.append({"id": f"swap_{min_idx}_pos", "objectId": id2, "type": "translate", "start": time, "end": time+1, "params": {"to": {"x": x1}}})
                actions.append({"id": f"swap_{min_idx}_val", "objectId": val_objs[min_idx], "type": "translate", "start": time, "end": time+1, "params": {"to": {"x": x1 + bar_width/2}}})
                
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                bar_objs[i], bar_objs[min_idx] = bar_objs[min_idx], bar_objs[i]
                val_objs[i], val_objs[min_idx] = val_objs[min_idx], val_objs[i]
                
                time += 1.0

            # Mark sorted
            actions.append({"id": f"sorted_{i}", "objectId": bar_objs[i], "type": "color", "start": time, "end": time+0.5, "params": {"color": "#a6e3a1"}, "narrative": f"{arr[i]} is sorted."})
            time += 0.5
            
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

def generate_matrix_template(rows, cols, operation="mult"):
    """Generates a detailed step-by-step matrix operation template."""
    import random
    
    # Generate Matrix A
    matrix_a = [[random.randint(0, 5) for _ in range(cols)] for _ in range(rows)]
    
    # Generate Matrix B
    if operation == "mult" or operation == "exp":
        rows_b = cols
        cols_b = rows if operation == "exp" else cols 
        matrix_b = [[random.randint(0, 5) for _ in range(cols_b)] for _ in range(rows_b)]
        if operation == "exp": matrix_b = matrix_a 
    else:
        matrix_b = [[random.randint(0, 5) for _ in range(cols)] for _ in range(rows)]

    # Calculate Result C
    matrix_c = []
    if operation == "mult" or operation == "exp":
        for i in range(rows):
            row = []
            for j in range(cols_b):
                val = sum(matrix_a[i][k] * matrix_b[k][j] for k in range(cols))
                row.append(val)
            matrix_c.append(row)
    elif operation == "add":
        matrix_c = [[matrix_a[i][j] + matrix_b[i][j] for j in range(cols)] for i in range(rows)]

    objects = [{"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}}]
    actions = []
    
    # Layout Constants
    cell_w = 40 if cols < 5 else 30
    cell_h = 40
    start_y = 150
    
    # Dynamic X positions
    width_a = cols * cell_w
    width_b = (cols_b if operation in ["mult", "exp"] else cols) * cell_w
    width_c = (cols_b if operation in ["mult", "exp"] else cols) * cell_w 
    
    gap = 50
    total_w = width_a + gap + width_b + gap + width_c
    start_x = (800 - total_w) / 2
    
    pos_a_x = start_x
    pos_op_x = pos_a_x + width_a + gap/2
    pos_b_x = pos_a_x + width_a + gap
    pos_eq_x = pos_b_x + width_b + gap/2
    pos_c_x = pos_b_x + width_b + gap

    # Helper to add matrix objects
    def add_matrix_objs(name, mat, x_start, y_start, color):
        h = len(mat)
        w = len(mat[0])
        
        # Brackets
        objects.append({"id": f"{name}_lb", "type": "text", "props": {"x": x_start - 10, "y": y_start + h*cell_h/2 + 10, "text": "[", "font": f"{h*cell_h}px Arial", "color": "#fff", "opacity": 0}})
        objects.append({"id": f"{name}_rb", "type": "text", "props": {"x": x_start + w*cell_w, "y": y_start + h*cell_h/2 + 10, "text": "]", "font": f"{h*cell_h}px Arial", "color": "#fff", "opacity": 0}})
        actions.append({"id": f"show_{name}_br", "objectId": f"{name}_lb", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}})
        actions.append({"id": f"show_{name}_br2", "objectId": f"{name}_rb", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}})

        for r in range(h):
            for c in range(w):
                val = mat[r][c]
                oid = f"{name}_{r}_{c}"
                # Highlight Rect (behind text)
                hid = f"h_{name}_{r}_{c}"
                objects.append({"id": hid, "type": "rect", "props": {"x": x_start + c*cell_w + cell_w/2 - 15, "y": y_start + r*cell_h + 5, "width": 30, "height": 30, "color": "#f9e2af", "opacity": 0}})
                
                # Text
                objects.append({"id": oid, "type": "text", "props": {"x": x_start + c*cell_w + cell_w/2, "y": y_start + r*cell_h + 25, "text": str(val), "font": "16px monospace", "color": color, "opacity": 0}})
                
                if name != "C":
                    actions.append({"id": f"show_{oid}", "objectId": oid, "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}})

    add_matrix_objs("A", matrix_a, pos_a_x, start_y, "#89b4fa")
    add_matrix_objs("B", matrix_b, pos_b_x, start_y, "#a6e3a1")
    add_matrix_objs("C", matrix_c, pos_c_x, start_y, "#f38ba8")

    # Operator and Equals
    op_sym = "×" if operation in ["mult", "exp"] else "+"
    objects.append({"id": "op", "type": "text", "props": {"x": pos_op_x, "y": start_y + rows*cell_h/2 + 10, "text": op_sym, "font": "30px Arial", "color": "#fff", "opacity": 0}})
    objects.append({"id": "eq", "type": "text", "props": {"x": pos_eq_x, "y": start_y + rows*cell_h/2 + 10, "text": "=", "font": "30px Arial", "color": "#fff", "opacity": 0}})
    actions.append({"id": "show_op", "objectId": "op", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}})
    actions.append({"id": "show_eq", "objectId": "eq", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}})

    # Animation Logic
    current_time = 2.5
    step_duration = 2.5
    max_steps = 9 # Cap detailed steps
    step_count = 0
    
    rows_c = len(matrix_c)
    cols_c = len(matrix_c[0])

    for i in range(rows_c):
        for j in range(cols_c):
            if step_count >= max_steps: break
            
            # Highlight A row i
            for k in range(len(matrix_a[0])):
                actions.append({"id": f"hi_a_{i}_{k}_{step_count}", "objectId": f"h_A_{i}_{k}", "type": "fade", "start": current_time, "end": current_time+0.5, "params": {"opacity": 0.3}})
            
            # Highlight B col j
            for k in range(len(matrix_b)):
                actions.append({"id": f"hi_b_{k}_{j}_{step_count}", "objectId": f"h_B_{k}_{j}", "type": "fade", "start": current_time, "end": current_time+0.5, "params": {"opacity": 0.3}})

            # Narrative & Calc Text
            if operation == "mult" or operation == "exp":
                calc_str = " + ".join([f"{matrix_a[i][k]}*{matrix_b[k][j]}" for k in range(len(matrix_a[0]))])
                narrative = f"Row {i+1} • Col {j+1}: {calc_str} = {matrix_c[i][j]}"
            else:
                narrative = f"{matrix_a[i][j]} + {matrix_b[i][j]} = {matrix_c[i][j]}"
            
            # Create temporary text for this step
            tid = f"txt_{step_count}"
            objects.append({"id": tid, "type": "text", "props": {"x": 400, "y": 400, "text": narrative, "font": "18px monospace", "color": "#cdd6f4", "opacity": 0}})
            actions.append({"id": f"show_{tid}", "objectId": tid, "type": "fade", "start": current_time, "end": current_time+0.5, "params": {"opacity": 1}, "narrative": narrative})
            
            # Reveal C cell
            actions.append({"id": f"show_c_{i}_{j}", "objectId": f"C_{i}_{j}", "type": "fade", "start": current_time + 1.0, "end": current_time + 1.5, "params": {"opacity": 1}})
            
            # Cleanup step
            actions.append({"id": f"hide_{tid}", "objectId": tid, "type": "fade", "start": current_time + 2.0, "end": current_time + 2.5, "params": {"opacity": 0}})
            for k in range(len(matrix_a[0])):
                actions.append({"id": f"unhi_a_{i}_{k}_{step_count}", "objectId": f"h_A_{i}_{k}", "type": "fade", "start": current_time + 2.0, "end": current_time + 2.5, "params": {"opacity": 0}})
            for k in range(len(matrix_b)):
                actions.append({"id": f"unhi_b_{k}_{j}_{step_count}", "objectId": f"h_B_{k}_{j}", "type": "fade", "start": current_time + 2.0, "end": current_time + 2.5, "params": {"opacity": 0}})
                
            current_time += step_duration
            step_count += 1
            
    # Reveal rest if any
    if step_count < rows_c * cols_c:
        for r in range(rows_c):
            for c in range(cols_c):
                actions.append({"id": f"final_show_c_{r}_{c}", "objectId": f"C_{r}_{c}", "type": "fade", "start": current_time, "end": current_time+1, "params": {"opacity": 1}})

    return {
        "sceneId": f"matrix_{rows}x{cols}_{operation}",
        "width": 800,
        "height": 450,
        "duration": current_time + 2,
        "code": f"# Matrix {operation}\nA = {matrix_a}\nB = {matrix_b}\nC = {operation}(A, B)",
        "objects": objects,
        "actions": actions
    }

def generate_quicksort_template(idx, difficulty="beginner", language="python"):
    """Generates a Quicksort partitioning visualization."""
    import random
    data = [random.randint(20, 90) for _ in range(7)]
    scene_id = f"algo_quicksort_{idx}"
    
    code_content = CodeGenerator.get_code("quicksort", language=language, level=difficulty)
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": "Quicksort: Partitioning", "font": "bold 32px Inter", "color": "#89b4fa", "textAlign": "center"}},
    ]
    
    bar_w, gap = 50, 15
    start_x = (800 - (len(data)*(bar_w+gap))) / 2
    
    for i, val in enumerate(data):
        objects.append({"id": f"bar_{i}", "type": "rect", "props": {"x": start_x + i*(bar_w+gap), "y": 400 - val*3.5, "width": bar_w, "height": val*3.5, "color": "#89b4fa"}})
        objects.append({"id": f"txt_{i}", "type": "text", "props": {"x": start_x + i*(bar_w+gap) + bar_w/2, "y": 400 - val*3.5 - 10, "text": str(val), "font": "16px monospace", "color": "#fff", "textAlign": "center"}})
        
    pivot_idx = len(data) - 1
    actions = [
        {"id": "hl_pivot", "objectId": f"bar_{pivot_idx}", "type": "fade", "start": 1, "end": 2, "params": {"color": "#f38ba8"}, "narrative": f"Pick {data[pivot_idx]} as the pivot."},
    ]
    
    i = -1
    for j in range(len(data) - 1):
        actions.append({"id": f"scan_{j}", "objectId": f"bar_{j}", "type": "fade", "start": 3 + j*2, "end": 4 + j*2, "params": {"color": "#fab387"}, "narrative": f"Compare {data[j]} with pivot."})
        if data[j] <= data[pivot_idx]:
            i += 1
            if i != j:
                actions.append({"id": f"swap_{j}", "objectId": f"bar_{j}", "type": "translate", "start": 4 + j*2, "end": 5 + j*2, "params": {"to": {"x": start_x + i*(bar_w+gap), "y": 400 - data[j]*3.5}}, "narrative": "Swap into left side."})
                actions.append({"id": f"swap_t_{j}", "objectId": f"txt_{j}", "type": "translate", "start": 4 + j*2, "end": 5 + j*2, "params": {"to": {"x": start_x + i*(bar_w+gap) + bar_w/2, "y": 400 - data[j]*3.5 - 10}}})

    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": 18, "code": code_content, "objects": objects, "actions": actions}

def generate_graph_algo_template(idx, algo="dijkstra", difficulty="beginner", language="python"):
    """Generates a Dijkstra pathfinding visualization."""
    scene_id = f"graph_{algo}_{idx}"
    
    code_content = CodeGenerator.get_code(algo, language=language, level=difficulty)
    nodes = [{"id": "A", "x": 100, "y": 225}, {"id": "B", "x": 300, "y": 100}, {"id": "C", "x": 300, "y": 350}, {"id": "D", "x": 500, "y": 225}, {"id": "E", "x": 700, "y": 225}]
    edges = [("A", "B", 4), ("A", "C", 2), ("B", "C", 5), ("B", "D", 10), ("C", "D", 3), ("D", "E", 1)]
    objects = [{"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}}, {"id": "title", "type": "text", "props": {"x": 400, "y": 40, "text": "Dijkstra's Shortest Path", "font": "bold 28px Inter", "color": "#89b4fa", "textAlign": "center"}}]
    for u_id, v_id, w in edges:
        u, v = next(n for n in nodes if n["id"] == u_id), next(n for n in nodes if n["id"] == v_id)
        objects.append({"id": f"e_{u_id}_{v_id}", "type": "path", "props": {"d": f"M {u['x']} {u['y']} L {v['x']} {v['y']}", "color": "#45475a", "width": 3}})
        objects.append({"id": f"w_{u_id}_{v_id}", "type": "text", "props": {"x": (u['x']+v['x'])/2, "y": (u['y']+v['y'])/2 - 10, "text": str(w), "font": "14px monospace", "color": "#fff"}})
    for n in nodes:
        objects.append({"id": f"n_{n['id']}", "type": "circle", "props": {"x": n['x'], "y": n['y'], "r": 25, "color": "#313244"}})
        objects.append({"id": f"l_{n['id']}", "type": "text", "props": {"x": n['x'], "y": n['y']+8, "text": n['id'], "font": "bold 20px Inter", "color": "#fff", "textAlign": "center"}})
        objects.append({"id": f"d_{n['id']}", "type": "text", "props": {"x": n['x'], "y": n['y']+50, "text": "∞", "font": "14px monospace", "color": "#89b4fa", "textAlign": "center"}})
    actions = [{"id": "a1", "objectId": "d_A", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}, "narrative": "Start at Node A."}, {"id": "a2", "objectId": "n_A", "type": "fade", "start": 1, "end": 2, "params": {"color": "#a6e3a1"}}, {"id": "a3", "objectId": "n_C", "type": "fade", "start": 3, "end": 4, "params": {"color": "#fab387"}, "narrative": CodeGenerator.get_narrative(f"{algo}_update", "C", "2", language=language, level=difficulty)}]
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": 12, "code": code_content, "objects": objects, "actions": actions}

def generate_fractal_template(idx, fractal="koch"):
    """Generates a recursive fractal visualization."""
    scene_id = f"fractal_{fractal}_{idx}"
    objects = [{"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}}, {"id": "snowflake", "type": "path", "props": {"d": "M 200 300 L 600 300 L 400 50 Z", "color": "#89b4fa", "width": 2}}]
    actions = [{"id": "f1", "objectId": "snowflake", "type": "scale", "start": 1, "end": 5, "params": {"scale": 1.2}, "narrative": "Adding recursive complexity to form the Koch Snowflake."}]
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": 10, "code": "def koch(L, depth):\n   if depth == 0: draw(L)", "objects": objects, "actions": actions}

def generate_ai_template(idx, model="neural_net"):
    """Generates an AI/ML concept visualization."""
    scene_id = f"ai_{model}_{idx}"
    objects = [{"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}}]
    # Simple 3-layer net
    lyrs = [2, 3, 1]
    for l, n_cnt in enumerate(lyrs):
        for i in range(n_cnt):
            objects.append({"id": f"n_{l}_{i}", "type": "circle", "props": {"x": 200 + l*200, "y": 100 + i*100 + (3-n_cnt)*50, "r": 20, "color": "#cba6f7"}})
    actions = [{"id": "fw", "objectId": "bg", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}, "narrative": "Signals flow through weights to produce a prediction."}]
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": 10, "code": "y = activation(Wx + b)", "objects": objects, "actions": actions}


def generate_advanced_math_template(topic):
    """Generates templates for advanced math concepts."""
    scene_id = f"adv_{topic.lower().replace(' ', '_')}"
    objects = [{"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#111"}}]
    actions = []
    code = ""
    
    if topic == "Determinant":
        # 2x2 Determinant visualization
        a, b, c, d = 3, 2, 1, 4
        det = a*d - b*c
        code = f"|{a} {b}|\n|{c} {d}| = {a}*{d} - {b}*{c} = {det}"
        objects.append({"id": "mat", "type": "text", "props": {"x": 400, "y": 150, "text": f"| {a}  {b} |", "font": "40px monospace", "color": "#fff"}})
        objects.append({"id": "mat2", "type": "text", "props": {"x": 400, "y": 200, "text": f"| {c}  {d} |", "font": "40px monospace", "color": "#fff"}})
        objects.append({"id": "calc", "type": "text", "props": {"x": 400, "y": 300, "text": f"Det = ({a})({d}) - ({b})({c})", "font": "24px monospace", "color": "#89b4fa", "opacity": 0}})
        objects.append({"id": "res", "type": "text", "props": {"x": 400, "y": 350, "text": f"= {det}", "font": "30px monospace", "color": "#a6e3a1", "opacity": 0}})
        actions.append({"id": "s1", "objectId": "calc", "type": "fade", "start": 1, "end": 2, "params": {"opacity": 1}})
        actions.append({"id": "s2", "objectId": "res", "type": "fade", "start": 2.5, "end": 3.5, "params": {"opacity": 1}})

    elif topic == "Gradient Descent":
        # Ball rolling down a curve with tangent line
        path_d = "M 100 100 Q 400 400 700 100"
        objects.append({"id": "curve", "type": "path", "props": {"d": path_d, "color": "#89b4fa", "width": 3}})
        objects.append({"id": "ball", "type": "circle", "props": {"x": 100, "y": 100, "r": 12, "color": "#e74c3c"}})
        # Tangent line
        objects.append({"id": "tangent", "type": "rect", "props": {"x": 100, "y": 100, "width": 60, "height": 2, "color": "#f9e2af", "rotation": 45, "opacity": 0}})
        
        actions.append({"id": "roll", "objectId": "ball", "type": "followPath", "start": 0.5, "end": 4.5, "params": {"pathId": "curve", "duration": 4}, "narrative": "The algorithm iteratively moves towards the minimum."})
        actions.append({"id": "show_tan", "objectId": "tangent", "type": "fade", "start": 0.5, "end": 1, "params": {"opacity": 1}})
        actions.append({"id": "move_tan", "objectId": "tangent", "type": "followPath", "start": 0.5, "end": 4.5, "params": {"pathId": "curve", "duration": 4}})
        code = "w = w - lr * gradient"

    elif topic == "Fourier Transform":
        # Sum of sines with individual components shown first
        code = "F(k) = ∫ f(x)e^(-2πikx) dx"
        objects.append({"id": "sig1", "type": "path", "props": {"d": "M 0 225 Q 200 125 400 225 T 800 225", "color": "#3498db", "width": 2, "opacity": 0}})
        objects.append({"id": "sig2", "type": "path", "props": {"d": "M 0 225 Q 100 175 200 225 T 400 225 T 600 225 T 800 225", "color": "#e74c3c", "width": 2, "opacity": 0}})
        objects.append({"id": "sum", "type": "path", "props": {"d": "M 0 225 Q 200 100 400 225 T 800 225", "color": "#fff", "width": 4, "opacity": 0}})
        
        actions.append({"id": "show_s1", "objectId": "sig1", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 0.6}, "narrative": "Component 1: Low frequency."})
        actions.append({"id": "show_s2", "objectId": "sig2", "type": "fade", "start": 2, "end": 3, "params": {"opacity": 0.6}, "narrative": "Component 2: High frequency."})
        actions.append({"id": "show_sum", "objectId": "sum", "type": "fade", "start": 3.5, "end": 5, "params": {"opacity": 1}, "narrative": "The Fourier Transform decomposes the signal into these frequencies."})

    elif topic == "Riemann Sum":
        # Rectangles under curve with sequential growth
        code = "Area ≈ Σ f(x_i)Δx"
        path_d = "M 100 350 Q 400 50 700 350"
        objects.append({"id": "curve", "type": "path", "props": {"d": path_d, "color": "#fff", "width": 2}})
        for i in range(10):
            h = random.randint(50, 200) # In reality should follow curve, but random for visual effect ok
            # Better approximation for visual
            x_pos = 100 + i*60
            # Simple parabolic height approx: y = -0.003(x-400)^2 + 300
            h_approx = -0.003 * ((x_pos + 30) - 400)**2 + 300
            
            objects.append({"id": f"r{i}", "type": "bar", "props": {"x": x_pos, "y": 350-h_approx, "width": 55, "height": h_approx, "color": "#3498db", "opacity": 0}})
            actions.append({"id": f"s{i}", "objectId": f"r{i}", "type": "fade", "start": 0.5 + i*0.3, "end": 1 + i*0.3, "params": {"opacity": 0.7}})
        
        actions.append({"id": "narr", "objectId": "curve", "type": "fade", "start": 0, "end": 0.1, "params": {"opacity": 1}, "narrative": "Approximating the area under the curve using rectangles."})

    elif topic == "Taylor Series":
        code = "f(x) = Σ f^n(a)/n! (x-a)^n"
        objects.append({"id": "eq", "type": "text", "props": {"x": 400, "y": 225, "text": "f(x) ≈ P(x)", "font": "40px Arial", "color": "#fff"}})
        actions.append({"id": "zoom", "objectId": "eq", "type": "scale", "start": 0, "end": 3, "params": {"scale": 1.5}})

    # ... Add more as needed to reach 10
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": 6,
        "code": code,
        "objects": objects,
        "actions": actions
    }

# --- GENERATE LIBRARIES ---

GEOMETRY_TEMPLATES = [generate_polygon_template(n) for n in range(3, 54)] # 51 templates

FORMULAS = [
    ("Area of Circle", "A = πr²", "Area is pi times radius squared"),
    ("Circumference", "C = 2πr", "Circumference is 2 pi r"),
    ("Pythagorean Thm", "a² + b² = c²", "For right triangles"),
    ("Quadratic Formula", "x = (-b ± √(b²-4ac))/2a", "Solves ax² + bx + c = 0"),
    ("Euler's Identity", "e^(iπ) + 1 = 0", "The most beautiful equation"),
    ("Newton's 2nd Law", "F = ma", "Force equals mass times acceleration"),
    ("Einstein's Mass-Energy", "E = mc²", "Energy equals mass times light speed squared"),
    ("Logarithm Rule", "log(ab) = log(a) + log(b)", "Log of product is sum of logs"),
    ("Derivative Power", "d/dx x^n = nx^(n-1)", "Power rule"),
    ("Integration Power", "∫x^n dx = x^(n+1)/(n+1)", "Power rule for integrals"),
    ("Trig Identity 1", "sin²θ + cos²θ = 1", "Fundamental identity"),
    ("Trig Identity 2", "tan θ = sin θ / cos θ", "Definition of tangent"),
    ("Ohm's Law", "V = IR", "Voltage equals Current times Resistance"),
    ("Kinetic Energy", "KE = ½mv²", "Energy of motion"),
    ("Potential Energy", "PE = mgh", "Gravitational potential energy"),
    ("Ideal Gas Law", "PV = nRT", "Pressure Volume relation"),
    ("Wave Equation", "v = fλ", "Velocity equals frequency times wavelength"),
    ("Density", "ρ = m/V", "Density is mass per volume"),
    ("Pressure", "P = F/A", "Pressure is Force per Area"),
    ("Work", "W = Fd", "Work is Force times distance"),
    ("Power", "P = W/t", "Power is Work per time"),
    ("Momentum", "p = mv", "Momentum is mass times velocity"),
    ("Impulse", "J = FΔt", "Impulse is Force times time change"),
    ("Centripetal Force", "Fc = mv²/r", "Force keeping object in circle"),
    ("Gravitation", "F = G(m1m2)/r²", "Universal gravitation"),
    ("Coulomb's Law", "F = k(q1q2)/r²", "Electrostatic force"),
    ("Snell's Law", "n1 sinθ1 = n2 sinθ2", "Refraction of light"),
    ("Lens Equation", "1/f = 1/do + 1/di", "Optics formula"),
    ("Magnification", "m = -di/do", "Image magnification"),
    ("Heat Energy", "Q = mcΔT", "Specific heat capacity"),
    ("Entropy", "S = k ln W", "Boltzmann's entropy formula"),
    ("Half-life", "N(t) = N0(1/2)^(t/T)", "Radioactive decay"),
    ("pH", "pH = -log[H+]", "Acidity measure"),
    ("Molarity", "M = n/V", "Concentration"),
    ("Avogadro's Law", "V1/n1 = V2/n2", "Volume and moles"),
    ("Boyle's Law", "P1V1 = P2V2", "Pressure and Volume"),
    ("Charles's Law", "V1/T1 = V2/T2", "Volume and Temperature"),
    ("Gay-Lussac's Law", "P1/T1 = P2/T2", "Pressure and Temperature"),
    ("Combined Gas Law", "P1V1/T1 = P2V2/T2", "Gas variables"),
    ("Hooke's Law", "F = -kx", "Spring force"),
    ("Elastic PE", "PE = ½kx²", "Spring energy"),
    ("Period of Pendulum", "T = 2π√(L/g)", "Time for one swing"),
    ("Period of Spring", "T = 2π√(m/k)", "Time for one oscillation"),
    ("Doppler Effect", "f' = f(v+vo)/(v-vs)", "Frequency shift"),
    ("Beat Frequency", "fb = |f1 - f2|", "Interference beats"),
    ("Capacitance", "C = Q/V", "Charge storage"),
    ("Resistors Series", "Req = R1 + R2", "Total resistance"),
    ("Resistors Parallel", "1/Req = 1/R1 + 1/R2", "Total resistance"),
    ("Transformers", "Vp/Vs = Np/Ns", "Voltage stepping"),
    ("Escape Velocity", "v = √(2GM/R)", "Speed to leave planet"),
    ("Bernoullis Principle", "P + ½ρv² + ρgh = C", "Fluid dynamics conservation"),
    ("Archimedes Principle", "Fb = ρgV", "Buoyant force = displaced weight"),
    ("Pascals Principle", "P = F1/A1 = F2/A2", "Pressure transmission"),
    ("Torricellis Law", "v = √(2gh)", "Speed of fluid efflux"),
    ("Youngs Modulus", "E = σ/ε", "Stress over strain"),
    ("Stefan Boltzmann Law", "P = σAT⁴", "Black body radiation"),
    ("Wiens Displacement", "λmax T = b", "Peak wavelength vs Temp"),
    ("Hubbles Law", "v = H0 d", "Galaxy recession velocity"),
    ("Schwarzschild Radius", "Rs = 2GM/c²", "Black hole event horizon"),
    ("De Broglie Wavelength", "λ = h/p", "Wave-particle duality"),
    ("Heisenberg Uncertainty", "ΔxΔp ≥ h/4π", "Quantum precision limit"),
    ("Lens Makers Eq", "1/f = (n-1)(1/R1 - 1/R2)", "Focal length of lens"),
    ("Malus Law", "I = I0 cos²θ", "Polarized light intensity"),
    ("Braggs Law", "nλ = 2d sinθ", "X-ray diffraction"),
    ("Rydberg Formula", "1/λ = R(1/n1² - 1/n2²)", "Atomic spectral lines"),
    ("Plancks Law", "E = hf", "Energy of photon"),
    ("Photoelectric Effect", "Kmax = hf - Φ", "Light ejecting electrons"),
    ("Compton Shift", "Δλ = h/mc(1-cosθ)", "Photon scattering"),
    ("Bohr Quantization", "L = nħ", "Angular momentum quantization"),
    ("Keplers 3rd Law", "T² ∝ a³", "Planetary orbital period"),
    ("Grav Potential", "U = -GMm/r", "Gravitational potential energy"),
    ("Damped Oscillation", "x(t) = Ae^(-bt/2m)cos(ωt)", "Decaying vibration"),
    ("Continuity Eq", "A1v1 = A2v2", "Fluid flow conservation"),
    ("Reynolds Number", "Re = ρvL/μ", "Flow turbulence predictor"),
    ("Stokes Law", "Fd = 6πμrv", "Viscous drag force"),
    ("Van der Waals", "(P + an²/V²)(V-nb) = nRT", "Real gas equation"),
    ("First Law Thermo", "ΔU = Q - W", "Energy conservation"),
    ("Carnot Efficiency", "η = 1 - Tc/Th", "Max heat engine efficiency"),
    ("Gibbs Free Energy", "G = H - TS", "Spontaneity of reaction"),
    ("Nernst Equation", "E = E0 - (RT/nF)lnQ", "Cell potential"),
    ("Faradays Law", "ε = -dΦ/dt", "Electromagnetic induction"),
    ("Amperes Law", "∮B·dl = μ0I", "Magnetic field from current"),
    ("Biot Savart Law", "dB = (μ0I dl x r)/4πr³", "Magnetic field point source"),
    ("Gauss Law Elec", "∮E·dA = Q/ε0", "Electric flux and charge"),
    ("Gauss Law Mag", "∮B·dA = 0", "No magnetic monopoles"),
    ("Lorentz Force", "F = q(E + v x B)", "EM force on charge"),
    ("Poynting Vector", "S = (1/μ0)E x B", "EM energy flow"),
    ("Time Dilation", "t' = t/√(1-v²/c²)", "Relativistic time"),
    ("Length Contraction", "L' = L√(1-v²/c²)", "Relativistic length"),
    ("Relativistic Mass", "m = m0/√(1-v²/c²)", "Mass increase with speed"),
    ("Lorentz Transform", "x' = γ(x - vt)", "Space-time coordinate shift"),
    ("Schrodinger Equation", "iħ∂Ψ/∂t = ĤΨ", "Quantum wave equation"),
    ("Dirac Equation", "(iγ·∂ - m)ψ = 0", "Relativistic quantum mechanics"),
    ("Maxwell Boltzmann", "f(v) ~ v²e^(-mv²/2kT)", "Gas particle speeds"),
    ("Fermi Dirac", "f(E) = 1/(1 + e^((E-μ)/kT))", "Fermion distribution"),
    ("Bose Einstein", "f(E) = 1/(e^((E-μ)/kT) - 1)", "Boson distribution"),
    ("Mean Free Path", "λ = 1/(√2πd²n)", "Avg distance between collisions"),
    ("Heat Conduction", "q = -k∇T", "Fourier's law of heat"),
    ("Heat Diffusion", "∂T/∂t = α∇²T", "Temperature change over time"),
    ("Wave Equation", "∂²u/∂t² = c²∇²u", "Propagation of waves"),
    ("Sound Intensity", "I = P/A", "Sound power per area"),
    ("Decibel Scale", "β = 10log(I/I0)", "Logarithmic sound level"),
    ("Mach Number", "M = v/c", "Speed relative to sound"),
    ("Moment of Inertia", "I = Σmr²", "Rotational inertia"),
    ("Parallel Axis", "I = Icm + Md²", "Inertia about offset axis"),
    ("Torque", "τ = r x F", "Rotational force"),
    ("Angular Momentum", "L = Iω", "Rotational momentum"),
    ("Rotational KE", "KE = ½Iω²", "Energy of rotation"),
    ("Rocket Equation", "Δv = ve ln(m0/mf)", "Tsiolkovsky rocket equation"),
    ("Center of Mass", "R = (1/M)Σmiri", "Balance point of system"),
    ("Elastic Collision", "v1' = (m1-m2)/(m1+m2)v1", "Bounce without energy loss"),
    ("Friction Static", "Fs ≤ μsN", "Force resisting motion start"),
    ("Friction Kinetic", "Fk = μkN", "Force resisting sliding"),
    ("Drag Equation", "Fd = ½ρv²CdA", "Air resistance"),
    ("Terminal Velocity", "vt = √(2mg/ρACd)", "Max falling speed"),
    ("Surface Tension", "γ = F/L", "Liquid surface force"),
    ("Capillary Action", "h = 2γcosθ/ρgr", "Liquid rise in tube"),
    ("Newton's Laws", "F = ma", "Laws of motion"),
    ("Friction", "F = μN", "Resistive force"),
    ("Work Energy Principle", "W = ΔKE", "Work changes energy"),
    ("Solar System", "F = GMm/r²", "Planetary orbits"),
    ("Life Cycle of Star", "E = mc²", "Stellar evolution"),
    ("Carbon Cycle", "C Cycle", "Carbon flow in nature"),
    ("Nitrogen Cycle", "N Cycle", "Nitrogen flow in nature"),
    ("Greenhouse Effect", "T_surf > T_eff", "Heat trapping"),
    ("Global Warming", "ΔT > 0", "Rising temperatures"),
    ("Water Cycle", "H2O Cycle", "Evaporation and rain"),
    ("Photosynthesis", "6CO2 + 6H2O -> C6H12O6 + 6O2", "Plant energy"),
    ("Respiration", "C6H12O6 + 6O2 -> 6CO2 + 6H2O", "Cellular energy"),
    ("Digestive System", "Digestion", "Food processing"),
    ("Human Heart", "Cardiac Cycle", "Blood pumping"),
    ("Nervous System", "Signal", "Neural transmission"),
    ("Electricity Basics", "V = IR", "Current flow"),
    ("Reflection Refraction", "n1sinθ1 = n2sinθ2", "Light bending"),
    ("Sound Propagation", "v = √(B/ρ)", "Sound waves"),
    ("States of Matter", "PV = nRT", "Solid, Liquid, Gas"),
    ("Force and Pressure", "P = F/A", "Force distribution")
]
MATH_TEMPLATES = [generate_formula_template(n, f, d) for n, f, d in FORMULAS] # 50 templates

VECTOR_TEMPLATES = [generate_vector_template(i) for i in range(50)] # 50 templates

FUNCTIONS = [
    ("x^2", "x**2"), ("x^3", "x**3"), ("sin(x)", "sin(x)"), ("cos(x)", "cos(x)"), ("tan(x)", "tan(x)"),
    ("exp(x)", "exp(x)"), ("sqrt(x)", "sqrt(x)"), ("1/x", "1/x"), ("-x^2", "-x**2"), ("abs(x)", "abs(x)"),
    ("x", "x"), ("2x", "2*x"), ("x/2", "x/2"), ("sin(2x)", "sin(2*x)"), ("cos(2x)", "cos(2*x)"),
    ("x^2+1", "x**2+1"), ("x^2-1", "x**2-1"), ("sin(x)+x", "sin(x)+x"), ("cos(x)*x", "cos(x)*x"), ("exp(-x)", "exp(-x)"),
    ("log(x)", "math.log(x) if x>0 else 0"), ("sigmoid", "1/(1+exp(-x))"), ("relu", "max(0, x)"), ("step", "1 if x>0 else 0"), ("sign", "1 if x>0 else -1"),
    ("x^4", "x**4"), ("x^5", "x**5"), ("sin(x)/x", "sin(x)/x if x!=0 else 1"), ("cos(x)/x", "cos(x)/x if x!=0 else 0"), ("x*sin(x)", "x*sin(x)"),
    ("x*cos(x)", "x*cos(x)"), ("x^2*sin(x)", "x**2*sin(x)"), ("sqrt(x+1)", "sqrt(x+1) if x>-1 else 0"), ("1/(1+x^2)", "1/(1+x**2)"), ("gauss", "exp(-x**2)"),
    ("sinc", "sin(x)/x if x!=0 else 1"), ("tanh", "math.tanh(x)"), ("sinh", "math.sinh(x)"), ("cosh", "math.cosh(x)"), ("floor", "math.floor(x)"),
    ("ceil", "math.ceil(x)"), ("round", "round(x)"), ("x%1", "x%1"), ("x^3-x", "x**3-x"), ("x^4-x^2", "x**4-x**2"),
    ("sin(x)+cos(x)", "sin(x)+cos(x)"), ("sin(x)-cos(x)", "sin(x)-cos(x)"), ("sin(x)*cos(x)", "sin(x)*cos(x)"), ("sin(x^2)", "sin(x**2)"), ("cos(x^2)", "cos(x**2)")
]
GRAPH_TEMPLATES = [generate_graph_template(n, e) for n, e in FUNCTIONS] # 50 templates

DERIVATION_TEMPLATES = [generate_derivation_template(i) for i in range(50)] # 50 templates

ALGO_TEMPLATES = [generate_algo_template(i) for i in range(50)] # 50 templates

SCIENTIFIC_TEMPLATES = [generate_atom_template(i) for i in range(1, 51)] # 50 templates

# Master Dictionary
GENERATED_TEMPLATES = {}
for t in GEOMETRY_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in MATH_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in VECTOR_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in GRAPH_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in DERIVATION_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in ALGO_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in SCIENTIFIC_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t

# New Advanced Topics
QUICK_TEMPLATES = [generate_quicksort_template(i) for i in range(20)]
GRAPH_ALGO_TEMPLATES = [generate_graph_algo_template(i) for i in range(20)]
FRACTAL_TEMPLATES = [generate_fractal_template(i) for i in range(20)]
AI_TEMPLATES = [generate_ai_template(i) for i in range(20)]

for t in QUICK_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in GRAPH_ALGO_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in FRACTAL_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t
for t in AI_TEMPLATES: GENERATED_TEMPLATES[t["sceneId"]] = t

def get_generated_template(key):
    return GENERATED_TEMPLATES.get(key)

def generate_full_course_template():
    """Generates a master template combining all formula animations."""
    combined_objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}}
    ]
    combined_actions = []
    
    current_time = 0
    topic_duration = 10 # Base duration per topic
    
    # Intro
    combined_objects.append({"id": "intro_title", "type": "text", "props": {"x": 400, "y": 225, "text": "DevForge Full Course", "font": "bold 40px Inter", "color": "#fff", "opacity": 0}})
    combined_actions.append({"id": "intro_in", "objectId": "intro_title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}})
    combined_actions.append({"id": "intro_out", "objectId": "intro_title", "type": "fade", "start": 3.5, "end": 4.5, "params": {"opacity": 0}})
    current_time += 5
    
    # Iterate through selected formulas (subset to avoid 10 min video if needed, but user asked for full)
    # Let's take the new ones we added + some classics
    # The user listed specific topics in the prompt. Let's try to match those.
    
    target_topics = [
        "Newton's Laws", "Friction", "Work Energy Principle", "Solar System", "Life Cycle of Star",
        "Carbon Cycle", "Nitrogen Cycle", "Greenhouse Effect", "Global Warming", "Water Cycle",
        "Photosynthesis", "Respiration", "Digestive System", "Human Heart", "Nervous System",
        "Electricity Basics", "Ohm's Law", "Reflection Refraction", "Sound Propagation",
        "States of Matter", "Force and Pressure"
    ]
    
    for i, topic in enumerate(target_topics):
        # Find formula data
        formula_data = next((f for f in FORMULAS if f[0] == topic), None)
        if not formula_data:
            # Fallback for topics not in FORMULAS but handled in get_formula_simulation
            formula_data = (topic, "", topic)
            
        name, eqn, desc = formula_data
        
        # Generate template
        tmpl = generate_formula_template(name, eqn, desc)
        
        # Prefix for uniqueness
        prefix = f"t{i}_"
        
        # Add Objects (skip bg)
        for obj in tmpl["objects"]:
            if obj["id"] == "bg": continue
            
            new_obj = obj.copy()
            new_obj["id"] = prefix + obj["id"]
            
            # Adjust props if needed (e.g. opacity 0 to start)
            # Most templates start with opacity 0 or are faded in.
            # If an object starts visible, we should probably hide it initially.
            if "opacity" not in new_obj["props"]:
                new_obj["props"]["opacity"] = 0
            
            combined_objects.append(new_obj)
            
        # Add Actions with time offset
        for act in tmpl["actions"]:
            new_act = act.copy()
            new_act["id"] = prefix + act["id"]
            new_act["objectId"] = prefix + act["objectId"]
            new_act["start"] += current_time
            new_act["end"] += current_time
            
            # Handle pathId for followPath
            if "params" in new_act and "pathId" in new_act["params"]:
                new_act["params"]["pathId"] = prefix + new_act["params"]["pathId"]
                
            combined_actions.append(new_act)
            
        # Transition out (Fade out all objects of this topic)
        # Find all objects for this topic
        topic_objs = [obj["id"] for obj in combined_objects if obj["id"].startswith(prefix)]
        for obj_id in topic_objs:
            combined_actions.append({
                "id": f"cleanup_{obj_id}",
                "objectId": obj_id,
                "type": "fade",
                "start": current_time + tmpl["duration"] - 1,
                "end": current_time + tmpl["duration"],
                "params": {"opacity": 0}
            })
            
        current_time += tmpl["duration"]
        
    return {
        "sceneId": "full_course",
        "width": 800,
        "height": 450,
        "duration": current_time,
        "code": "# Full Course Generated\n# Topics: " + ", ".join(target_topics),
        "objects": combined_objects,
        "actions": combined_actions
    }

def generate_search_template(idx, difficulty="beginner", language="python", target_val=None):
    """Generates a Binary Search visualization with difficulty levels."""
    import random
    
    # 1. Data Setup
    if difficulty == "kids":
       data = sorted([random.randint(1, 15) for _ in range(5)])
    else:
       data = sorted([random.randint(10, 99) for _ in range(9)])
       
    target = target_val if target_val else random.choice(data)
    n = len(data)
    
    scene_id = f"search_binary_{idx}"
    
    # 2. Code Content based on Difficulty, Language, and Skill Level
    code_content = CodeGenerator.get_code("binary_search", language=language, level=difficulty)
    
    # 3. Base Objects
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 50, "text": f"Binary Search: Finding {target}", "font": "bold 32px Inter", "color": "#89b4fa", "opacity": 0}},
    ]
    
    bar_width = 40
    gap = 10
    total_w = n * bar_width + (n-1) * gap
    start_x = (800 - total_w) / 2
    
    # Pointers
    objects.append({"id": "ptr_low", "type": "text", "props": {"x": start_x + bar_width/2, "y": 430, "text": "L", "font": "bold 20px monospace", "color": "#f9e2af", "opacity": 0}})
    objects.append({"id": "ptr_high", "type": "text", "props": {"x": start_x + (n-1)*(bar_width+gap) + bar_width/2, "y": 430, "text": "H", "font": "bold 20px monospace", "color": "#f9e2af", "opacity": 0}})
    objects.append({"id": "ptr_mid", "type": "text", "props": {"x": 400, "y": 150, "text": "M", "font": "bold 20px monospace", "color": "#e74c3c", "opacity": 0}}) # Initially hidden
    
    # Create Bar Objects
    for i, val in enumerate(data):
        h = val * 3
        x = start_x + i * (bar_width + gap)
        y = 400 - h
        color = "#89b4fa"
        
        objects.append({
            "id": f"bar_{i}", 
            "type": "rect", 
            "props": {"x": x, "y": y, "width": bar_width, "height": h, "color": color, "opacity": 0}
        })
        objects.append({
            "id": f"val_{i}", 
            "type": "text", 
            "props": {"x": x + bar_width/2, "y": y - 10, "text": str(val), "font": "16px monospace", "color": "#fff", "opacity": 0}
        })

    actions = [
        {"id": "show_title", "objectId": "title", "type": "fade", "start": 0.5, "end": 1.5, "params": {"opacity": 1}},
        {"id": "show_ptrs", "objectId": "ptr_low", "type": "fade", "start": 1.5, "end": 2.5, "params": {"opacity": 1}},
        {"id": "show_ptrs_h", "objectId": "ptr_high", "type": "fade", "start": 1.5, "end": 2.5, "params": {"opacity": 1}}
    ]

    # Show bars
    for i in range(n):
        actions.append({"id": f"show_bar_{i}", "objectId": f"bar_{i}", "type": "fade", "start": 1.0 + i*0.1, "end": 1.5 + i*0.1, "params": {"opacity": 1}})
        actions.append({"id": f"show_val_{i}", "objectId": f"val_{i}", "type": "fade", "start": 1.0 + i*0.1, "end": 1.5 + i*0.1, "params": {"opacity": 1}})

    # 4. Simulation
    low = 0
    high = n - 1
    found = False
    
    time = 3.0
    step_dur = 2.0
    
    while low <= high:
        # Calculate Mid
        mid = (low + high) // 2
        
        mid_x = start_x + mid * (bar_width + gap) + bar_width/2
        
        # Step 2: First Mid
        actions.append({
            "id": f"calc_mid_{time}", 
            "objectId": "ptr_mid", 
            "type": "translate", # Changed to translate to allow narrative
            "start": time, 
            "end": time + 0.5, 
            "params": {"to": {"x": mid_x, "y": 380 - data[mid]*3 - 30}}, 
            "narrative": CodeGenerator.get_narrative("binary_mid", data[mid], language=language, level=difficulty), 
            "codeLine": 4 if difficulty == "beginner" else (2 if difficulty == "kids" else 3)
        })
        actions.append({"id": f"show_mid_{time}", "objectId": "ptr_mid", "type": "fade", "start": time, "end": time + 0.5, "params": {"opacity": 1}})
        time += 0.5
        
        # Highlight Mid Bar
        mid_bar_id = f"bar_{mid}"
        actions.append({"id": f"hi_mid_{time}", "objectId": mid_bar_id, "type": "color", "start": time, "end": time + 0.5, "params": {"color": "#e74c3c"}})
        
        if data[mid] == target_val:
            actions.append({
                "id": f"found_{time}",
                "objectId": mid_bar_id,
                "type": "color", 
                "start": time, 
                "end": time + 1.0, 
                "params": {"color": "#a6e3a1"}, 
                "narrative": f"Found target {target_val} at index {mid}!" if difficulty != "kids" else "We found it! Yay!",
                "codeLine": 6 if difficulty == "beginner" else (3 if difficulty == "kids" else 6)
            })
            found = True
            break
        elif data[mid] < target_val:
            narr = f"{data[mid]} < {target_val}, so ignore left half." if difficulty != "kids" else "Too small! Look to the right."
            ln = 8 if difficulty == "beginner" else (2 if difficulty == "kids" else 8)
            actions.append({
                "id": f"narr_low_{time}",
                "objectId": "title",
                "type": "wait",
                "start": time,
                "end": time + step_dur,
                "narrative": narr,
                "codeLine": ln
            })
            
            # Grey out left half
            for i in range(low, mid + 1):
                actions.append({"id": f"grey_{i}_{time}", "objectId": f"bar_{i}", "type": "color", "start": time, "end": time + 1, "params": {"color": "#45475a"}})
                
            low = mid + 1
            # Move Low Ptr
            new_low_x = start_x + low * (bar_width + gap) + bar_width/2
            actions.append({"id": f"move_low_{time}", "objectId": "ptr_low", "type": "translate", "start": time + 1, "end": time + 1.5, "params": {"to": {"x": new_low_x}}})
            
        else:
            narr = f"{data[mid]} > {target_val}, so ignore right half." if difficulty != "kids" else "Too big! Look to the left."
            ln = 10 if difficulty == "beginner" else (2 if difficulty == "kids" else 10)
            actions.append({
                "id": f"narr_high_{time}",
                "objectId": "title",
                "type": "wait",
                "start": time,
                "end": time + step_dur,
                "narrative": narr,
                "codeLine": ln
            })
            
            # Grey out right half
            for i in range(mid, high + 1):
                actions.append({"id": f"grey_{i}_{time}", "objectId": f"bar_{i}", "type": "color", "start": time, "end": time + 1, "params": {"color": "#45475a"}})
                
            high = mid - 1
            # Move High Ptr
            new_high_x = start_x + high * (bar_width + gap) + bar_width/2
            actions.append({"id": f"move_high_{time}", "objectId": "ptr_high", "type": "translate", "start": time + 1, "end": time + 1.5, "params": {"to": {"x": new_high_x}}})

        time += 2.0
    
    if not found:
        actions.append({"id": "not_found", "objectId": "title", "type": "wait", "start": time, "end": time + 2, "narrative": "Target not found."})

    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 3,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

# ==========================================
# PHASE 1 ALGORITHMS (PART 1)
# ==========================================

def generate_fibonacci_template(idx, n=10, difficulty="beginner", language="python"):
    """
    Generates Fibonacci Sequence visualization using Dynamic Programming.
    Shows the classic sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34...
    """
    from code_generator import CodeGenerator
    
    scene_id = f"fibonacci_{idx}"
    code_content = CodeGenerator.get_code("fibonacci", language=language, level=difficulty)
    
    # Calculate Fibonacci sequence
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    # Base objects
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 40, "text": f"Fibonacci Sequence (n={n})", "font": "bold 28px Inter", "color": "#89b4fa"}},
    ]
    
    # Create boxes for each Fibonacci number
    box_width = 60
    box_height = 60
    start_x = 50
    start_y = 150
    gap = 10
    
    for i in range(n):
        x = start_x + i * (box_width + gap)
        if i >= 8:  # Wrap to second row
            x = start_x + (i - 8) * (box_width + gap)
            y = start_y + 100
        else:
            y = start_y
            
        objects.append({
            "id": f"box_{i}",
            "type": "rect",
            "props": {
                "x": x, "y": y, "width": box_width, "height": box_height,
                "color": "#313244", "opacity": 0
            }
        })
        objects.append({
            "id": f"num_{i}",
            "type": "text",
            "props": {
                "x": x + box_width/2, "y": y + box_height/2,
                "text": str(fib[i]), "font": "bold 20px monospace",
                "color": "#cdd6f4", "opacity": 0
            }
        })
    
    # Create actions
    actions = []
    time = 0.5
    
    # Show first two base cases
    actions.append({"id": "show_base_0", "objectId": "box_0", "type": "fade", "start": time, "end": time + 0.5, "params": {"opacity": 1}, "narrative": "Base case: F(0) = 0"})
    actions.append({"id": "show_num_0", "objectId": "num_0", "type": "fade", "start": time, "end": time + 0.5, "params": {"opacity": 1}})
    actions.append({"id": "highlight_0", "objectId": "box_0", "type": "color", "start": time, "end": time + 0.5, "params": {"color": "#a6e3a1"}})
    time += 1
    
    actions.append({"id": "show_base_1", "objectId": "box_1", "type": "fade", "start": time, "end": time + 0.5, "params": {"opacity": 1}, "narrative": "Base case: F(1) = 1"})
    actions.append({"id": "show_num_1", "objectId": "num_1", "type": "fade", "start": time, "end": time + 0.5, "params": {"opacity": 1}})
    actions.append({"id": "highlight_1", "objectId": "box_1", "type": "color", "start": time, "end": time + 0.5, "params": {"color": "#a6e3a1"}})
    time += 1
    
    # Calculate remaining Fibonacci numbers
    for i in range(2, n):
        # Show calculation
        narrative = f"F({i}) = F({i-1}) + F({i-2}) = {fib[i-1]} + {fib[i-2]} = {fib[i]}"
        
        # Highlight previous two numbers
        actions.append({"id": f"calc_{i}_prev1", "objectId": f"box_{i-1}", "type": "color", "start": time, "end": time + 0.5, "params": {"color": "#fab387"}, "narrative": narrative})
        actions.append({"id": f"calc_{i}_prev2", "objectId": f"box_{i-2}", "type": "color", "start": time, "end": time + 0.5, "params": {"color": "#fab387"}})
        time += 0.7
        
        # Show new number
        actions.append({"id": f"show_box_{i}", "objectId": f"box_{i}", "type": "fade", "start": time, "end": time + 0.5, "params": {"opacity": 1}})
        actions.append({"id": f"show_num_{i}", "objectId": f"num_{i}", "type": "fade", "start": time, "end": time + 0.5, "params": {"opacity": 1}})
        actions.append({"id": f"highlight_{i}", "objectId": f"box_{i}", "type": "color", "start": time, "end": time + 0.5, "params": {"color": "#a6e3a1"}})
        time += 0.5
        
        # Reset previous highlights
        actions.append({"id": f"reset_{i}_prev1", "objectId": f"box_{i-1}", "type": "color", "start": time, "end": time + 0.3, "params": {"color": "#313244"}})
        actions.append({"id": f"reset_{i}_prev2", "objectId": f"box_{i-2}", "type": "color", "start": time, "end": time + 0.3, "params": {"color": "#313244"}})
        time += 0.5
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }


def generate_counting_sort_template(idx, difficulty="beginner", language="python"):
    """
    Generates Counting Sort visualization.
    Linear time O(n+k) sorting algorithm for integers in a known range.
    """
    from code_generator import CodeGenerator
    import random
    
    scene_id = f"counting_sort_{idx}"
    code_content = CodeGenerator.get_code("counting_sort", language=language, level=difficulty)
    
    # Generate random array with small range
    data = [random.randint(0, 9) for _ in range(8)]
    n = len(data)
    max_val = max(data)
    
    # Base objects
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 40, "text": f"Counting Sort: {data}", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "label_input", "type": "text", "props": {"x": 100, "y": 100, "text": "Input Array:", "font": "16px Inter", "color": "#cdd6f4"}},
        {"id": "label_count", "type": "text", "props": {"x": 100, "y": 220, "text": "Count Array:", "font": "16px Inter", "color": "#cdd6f4"}},
        {"id": "label_output", "type": "text", "props": {"x": 100, "y": 340, "text": "Output Array:", "font": "16px Inter", "color": "#cdd6f4"}},
    ]
    
    # Input array bars
    bar_width = 40
    gap = 10
    start_x = 200
    
    for i in range(n):
        h = data[i] * 15 + 20
        x = start_x + i * (bar_width + gap)
        objects.append({
            "id": f"input_{i}",
            "type": "bar",
            "props": {"x": x, "y": 150, "width": bar_width, "height": h, "color": "#89b4fa", "text": str(data[i])}
        })
    
    # Count array (0-9)
    for i in range(max_val + 1):
        x = start_x + i * (bar_width + gap)
        objects.append({
            "id": f"count_{i}",
            "type": "bar",
            "props": {"x": x, "y": 270, "width": bar_width, "height": 20, "color": "#313244", "text": "0"}
        })
    
    # Output array
    for i in range(n):
        x = start_x + i * (bar_width + gap)
        objects.append({
            "id": f"output_{i}",
            "type": "bar",
            "props": {"x": x, "y": 390, "width": bar_width, "height": 20, "color": "#313244", "text": "", "opacity": 0}
        })
    
    # Create actions
    actions = []
    time = 0.5
    
    # Count occurrences
    count = [0] * (max_val + 1)
    for i, val in enumerate(data):
        count[val] += 1
        actions.append({
            "id": f"highlight_input_{i}",
            "objectId": f"input_{i}",
            "type": "color",
            "start": time,
            "end": time + 0.5,
            "params": {"color": "#f9e2af"},
            "narrative": f"Count occurrence of {val}"
        })
        
        # Update count array
        new_height = count[val] * 20 + 20
        actions.append({
            "id": f"update_count_{val}_{i}",
            "objectId": f"count_{val}",
            "type": "resize",
            "start": time + 0.3,
            "end": time + 0.8,
            "params": {"height": new_height, "text": str(count[val]), "color": "#a6e3a1"}
        })
        time += 1
    
    # Build output array
    time += 0.5
    output_idx = 0
    for val in range(max_val + 1):
        for _ in range(count[val]):
            h = val * 15 + 20
            actions.append({
                "id": f"place_output_{output_idx}",
                "objectId": f"output_{output_idx}",
                "type": "fade",
                "start": time,
                "end": time + 0.5,
                "params": {"opacity": 1, "height": h, "text": str(val), "color": "#a6e3a1"},
                "narrative": f"Place {val} in sorted position"
            })
            output_idx += 1
            time += 0.6
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

# ==========================================
# PHASE 1 ALGORITHMS (PART 2)
# ==========================================

def generate_bucket_sort_template(idx, difficulty="beginner", language="python"):
    """
    Generates Bucket Sort visualization.
    Distributes elements into buckets, sorts each bucket, then concatenates.
    """
    from code_generator import CodeGenerator
    import random
    
    scene_id = f"bucket_sort_{idx}"
    code_content = CodeGenerator.get_code("bucket_sort", language=language, level=difficulty)
    
    # Generate data in range 0-99
    data = [random.randint(0, 99) for _ in range(10)]
    n = len(data)
    num_buckets = 5
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": f"Bucket Sort: {data}", "font": "bold 22px Inter", "color": "#89b4fa"}},
    ]
    
    # Input array
    bar_width = 35
    gap = 8
    start_x = 100
    for i in range(n):
        h = data[i] + 20
        x = start_x + i * (bar_width + gap)
        objects.append({
            "id": f"input_{i}",
            "type": "bar",
            "props": {"x": x, "y": 120, "width": bar_width, "height": h, "color": "#89b4fa", "text": str(data[i])}
        })
    
    # Buckets
    bucket_y = 250
    bucket_width = 120
    for i in range(num_buckets):
        x = 50 + i * (bucket_width + 20)
        objects.append({
            "id": f"bucket_{i}",
            "type": "rect",
            "props": {"x": x, "y": bucket_y, "width": bucket_width, "height": 150, "color": "#313244", "opacity": 0.5}
        })
        objects.append({
            "id": f"bucket_label_{i}",
            "type": "text",
            "props": {"x": x + bucket_width/2, "y": bucket_y - 10, "text": f"[{i*20}-{(i+1)*20-1}]", "font": "12px Inter", "color": "#cdd6f4"}
        })
    
    actions = []
    time = 0.5
    
    # Distribute into buckets
    buckets = [[] for _ in range(num_buckets)]
    for i, val in enumerate(data):
        bucket_idx = min(val // 20, num_buckets - 1)
        buckets[bucket_idx].append(val)
        
        actions.append({
            "id": f"highlight_{i}",
            "objectId": f"input_{i}",
            "type": "color",
            "start": time,
            "end": time + 0.5,
            "params": {"color": "#f9e2af"},
            "narrative": f"Place {val} in bucket {bucket_idx}"
        })
        
        # Move to bucket
        target_x = 50 + bucket_idx * (bucket_width + 20) + 20
        target_y = bucket_y + 30 + len(buckets[bucket_idx]) * 25
        actions.append({
            "id": f"move_{i}",
            "objectId": f"input_{i}",
            "type": "translate",
            "start": time + 0.3,
            "end": time + 0.8,
            "params": {"to": {"x": target_x, "y": target_y}, "color": "#a6e3a1"}
        })
        time += 1
    
    # Sort and merge
    time += 0.5
    output_x = 100
    output_idx = 0
    for bucket_idx, bucket in enumerate(buckets):
        bucket.sort()
        for val in bucket:
            x = output_x + output_idx * (bar_width + gap)
            actions.append({
                "id": f"final_{output_idx}",
                "objectId": f"input_{data.index(val)}",
                "type": "translate",
                "start": time,
                "end": time + 0.5,
                "params": {"to": {"x": x, "y": 120}, "color": "#a6e3a1"},
                "narrative": "Merge sorted buckets"
            })
            output_idx += 1
            time += 0.4
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }


def generate_knapsack_template(idx, difficulty="beginner", language="python"):
    """
    Generates 0/1 Knapsack Problem visualization using Dynamic Programming.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"knapsack_{idx}"
    code_content = CodeGenerator.get_code("knapsack", language=language, level=difficulty)
    
    # Sample items: (weight, value)
    items = [(2, 3), (3, 4), (4, 5), (5, 6)]
    capacity = 8
    n = len(items)
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": f"0/1 Knapsack (Capacity={capacity})", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "label_items", "type": "text", "props": {"x": 100, "y": 70, "text": "Items (weight, value):", "font": "16px Inter", "color": "#cdd6f4"}},
    ]
    
    # Display items
    for i, (w, v) in enumerate(items):
        x = 100 + i * 100
        objects.append({
            "id": f"item_{i}",
            "type": "rect",
            "props": {"x": x, "y": 100, "width": 80, "height": 60, "color": "#313244"}
        })
        objects.append({
            "id": f"item_text_{i}",
            "type": "text",
            "props": {"x": x + 40, "y": 130, "text": f"W:{w}\nV:{v}", "font": "14px monospace", "color": "#cdd6f4"}
        })
    
    # DP table
    cell_size = 40
    table_start_x = 100
    table_start_y = 200
    
    for i in range(n + 1):
        for w in range(capacity + 1):
            x = table_start_x + w * cell_size
            y = table_start_y + i * cell_size
            objects.append({
                "id": f"cell_{i}_{w}",
                "type": "rect",
                "props": {"x": x, "y": y, "width": cell_size, "height": cell_size, "color": "#1e1e2e", "opacity": 0.3}
            })
            objects.append({
                "id": f"val_{i}_{w}",
                "type": "text",
                "props": {"x": x + cell_size/2, "y": y + cell_size/2, "text": "0", "font": "12px monospace", "color": "#cdd6f4", "opacity": 0}
            })
    
    # Create DP solution
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    actions = []
    time = 0.5
    
    for i in range(1, n + 1):
        w_item, v_item = items[i-1]
        for w in range(capacity + 1):
            if w_item <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-w_item] + v_item)
            else:
                dp[i][w] = dp[i-1][w]
            
            # Animate cell update
            actions.append({
                "id": f"show_{i}_{w}",
                "objectId": f"val_{i}_{w}",
                "type": "fade",
                "start": time,
                "end": time + 0.3,
                "params": {"opacity": 1, "text": str(dp[i][w])},
                "narrative": f"DP[{i}][{w}] = {dp[i][w]}"
            })
            actions.append({
                "id": f"highlight_{i}_{w}",
                "objectId": f"cell_{i}_{w}",
                "type": "color",
                "start": time,
                "end": time + 0.3,
                "params": {"color": "#a6e3a1", "opacity": 0.5}
            })
            time += 0.15
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }


def generate_lcs_template(idx, difficulty="beginner", language="python"):
    """
    Generates Longest Common Subsequence visualization.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"lcs_{idx}"
    code_content = CodeGenerator.get_code("lcs", language=language, level=difficulty)
    
    str1 = "AGGTAB"
    str2 = "GXTXAYB"
    m, n = len(str1), len(str2)
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": f"Longest Common Subsequence", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "str1_label", "type": "text", "props": {"x": 100, "y": 70, "text": f"String 1: {str1}", "font": "18px monospace", "color": "#f9e2af"}},
        {"id": "str2_label", "type": "text", "props": {"x": 100, "y": 100, "text": f"String 2: {str2}", "font": "18px monospace", "color": "#fab387"}},
    ]
    
    # DP table
    cell_size = 45
    start_x = 150
    start_y = 150
    
    for i in range(m + 1):
        for j in range(n + 1):
            x = start_x + j * cell_size
            y = start_y + i * cell_size
            objects.append({
                "id": f"cell_{i}_{j}",
                "type": "rect",
                "props": {"x": x, "y": y, "width": cell_size, "height": cell_size, "color": "#313244", "opacity": 0.3}
            })
            objects.append({
                "id": f"val_{i}_{j}",
                "type": "text",
                "props": {"x": x + cell_size/2, "y": y + cell_size/2, "text": "0", "font": "14px monospace", "color": "#cdd6f4", "opacity": 0}
            })
    
    # DP solution
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    actions = []
    time = 0.5
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                narrative = f"Match: {str1[i-1]} = {str2[j-1]}, LCS = {dp[i][j]}"
                color = "#a6e3a1"
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                narrative = f"No match, take max({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}"
                color = "#89b4fa"
            
            actions.append({
                "id": f"show_{i}_{j}",
                "objectId": f"val_{i}_{j}",
                "type": "fade",
                "start": time,
                "end": time + 0.3,
                "params": {"opacity": 1, "text": str(dp[i][j])},
                "narrative": narrative
            })
            actions.append({
                "id": f"highlight_{i}_{j}",
                "objectId": f"cell_{i}_{j}",
                "type": "color",
                "start": time,
                "end": time + 0.3,
                "params": {"color": color, "opacity": 0.5}
            })
            time += 0.2
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }


def generate_edit_distance_template(idx, difficulty="beginner", language="python"):
    """
    Generates Levenshtein Edit Distance visualization.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"edit_distance_{idx}"
    code_content = CodeGenerator.get_code("edit_distance", language=language, level=difficulty)
    
    str1 = "SUNDAY"
    str2 = "SATURDAY"
    m, n = len(str1), len(str2)
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Edit Distance (Levenshtein)", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "str1_label", "type": "text", "props": {"x": 100, "y": 70, "text": f"From: {str1}", "font": "18px monospace", "color": "#f9e2af"}},
        {"id": "str2_label", "type": "text", "props": {"x": 100, "y": 100, "text": f"To: {str2}", "font": "18px monospace", "color": "#fab387"}},
    ]
    
    # DP table
    cell_size = 40
    start_x = 100
    start_y = 150
    
    for i in range(m + 1):
        for j in range(n + 1):
            x = start_x + j * cell_size
            y = start_y + i * cell_size
            objects.append({
                "id": f"cell_{i}_{j}",
                "type": "rect",
                "props": {"x": x, "y": y, "width": cell_size, "height": cell_size, "color": "#313244", "opacity": 0.3}
            })
            objects.append({
                "id": f"val_{i}_{j}",
                "type": "text",
                "props": {"x": x + cell_size/2, "y": y + cell_size/2, "text": "", "font": "12px monospace", "color": "#cdd6f4", "opacity": 0}
            })
    
    # DP solution
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    actions = []
    time = 0.5
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                narrative = f"Match: {str1[i-1]} = {str2[j-1]}, no edit needed"
                color = "#a6e3a1"
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                narrative = f"Min edits: {dp[i][j]}"
                color = "#fab387"
            
            actions.append({
                "id": f"show_{i}_{j}",
                "objectId": f"val_{i}_{j}",
                "type": "fade",
                "start": time,
                "end": time + 0.3,
                "params": {"opacity": 1, "text": str(dp[i][j])},
                "narrative": narrative
            })
            actions.append({
                "id": f"highlight_{i}_{j}",
                "objectId": f"cell_{i}_{j}",
                "type": "color",
                "start": time,
                "end": time + 0.3,
                "params": {"color": color, "opacity": 0.5}
            })
            time += 0.15
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

# ==========================================
# PHASE 1 ALGORITHMS (PART 3)
# ==========================================

def generate_nqueens_template(idx, n=4, difficulty="beginner", language="python"):
    """
    Generates N-Queens Problem visualization using Backtracking.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"nqueens_{idx}"
    code_content = CodeGenerator.get_code("nqueens", language=language, level=difficulty)
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": f"{n}-Queens Problem", "font": "bold 28px Inter", "color": "#89b4fa"}},
    ]
    
    # Chessboard
    cell_size = 60
    board_start_x = 250
    board_start_y = 100
    
    for i in range(n):
        for j in range(n):
            x = board_start_x + j * cell_size
            y = board_start_y + i * cell_size
            color = "#313244" if (i + j) % 2 == 0 else "#45475a"
            objects.append({
                "id": f"cell_{i}_{j}",
                "type": "rect",
                "props": {"x": x, "y": y, "width": cell_size, "height": cell_size, "color": color}
            })
            objects.append({
                "id": f"queen_{i}_{j}",
                "type": "text",
                "props": {"x": x + cell_size/2, "y": y + cell_size/2, "text": "♛", "font": "40px Arial", "color": "#f9e2af", "opacity": 0}
            })
    
    # Backtracking solution (simplified for 4-queens)
    solution = [1, 3, 0, 2] if n == 4 else [0, 2, 4, 1, 3] if n == 5 else list(range(n))
    
    actions = []
    time = 0.5
    
    for col, row in enumerate(solution):
        # Try placing queen
        actions.append({
            "id": f"place_{col}_{row}",
            "objectId": f"queen_{row}_{col}",
            "type": "fade",
            "start": time,
            "end": time + 0.5,
            "params": {"opacity": 1},
            "narrative": f"Place queen at row {row}, col {col}"
        })
        
        # Highlight safe cell
        actions.append({
            "id": f"safe_{col}_{row}",
            "objectId": f"cell_{row}_{col}",
            "type": "color",
            "start": time,
            "end": time + 0.5,
            "params": {"color": "#a6e3a1"}
        })
        time += 1
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }


def generate_kruskal_mst_template(idx, difficulty="beginner", language="python"):
    """
    Generates Kruskal's Minimum Spanning Tree visualization.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"kruskal_mst_{idx}"
    code_content = CodeGenerator.get_code("kruskal_mst", language=language, level=difficulty)
    
    # Graph nodes
    nodes = [
        {"id": "A", "x": 200, "y": 150},
        {"id": "B", "x": 400, "y": 100},
        {"id": "C", "x": 600, "y": 150},
        {"id": "D", "x": 300, "y": 300},
        {"id": "E", "x": 500, "y": 300}
    ]
    
    # Edges with weights
    edges = [
        ("A", "B", 4), ("A", "D", 2), ("B", "C", 3),
        ("B", "D", 5), ("B", "E", 6), ("C", "E", 1),
        ("D", "E", 7)
    ]
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Kruskal's MST", "font": "bold 28px Inter", "color": "#89b4fa"}},
    ]
    
    # Draw edges
    for i, (u, v, w) in enumerate(edges):
        u_node = next(n for n in nodes if n["id"] == u)
        v_node = next(n for n in nodes if n["id"] == v)
        objects.append({
            "id": f"edge_{i}",
            "type": "line",
            "props": {"x1": u_node["x"], "y1": u_node["y"], "x2": v_node["x"], "y2": v_node["y"], "color": "#45475a", "width": 2}
        })
        mid_x = (u_node["x"] + v_node["x"]) / 2
        mid_y = (u_node["y"] + v_node["y"]) / 2
        objects.append({
            "id": f"weight_{i}",
            "type": "text",
            "props": {"x": mid_x, "y": mid_y, "text": str(w), "font": "14px monospace", "color": "#f9e2af"}
        })
    
    # Draw nodes
    for node in nodes:
        objects.append({
            "id": f"node_{node['id']}",
            "type": "circle",
            "props": {"x": node["x"], "y": node["y"], "radius": 25, "color": "#313244"}
        })
        objects.append({
            "id": f"label_{node['id']}",
            "type": "text",
            "props": {"x": node["x"], "y": node["y"], "text": node["id"], "font": "bold 18px Inter", "color": "#cdd6f4"}
        })
    
    # Sort edges by weight
    sorted_edges = sorted(enumerate(edges), key=lambda x: x[1][2])
    
    actions = []
    time = 0.5
    
    for edge_idx, (u, v, w) in sorted_edges:
        actions.append({
            "id": f"select_{edge_idx}",
            "objectId": f"edge_{edge_idx}",
            "type": "color",
            "start": time,
            "end": time + 0.5,
            "params": {"color": "#a6e3a1", "width": 4},
            "narrative": f"Add edge {u}-{v} (weight {w}) to MST"
        })
        time += 1
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }


def generate_prim_mst_template(idx, difficulty="beginner", language="python"):
    """
    Generates Prim's Minimum Spanning Tree visualization.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"prim_mst_{idx}"
    code_content = CodeGenerator.get_code("prim_mst", language=language, level=difficulty)
    
    # Same graph as Kruskal's
    nodes = [
        {"id": "A", "x": 200, "y": 150},
        {"id": "B", "x": 400, "y": 100},
        {"id": "C", "x": 600, "y": 150},
        {"id": "D", "x": 300, "y": 300},
        {"id": "E", "x": 500, "y": 300}
    ]
    
    edges = [
        ("A", "B", 4), ("A", "D", 2), ("B", "C", 3),
        ("B", "D", 5), ("B", "E", 6), ("C", "E", 1),
        ("D", "E", 7)
    ]
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Prim's MST", "font": "bold 28px Inter", "color": "#89b4fa"}},
    ]
    
    # Draw edges and nodes (same as Kruskal's)
    for i, (u, v, w) in enumerate(edges):
        u_node = next(n for n in nodes if n["id"] == u)
        v_node = next(n for n in nodes if n["id"] == v)
        objects.append({
            "id": f"edge_{i}",
            "type": "line",
            "props": {"x1": u_node["x"], "y1": u_node["y"], "x2": v_node["x"], "y2": v_node["y"], "color": "#45475a", "width": 2}
        })
        mid_x = (u_node["x"] + v_node["x"]) / 2
        mid_y = (u_node["y"] + v_node["y"]) / 2
        objects.append({
            "id": f"weight_{i}",
            "type": "text",
            "props": {"x": mid_x, "y": mid_y, "text": str(w), "font": "14px monospace", "color": "#f9e2af"}
        })
    
    for node in nodes:
        objects.append({
            "id": f"node_{node['id']}",
            "type": "circle",
            "props": {"x": node["x"], "y": node["y"], "radius": 25, "color": "#313244"}
        })
        objects.append({
            "id": f"label_{node['id']}",
            "type": "text",
            "props": {"x": node["x"], "y": node["y"], "text": node["id"], "font": "bold 18px Inter", "color": "#cdd6f4"}
        })
    
    # Prim's algorithm starting from A
    actions = []
    time = 0.5
    
    # Start with A
    actions.append({
        "id": "start_A",
        "objectId": "node_A",
        "type": "color",
        "start": time,
        "end": time + 0.5,
        "params": {"color": "#a6e3a1"},
        "narrative": "Start from node A"
    })
    time += 1
    
    # Add edges in order: A-D(2), B-C(3), C-E(1), A-B(4)
    mst_edges = [(1, "A", "D", 2), (2, "B", "C", 3), (5, "C", "E", 1), (0, "A", "B", 4)]
    for edge_idx, u, v, w in mst_edges:
        actions.append({
            "id": f"add_{edge_idx}",
            "objectId": f"edge_{edge_idx}",
            "type": "color",
            "start": time,
            "end": time + 0.5,
            "params": {"color": "#a6e3a1", "width": 4},
            "narrative": f"Add edge {u}-{v} (weight {w})"
        })
        time += 1
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }


def generate_max_subarray_template(idx, difficulty="beginner", language="python"):
    """
    Generates Maximum Subarray (Kadane's Algorithm) visualization.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"max_subarray_{idx}"
    code_content = CodeGenerator.get_code("max_subarray", language=language, level=difficulty)
    
    data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    n = len(data)
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Maximum Subarray (Kadane's)", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "array_label", "type": "text", "props": {"x": 100, "y": 70, "text": f"Array: {data}", "font": "16px monospace", "color": "#cdd6f4"}},
    ]
    
    # Array elements
    bar_width = 50
    gap = 10
    start_x = 100
    base_y = 300
    
    for i, val in enumerate(data):
        x = start_x + i * (bar_width + gap)
        h = abs(val) * 15
        y = base_y - h if val > 0 else base_y
        color = "#a6e3a1" if val > 0 else "#f38ba8"
        
        objects.append({
            "id": f"bar_{i}",
            "type": "bar",
            "props": {"x": x, "y": y, "width": bar_width, "height": h, "color": color, "text": str(val)}
        })
    
    # Kadane's algorithm
    max_sum = data[0]
    current_sum = data[0]
    start = 0
    end = 0
    temp_start = 0
    
    actions = []
    time = 0.5
    
    for i in range(n):
        if i > 0:
            if current_sum + data[i] > data[i]:
                current_sum += data[i]
            else:
                current_sum = data[i]
                temp_start = i
            
            if current_sum > max_sum:
                max_sum = current_sum
                start = temp_start
                end = i
        
        # Highlight current element
        actions.append({
            "id": f"check_{i}",
            "objectId": f"bar_{i}",
            "type": "color",
            "start": time,
            "end": time + 0.5,
            "params": {"color": "#f9e2af"},
            "narrative": f"Current sum: {current_sum}, Max sum: {max_sum}"
        })
        time += 0.7
    
    # Highlight final max subarray
    for i in range(start, end + 1):
        actions.append({
            "id": f"final_{i}",
            "objectId": f"bar_{i}",
            "type": "color",
            "start": time,
            "end": time + 1,
            "params": {"color": "#89b4fa"},
            "narrative": f"Maximum subarray sum: {max_sum}"
        })
    
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 3,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

def generate_mergesort_template(idx, difficulty="beginner", language="python"):
    """
    Generates Merge Sort visualization.
    Shows the Divide and Conquer approach: splitting the array and merging sorted halves.
    """
    from code_generator import CodeGenerator
    import random
    
    scene_id = f"mergesort_{idx}"
    code_content = CodeGenerator.get_code("mergesort", language=language, level=difficulty)
    
    # Generate random small array
    data = [random.randint(10, 90) for _ in range(8)]
    n = len(data)
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Merge Sort (Divide & Conquer)", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Divide...", "font": "18px monospace", "color": "#cdd6f4"}}
    ]
    
    bar_width = 30
    gap = 5
    
    def add_bars(arr, level, offset_x, start_idx):
        level_y = 120 + level * 80
        total_width = len(arr) * (bar_width + gap) - gap
        x_start = offset_x - total_width / 2
        
        for i, val in enumerate(arr):
            x = x_start + i * (bar_width + gap)
            obj_id = f"bar_l{level}_i{start_idx + i}"
            objects.append({
                "id": obj_id,
                "type": "bar",
                "props": {
                    "x": x, "y": level_y, "width": bar_width, "height": val*0.6 + 10,
                    "color": "#45475a", "text": str(val), "opacity": 0
                }
            })

    # Initial array
    add_bars(data, 0, 400, 0)
    
    actions = []
    time = 0.5
    
    # Show initial array
    for i in range(n):
        actions.append({"id": f"show_base_{i}", "objectId": f"bar_l0_i{i}", "type": "fade", "start": time, "end": time+0.5, "params": {"opacity": 1}})
    time += 1

    def merge_sort_viz(arr, level, offset_x, start_idx):
        nonlocal time
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        
        # Visualize splitting
        depth_offset = 240 / (2**level)
        
        left_offset = offset_x - depth_offset/2
        right_offset = offset_x + depth_offset/2
        
        add_bars(left, level + 1, left_offset, start_idx)
        add_bars(right, level + 1, right_offset, start_idx + mid)
        
        # Narrative for splitting
        actions.append({"id": f"nar_split_l{level}_i{start_idx}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Split at index {start_idx + mid}"}, "narrative": f"Dividing array of size {len(arr)} into two halves."})
        
        for i in range(len(left)):
            actions.append({"id": f"fadein_l_l{level+1}_i{start_idx+i}", "objectId": f"bar_l{level+1}_i{start_idx+i}", "type": "fade", "start": time, "end": time+0.5, "params": {"opacity": 1}})
        for i in range(len(right)):
            actions.append({"id": f"fadein_r_l{level+1}_i{start_idx+mid+i}", "objectId": f"bar_l{level+1}_i{start_idx+mid+i}", "type": "fade", "start": time, "end": time+0.5, "params": {"opacity": 1}})
        time += 1
        
        left_sorted = merge_sort_viz(left, level + 1, left_offset, start_idx)
        right_sorted = merge_sort_viz(right, level + 1, right_offset, start_idx + mid)
        
        # Visualize merging
        actions.append({"id": f"nar_merge_l{level}_i{start_idx}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Merging..."}, "narrative": f"Merging two sorted subarrays into one of size {len(arr)}."})
        
        merged = []
        i_idx = j_idx = 0
        while i_idx < len(left_sorted) and j_idx < len(right_sorted):
            if left_sorted[i_idx] <= right_sorted[j_idx]:
                merged.append(left_sorted[i_idx])
                i_idx += 1
            else:
                merged.append(right_sorted[j_idx])
                j_idx += 1
        merged.extend(left_sorted[i_idx:])
        merged.extend(right_sorted[j_idx:])
        
        # Update colors on children
        for k in range(len(arr)):
            actions.append({"id": f"color_merge_l{level+1}_i{start_idx+k}", "objectId": f"bar_l{level+1}_i{start_idx+k}", "type": "color", "start": time, "end": time+0.3, "params": {"color": "#a6e3a1"}})
        
        time += 0.5
        
        # Update parent bars with sorted values
        for k, val in enumerate(merged):
            actions.append({"id": f"update_parent_l{level}_i{start_idx+k}", "objectId": f"bar_l{level}_i{start_idx+k}", "type": "color", "start": time, "end": time+0.5, "params": {"color": "#a6e3a1", "text": str(val), "height": val*0.6 + 10}})
        
        time += 0.8
        
        return merged

    merge_sort_viz(data, 0, 400, 0)
    
    actions.append({"id": "success", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "Array Sorted!", "color": "#a6e3a1"}, "narrative": "Merge Sort completed successfully using O(n log n) time."})

    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

def generate_bellman_ford_template(idx, difficulty="beginner", language="python"):
    """
    Generates Bellman-Ford shortest path visualization.
    Highlights edge relaxations and the detection of negative cycles.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"bellman_ford_{idx}"
    code_content = CodeGenerator.get_code("bellman_ford", language=language, level=difficulty)
    
    nodes = [
        {"id": "0", "x": 100, "y": 225, "val": "S"},
        {"id": "1", "x": 300, "y": 100, "val": "A"},
        {"id": "2", "x": 300, "y": 350, "val": "B"},
        {"id": "3", "x": 500, "y": 100, "val": "C"},
        {"id": "4", "x": 500, "y": 350, "val": "D"},
        {"id": "5", "x": 700, "y": 225, "val": "E"},
    ]
    edges = [
        ("0", "1", 6), ("0", "2", 7),
        ("1", "3", 5), ("1", "2", 8), ("1", "4", -4),
        ("2", "3", -3), ("2", "4", 9),
        ("3", "1", -2),
        ("4", "3", 7), ("4", "5", 2),
        ("3", "5", -1)
    ]
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Bellman-Ford Algorithm", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Relaxing Edges...", "font": "18px monospace", "color": "#cdd6f4"}}
    ]
    
    for node in nodes:
        objects.append({
            "id": f"node_{node['id']}",
            "type": "circle",
            "props": {"x": node['x'], "y": node['y'], "radius": 20, "color": "#313244", "borderColor": "#cdd6f4", "borderWidth": 2, "text": f"{node['val']}\n∞"}
        })
        
    for u, v, w in edges:
        u_node = next(n for n in nodes if n['id'] == u)
        v_node = next(n for n in nodes if n['id'] == v)
        mx, my = (u_node['x'] + v_node['x']) / 2, (u_node['y'] + v_node['y']) / 2
        objects.append({
            "id": f"edge_{u}_{v}",
            "type": "line",
            "props": {"x1": u_node['x'], "y1": u_node['y'], "x2": v_node['x'], "y2": v_node['y'], "color": "#45475a", "width": 2}
        })
        objects.append({
            "id": f"weight_{u}_{v}",
            "type": "text",
            "props": {"x": mx, "y": my-10, "text": str(w), "font": "14px Inter", "color": "#bac2de"}
        })

    actions = []
    time = 0.5
    dist = {node['id']: float('inf') for node in nodes}; dist['0'] = 0
    actions.append({"id": "init", "objectId": "node_0", "type": "color", "start": time, "end": time+0.5, "params": {"text": "S\n0", "color": "#a6e3a1"}, "narrative": "Initializing distances. Source node S set to 0, others to infinity."})
    time += 1

    for it in range(len(nodes) - 1):
        changed = False
        time += 0.5
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w; changed = True
                v_node_val = next(n for n in nodes if n['id'] == v)['val']
                actions.append({"id": f"relax_{it}_{u}_{v}", "objectId": f"edge_{u}_{v}", "type": "color", "start": time, "end": time+0.3, "params": {"color": "#f9e2af", "width": 4}})
                actions.append({"id": f"update_{it}_{v}", "objectId": f"node_{v}", "type": "color", "start": time+0.3, "end": time+0.6, "params": {"text": f"{v_node_val}\n{dist[v]}", "color": "#fab387"}, "narrative": f"Relaxing edge ({next(n for n in nodes if n['id']==u)['val']},{v_node_val}): updated to {dist[v]}."})
                time += 0.7
                actions.append({"id": f"reset_{it}_{u}_{v}", "objectId": f"edge_{u}_{v}", "type": "color", "start": time, "end": time+0.1, "params": {"color": "#45475a", "width": 2}})
        if not changed: break

    actions.append({"id": "complete", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "Shortest Paths Calculated", "color": "#a6e3a1"}})
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

def generate_floyd_warshall_template(idx, difficulty="beginner", language="python"):
    """
    Generates Floyd-Warshall All-Pairs Shortest Path visualization.
    Shows the distance matrix updating as we consider each vertex as an intermediate node.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"floyd_warshall_{idx}"
    code_content = CodeGenerator.get_code("floyd_warshall", language=language, level=difficulty)
    
    matrix = [[0, 3, float('inf'), 7], [8, 0, 2, float('inf')], [5, float('inf'), 0, 1], [2, float('inf'), float('inf'), 0]]
    V = 4
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Floyd-Warshall (All-Pairs Shortest Path)", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Initial Distance Matrix", "font": "18px monospace", "color": "#cdd6f4"}}
    ]
    
    cell_size, start_x, start_y = 60, 280, 150
    for i in range(V):
        objects.append({"id": f"row_lab_{i}", "type": "text", "props": {"x": start_x - 40, "y": start_y + i*cell_size + 30, "text": f"V{i}", "font": "bold 16px Inter", "color": "#f5c2e7"}})
        objects.append({"id": f"col_lab_{i}", "type": "text", "props": {"x": start_x + i*cell_size + 30, "y": start_y - 30, "text": f"V{i}", "font": "bold 16px Inter", "color": "#f5c2e7"}})
        for j in range(V):
            val = matrix[i][j]; display_val = "∞" if val == float('inf') else str(val)
            objects.append({"id": f"cell_bg_{i}_{j}", "type": "rect", "props": {"x": start_x + j*cell_size, "y": start_y + i*cell_size, "width": cell_size, "height": cell_size, "color": "#313244", "borderColor": "#45475a", "borderWidth": 1}})
            objects.append({"id": f"cell_txt_{i}_{j}", "type": "text", "props": {"x": start_x + j*cell_size + 30, "y": start_y + i*cell_size + 30, "text": display_val, "font": "16px Inter", "color": "#cdd6f4"}})

    actions = []; time = 1.0; dist = [row[:] for row in matrix]
    for k in range(V):
        actions.append({"id": f"iter_k_{k}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Considering intermediate vertex V{k}"}, "narrative": f"Using V{k} to find shorter paths."})
        for i in range(V):
            actions.append({"id": f"high_row_{k}_{i}", "objectId": f"cell_bg_{k}_{i}", "type": "color", "start": time, "end": time+0.5, "params": {"color": "#45475a"}})
            actions.append({"id": f"high_col_{k}_{i}", "objectId": f"cell_bg_{i}_{k}", "type": "color", "start": time, "end": time+0.5, "params": {"color": "#45475a"}})
        time += 0.8
        for i in range(V):
            for j in range(V):
                if i == k or j == k: continue
                actions.append({"id": f"check_{k}_{i}_{j}", "objectId": f"cell_bg_{i}_{j}", "type": "color", "start": time, "end": time+0.2, "params": {"color": "#89b4fa"}})
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    actions.append({"id": f"update_{k}_{i}_{j}", "objectId": f"cell_txt_{i}_{j}", "type": "fade", "start": time+0.2, "end": time+0.4, "params": {"text": str(dist[i][j]), "color": "#a6e3a1"}, "narrative": f"V{i}->V{j} through V{k} is shorter: {dist[i][j]}"})
                    time += 0.6
                else: time += 0.2
                actions.append({"id": f"reset_{k}_{i}_{j}", "objectId": f"cell_bg_{i}_{j}", "type": "color", "start": time, "end": time+0.1, "params": {"color": "#313244"}})
        for i in range(V):
            actions.append({"id": f"unhigh_row_{k}_{i}", "objectId": f"cell_bg_{k}_{i}", "type": "color", "start": time, "end": time+0.1, "params": {"color": "#313244"}})
            actions.append({"id": f"unhigh_col_{k}_{i}", "objectId": f"cell_bg_{i}_{k}", "type": "color", "start": time, "end": time+0.1, "params": {"color": "#313244"}})
        time += 0.5

    actions.append({"id": "complete", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "All-Pairs Shortest Paths Found", "color": "#a6e3a1"}})
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

def generate_dfs_bfs_template(idx, algo_type="bfs", difficulty="beginner", language="python"):
    """
    Generates DFS or BFS Graph Traversal visualization.
    Shows the difference between Stack (DFS) and Queue (BFS) order.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"{algo_type}_{idx}"
    code_content = CodeGenerator.get_code(algo_type, language=language, level=difficulty)
    
    # Simple graph layout
    nodes = [
        {"id": "0", "x": 400, "y": 80, "val": "A"},
        {"id": "1", "x": 200, "y": 180, "val": "B"},
        {"id": "2", "x": 600, "y": 180, "val": "C"},
        {"id": "3", "x": 100, "y": 300, "val": "D"},
        {"id": "4", "x": 300, "y": 300, "val": "E"},
        {"id": "5", "x": 500, "y": 300, "val": "F"},
        {"id": "6", "x": 700, "y": 300, "val": "G"},
    ]
    edges = [
        ("0", "1"), ("0", "2"),
        ("1", "3"), ("1", "4"),
        ("2", "5"), ("2", "6")
    ]
    
    adj = {
        "0": ["1", "2"],
        "1": ["3", "4"],
        "2": ["5", "6"],
        "3": [], "4": [], "5": [], "6": []
    }
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": f"{algo_type.upper()} Graph Traversal", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Starting...", "font": "18px monospace", "color": "#cdd6f4"}},
    ]
    
    # Add nodes
    for node in nodes:
        objects.append({
            "id": f"node_{node['id']}",
            "type": "circle",
            "props": {"x": node['x'], "y": node['y'], "radius": 25, "color": "#313244", "borderColor": "#cdd6f4", "borderWidth": 2, "text": node['val']}
        })
        
    # Add edges
    for u, v in edges:
        u_node = next(n for n in nodes if n['id'] == u)
        v_node = next(n for n in nodes if n['id'] == v)
        objects.append({
            "id": f"edge_{u}_{v}",
            "type": "line",
            "props": {"x1": u_node['x'], "y1": u_node['y'], "x2": v_node['x'], "y2": v_node['y'], "color": "#45475a", "width": 2}
        })

    actions = []
    time = 0.5
    visited = []
    
    if algo_type == "bfs":
        queue = ["0"]
        actions.append({"id": "start_bfs", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": "Enqueue Root node A"}, "narrative": "Starting BFS from the root node."})
        time += 0.8
        
        while queue:
            u = queue.pop(0)
            if u not in visited:
                visited.append(u)
                u_val = next(n for n in nodes if n['id'] == u)['val']
                actions.append({"id": f"visit_{u}", "objectId": f"node_{u}", "type": "color", "start": time, "end": time+0.5, "params": {"color": "#fab387"}, "narrative": f"Visiting node {u_val}."})
                actions.append({"id": f"stat_{u}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Visiting {u_val}"}})
                time += 0.8
                for v in adj[u]:
                    if v not in visited and v not in queue:
                        queue.append(v)
                        v_val = next(n for n in nodes if n['id'] == v)['val']
                        actions.append({"id": f"edge_{u}_{v}_on", "objectId": f"edge_{u}_{v}", "type": "color", "start": time, "end": time+0.5, "params": {"color": "#89b4fa", "width": 4}})
                        actions.append({"id": f"stat_enc_{v}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Enqueue {v_val}"}, "narrative": f"Discovered child {v_val}, adding it to the queue."})
                        time += 0.5
    else:
        stack = ["0"]
        actions.append({"id": "start_dfs", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": "Push Root node A"}, "narrative": "Starting DFS from the root node."})
        time += 0.8
        
        while stack:
            u = stack.pop()
            if u not in visited:
                visited.append(u)
                u_val = next(n for n in nodes if n['id'] == u)['val']
                actions.append({"id": f"visit_{u}", "objectId": f"node_{u}", "type": "color", "start": time, "end": time+0.5, "params": {"color": "#a6e3a1"}, "narrative": f"Visiting node {u_val}."})
                actions.append({"id": f"stat_{u}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Visiting {u_val}"}})
                time += 0.8
                for v in reversed(adj[u]):
                    if v not in visited:
                        stack.append(v)
                        v_val = next(n for n in nodes if n['id'] == v)['val']
                        actions.append({"id": f"edge_{u}_{v}_on", "objectId": f"edge_{u}_{v}", "type": "color", "start": time, "end": time+0.5, "params": {"color": "#89b4fa", "width": 4}})
                        actions.append({"id": f"stat_push_{v}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Push {v_val}"}, "narrative": f"Exploring deeper to child {v_val}, adding it to the stack."})
                        time += 0.5

    actions.append({"id": "complete", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "Traversal Complete!", "color": "#a6e3a1"}, "narrative": f"{algo_type.upper()} completed."})

    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }

def generate_radix_sort_template(idx, difficulty="beginner", language="python"):
    """
    Generates Radix Sort visualization.
    Shows the sorting process digit by digit from least significant to most significant.
    """
    from code_generator import CodeGenerator
    scene_id = f"radix_sort_{idx}"
    code_content = CodeGenerator.get_code("radix_sort", language=language, level=difficulty)
    vals = [170, 45, 75, 90, 802, 24, 2, 66]
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Radix Sort (LSD) Visualization", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Starting...", "font": "18px monospace", "color": "#cdd6f4"}}
    ]
    bucket_w, start_x = 70, 40
    for i in range(10):
        objects.append({"id": f"bucket_{i}", "type": "rect", "props": {"x": start_x + i * 75, "y": 350, "width": bucket_w, "height": 80, "color": "#313244", "borderColor": "#45475a", "borderWidth": 2, "text": f"D{i}"}})
    for i, val in enumerate(vals):
        objects.append({"id": f"num_{i}", "type": "circle", "props": {"x": 100 + i * 80, "y": 150, "radius": 25, "color": "#181825", "borderColor": "#cdd6f4", "borderWidth": 2, "text": str(val)}})
    actions = []; time = 1.0; max_val = max(vals); exp = 1
    while max_val // exp > 0:
        actions.append({"id": f"digit_{exp}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"Sorting by digit at 10^{len(str(exp))-1} place"}, "narrative": f"Processing digit position {exp}."}); time += 0.8
        bucket_counts = [0] * 10
        for i, val in enumerate(vals):
            digit = (val // exp) % 10; bx = start_x + digit * 75 + 35; by = 350 + 20 + bucket_counts[digit] * 20; bucket_counts[digit] += 1
            actions.append({"id": f"move_to_b_{exp}_{i}", "objectId": f"num_{i}", "type": "move", "start": time, "end": time+0.5, "params": {"x": bx, "y": by}}); time += 0.2
        time += 0.6; actions.append({"id": f"col_{exp}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": "Collecting from buckets..."}}); time += 0.8
        for i in range(len(vals)):
             actions.append({"id": f"move_back_{exp}_{i}", "objectId": f"num_{i}", "type": "move", "start": time, "end": time+0.5, "params": {"x": 100 + i * 80, "y": 150}}); time += 0.1
        exp *= 10; time += 0.5
    actions.append({"id": "complete", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "Radix Sort Complete", "color": "#a6e3a1"}})
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": time + 1, "code": code_content, "objects": objects, "actions": actions}

def generate_astar_template(idx, difficulty="beginner", language="python"):
    """
    Generates A* Search Pathfinding visualization.
    Shows the exploration of nodes based on f(n) = g(n) + h(n).
    """
    from code_generator import CodeGenerator
    scene_id = f"astar_{idx}"
    code_content = CodeGenerator.get_code("astar", language=language, level=difficulty)
    grid = [[2, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 1, 0], [1, 1, 0, 1, 0], [0, 0, 0, 0, 3]]
    rows, cols, cell_size, start_x, start_y = 5, 5, 50, 275, 120
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "A* Pathfinding Visualization", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Exploring Paths...", "font": "18px monospace", "color": "#cdd6f4"}}
    ]
    for r in range(rows):
        for c in range(cols):
            x, y = start_x + c * cell_size, start_y + r * cell_size; color = "#313244"
            if grid[r][c] == 1: color = "#45475a"
            elif grid[r][c] == 2: color = "#a6e3a1"
            elif grid[r][c] == 3: color = "#f38ba8"
            objects.append({"id": f"cell_{r}_{c}", "type": "rect", "props": {"x": x, "y": y, "width": cell_size-2, "height": cell_size-2, "color": color, "borderColor": "#cdd6f4", "borderWidth": 1}})
    actions = []; time = 1.0; path = [(0,0), (1,0), (2,0), (2,1), (2,2), (3,2), (4,2), (4,3), (4,4)]; explored = [(0,1), (0,2), (1,3), (1,4), (2,4), (3,0)]
    for r, c in explored:
        actions.append({"id": f"exp_{r}_{c}", "objectId": f"cell_{r}_{c}", "type": "color", "start": time, "end": time+0.4, "params": {"color": "#89b4fa"}, "narrative": f"Exploring node at ({r}, {c}) with lowest f-score."}); time += 0.3
    time += 0.5; actions.append({"id": "found", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": "Target Reached! Highlighting Path"}, "narrative": "Target node found. Backtracking to show the shortest path."}); time += 0.8
    for r, c in path:
        actions.append({"id": f"path_{r}_{c}", "objectId": f"cell_{r}_{c}", "type": "color", "start": time, "end": time+0.3, "params": {"color": "#f9e2af"}}); time += 0.2
    actions.append({"id": "complete", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "A* Search Complete", "color": "#a6e3a1"}})
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": time + 1, "code": code_content, "objects": objects, "actions": actions}

def generate_linked_list_template(idx, difficulty="beginner", language="python"):
    """
    Generates Linked List visualization.
    Shows node creation, pointer linking, and traversal.
    """
    from code_generator import CodeGenerator
    scene_id = f"linked_list_{idx}"
    code_content = CodeGenerator.get_code("linked_list", language=language, level=difficulty)
    vals = [10, 20, 30, 40]
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Singly Linked List Visualization", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Creating Nodes...", "font": "18px monospace", "color": "#cdd6f4"}}
    ]
    node_w, node_h, gap, start_x, start_y = 80, 40, 60, 100, 200
    actions = []; time = 0.5
    for i, val in enumerate(vals):
        x = start_x + i * (node_w + gap)
        objects.append({"id": f"node_{i}", "type": "rect", "props": {"x": x, "y": start_y, "width": node_w, "height": node_h, "color": "#313244", "borderColor": "#cdd6f4", "borderWidth": 2, "text": str(val), "opacity": 0}})
        objects.append({"id": f"ptr_{i}", "type": "rect", "props": {"x": x + node_w - 20, "y": start_y, "width": 20, "height": node_h, "color": "#45475a", "borderColor": "#cdd6f4", "borderWidth": 1, "opacity": 0}})
        actions.append({"id": f"fade_node_{i}", "objectId": f"node_{i}", "type": "fade", "start": time, "end": time+0.5, "params": {"opacity": 1}, "narrative": f"Creating node with value {val}."})
        actions.append({"id": f"fade_ptr_{i}", "objectId": f"ptr_{i}", "type": "fade", "start": time, "end": time+0.5, "params": {"opacity": 1}}); time += 0.8
        if i > 0:
            prev_x = start_x + (i-1) * (node_w + gap) + node_w - 10
            objects.append({"id": f"edge_{i-1}_{i}", "type": "line", "props": {"x1": prev_x, "y1": start_y + node_h/2, "x2": x, "y2": start_y + node_h/2, "color": "#f5c2e7", "width": 2, "opacity": 0}})
            actions.append({"id": f"fade_edge_{i}", "objectId": f"edge_{i-1}_{i}", "type": "fade", "start": time, "end": time+0.5, "params": {"opacity": 1}, "narrative": f"Linking node {vals[i-1]} to node {val}."}); time += 0.6
    actions.append({"id": "complete", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "Linked List Created", "color": "#a6e3a1"}})
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": time + 2, "code": code_content, "objects": objects, "actions": actions}

def generate_stack_template(idx, difficulty="beginner", language="python"):
    """
    Generates Stack visualization.
    Shows LIFO (Last-In, First-Out) behavior with Push and Pop operations.
    """
    from code_generator import CodeGenerator
    scene_id = f"stack_{idx}"
    code_content = CodeGenerator.get_code("stack", language=language, level=difficulty)
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Stack Visualization (LIFO)", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Ready", "font": "18px monospace", "color": "#cdd6f4"}},
        {"id": "container", "type": "rect", "props": {"x": 350, "y": 120, "width": 100, "height": 300, "color": "#313244", "borderColor": "#cdd6f4", "borderWidth": 4}}
    ]
    actions = []; time = 1.0; stack_data = [10, 20, 30]
    for i, val in enumerate(stack_data):
        obj_id = f"item_{i}"; y = 390 - i*40
        objects.append({"id": obj_id, "type": "rect", "props": {"x": 360, "y": -50, "width": 80, "height": 30, "color": "#fab387", "text": str(val)}})
        actions.append({"id": f"push_{i}", "objectId": obj_id, "type": "move", "start": time, "end": time+0.5, "params": {"y": y}, "narrative": f"Pushing {val} onto the stack."})
        actions.append({"id": f"stat_push_{i}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"PUSH {val}"}}); time += 0.8
    i = len(stack_data) - 1
    actions.append({"id": f"pop_{i}", "objectId": f"item_{i}", "type": "move", "start": time, "end": time+0.5, "params": {"y": -50}, "narrative": f"Popping {stack_data[i]} from the stack (Top element)."}); actions.append({"id": f"stat_pop_{i}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"POP {stack_data[i]}"}}); time += 1.0
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": time + 1, "code": code_content, "objects": objects, "actions": actions}

def generate_queue_template(idx, difficulty="beginner", language="python"):
    """
    Generates Queue visualization.
    Shows FIFO (First-In, First-Out) behavior with Enqueue and Dequeue operations.
    """
    from code_generator import CodeGenerator
    scene_id = f"queue_{idx}"
    code_content = CodeGenerator.get_code("queue", language=language, level=difficulty)
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Queue Visualization (FIFO)", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Ready", "font": "18px monospace", "color": "#cdd6f4"}},
        {"id": "container", "type": "rect", "props": {"x": 200, "y": 200, "width": 400, "height": 60, "color": "#313244", "borderColor": "#cdd6f4", "borderWidth": 4}}
    ]
    actions = []; time = 1.0; queue_data = [10, 20, 30, 40]
    for i, val in enumerate(queue_data):
        obj_id = f"item_{i}"; x = 515 - i*85
        objects.append({"id": obj_id, "type": "rect", "props": {"x": 850, "y": 210, "width": 80, "height": 40, "color": "#a6e3a1", "text": str(val)}})
        actions.append({"id": f"enq_{i}", "objectId": obj_id, "type": "move", "start": time, "end": time+0.5, "params": {"x": x}, "narrative": f"Enqueuing {val} into the queue."}); actions.append({"id": f"stat_enq_{i}", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"ENQUEUE {val}"}}); time += 0.8
    actions.append({"id": "deq_0", "objectId": "item_0", "type": "move", "start": time, "end": time+0.5, "params": {"x": -100}, "narrative": f"Dequeuing {queue_data[0]} from the front of the queue."}); actions.append({"id": "stat_deq", "objectId": "status", "type": "fade", "start": time, "end": time+0.5, "params": {"text": f"DEQUEUE {queue_data[0]}"}}); time += 0.6
    for i in range(1, len(queue_data)): actions.append({"id": f"shift_{i}", "objectId": f"item_{i}", "type": "move", "start": time, "end": time+0.3, "params": {"x": 515 - (i-1)*85}})
    time += 0.5
    return {"sceneId": scene_id, "width": 800, "height": 450, "duration": time + 1, "code": code_content, "objects": objects, "actions": actions}

def generate_bst_template(idx, difficulty="beginner", language="python"):
    """
    Generates Binary Search Tree (BST) visualization.
    Shows the step-by-step insertion of values and how the tree maintains its properties.
    """
    from code_generator import CodeGenerator
    
    scene_id = f"bst_{idx}"
    code_content = CodeGenerator.get_code("bst", language=language, level=difficulty)
    vals = [50, 30, 70, 20, 40, 60, 80]
    
    objects = [
        {"id": "bg", "type": "rect", "props": {"x": 0, "y": 0, "width": 800, "height": 450, "color": "#1e1e2e"}},
        {"id": "title", "type": "text", "props": {"x": 400, "y": 30, "text": "Binary Search Tree (BST) Insertion", "font": "bold 24px Inter", "color": "#89b4fa"}},
        {"id": "status", "type": "text", "props": {"x": 400, "y": 70, "text": "Starting Insertion...", "font": "18px monospace", "color": "#cdd6f4"}}
    ]
    
    actions = []; time = 0.5; root = None
    for val in vals:
        if root is None:
            root = {"val": val, "x": 400, "y": 120, "level": 1, "id": f"node_{val}", "left": None, "right": None}
            objects.append({"id": root['id'], "type": "circle", "props": {"x": root['x'], "y": root['y'], "radius": 22, "color": "#313244", "borderColor": "#cdd6f4", "borderWidth": 2, "text": str(val), "opacity": 0}})
            actions.append({"id": f"fade_{val}", "objectId": root['id'], "type": "fade", "start": time, "end": time+0.5, "params": {"opacity": 1}, "narrative": f"Root node {val} created."})
            time += 1
            continue
        curr = root; parent = None
        while curr:
            parent = curr
            actions.append({"id": f"high_{val}_{curr['val']}", "objectId": curr['id'], "type": "color", "start": time, "end": time+0.4, "params": {"color": "#89b4fa"}})
            if val < curr['val']:
                actions.append({"id": f"msg_{val}_{curr['val']}", "objectId": "status", "type": "fade", "start": time, "end": time+0.4, "params": {"text": f"{val} < {curr['val']}, Go LEFT"}})
                time += 0.5
                actions.append({"id": f"reset_{val}_{curr['val']}", "objectId": curr['id'], "type": "color", "start": time, "end": time+0.1, "params": {"color": "#313244"}})
                if curr['left'] is None:
                    dx = 200 / (2**curr['level'])
                    new_node = {"val": val, "x": curr['x'] - dx, "y": curr['y'] + 80, "level": curr['level'] + 1, "id": f"node_{val}", "left": None, "right": None}
                    curr['left'] = new_node; break
                else: curr = curr['left']
            else:
                actions.append({"id": f"msg_{val}_{curr['val']}", "objectId": "status", "type": "fade", "start": time, "end": time+0.4, "params": {"text": f"{val} > {curr['val']}, Go RIGHT"}})
                time += 0.5
                actions.append({"id": f"reset_{val}_{curr['val']}", "objectId": curr['id'], "type": "color", "start": time, "end": time+0.1, "params": {"color": "#313244"}})
                if curr['right'] is None:
                    dx = 200 / (2**curr['level'])
                    new_node = {"val": val, "x": curr['x'] + dx, "y": curr['y'] + 80, "level": curr['level'] + 1, "id": f"node_{val}", "left": None, "right": None}
                    curr['right'] = new_node; break
                else: curr = curr['right']
        objects.append({"id": new_node['id'], "type": "circle", "props": {"x": new_node['x'], "y": new_node['y'], "radius": 22, "color": "#313244", "borderColor": "#cdd6f4", "borderWidth": 2, "text": str(val), "opacity": 0}})
        objects.append({"id": f"edge_{parent['id']}_{new_node['id']}", "type": "line", "props": {"x1": parent['x'], "y1": parent['y'], "x2": new_node['x'], "y2": new_node['y'], "color": "#45475a", "width": 2, "opacity": 0}})
        actions.append({"id": f"fade_edge_{val}", "objectId": f"edge_{parent['id']}_{new_node['id']}", "type": "fade", "start": time, "end": time+0.4, "params": {"opacity": 1}})
        actions.append({"id": f"fade_node_{val}", "objectId": new_node['id'], "type": "fade", "start": time, "end": time+0.4, "params": {"opacity": 1}, "narrative": f"Inserted {val} at its correct position."})
        time += 0.6

    actions.append({"id": "complete", "objectId": "status", "type": "fade", "start": time, "end": time+1, "params": {"text": "BST Insertion Complete", "color": "#a6e3a1"}})
    return {
        "sceneId": scene_id,
        "width": 800,
        "height": 450,
        "duration": time + 2,
        "code": code_content,
        "objects": objects,
        "actions": actions
    }
