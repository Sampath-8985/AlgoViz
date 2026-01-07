import template_generator
print("Testing Matrix Mult...")
try:
    template_generator.generate_matrix_template(2, 2, "mult")
    print("Mult OK")
except Exception as e:
    print(f"Mult Failed: {e}")

print("Testing Matrix Exp...")
try:
    template_generator.generate_matrix_template(2, 2, "exp")
    print("Exp OK")
except Exception as e:
    print(f"Exp Failed: {e}")

print("Testing Matrix Add...")
try:
    template_generator.generate_matrix_template(2, 2, "add")
    print("Add OK")
except Exception as e:
    print(f"Add Failed: {e}")
