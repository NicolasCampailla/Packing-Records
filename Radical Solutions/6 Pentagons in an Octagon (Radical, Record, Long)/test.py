import sympy as sp

def main():
    # 1. Define symbols
    h = sp.Symbol('h', real=True, positive=True)
    x, y = sp.symbols('x y', real=True)
    
    # 2. Define the exact constants based on the angles in your equations
    pi5 = sp.pi / 5
    cos_pi5 = sp.cos(pi5)
    tan_pi5 = sp.tan(pi5)
    
    # Evaluate 8pi/5 terms
    sin_8pi5 = sp.sin(8 * pi5)
    cos_8pi5 = sp.cos(8 * pi5)
    
    # 3. Formulate the geometric boundaries
    # Purple line (right side of the V, from Eq 4): y - sin(8pi/5) = x - cos(8pi/5) - cos(pi/5)
    # Solve for x in terms of y:
    x_purple = y - sin_8pi5 + cos_8pi5 + cos_pi5
    
    # Vertical boundary line (Black line, from Eq 10)
    # x = cos(9pi/5) + 2 + cos(pi/5) - h*tan(pi/5)
    # Since cos(9pi/5) is equivalent to cos(pi/5), this simplifies to:
    x_vert = 2 * cos_pi5 + 2 - h * tan_pi5
    
    # Bottom horizontal line (Green line, from Eq 13 with j = -1)
    # y = sin(pi) + h - (cos(9pi/5) + 2 + cos(pi/5) - h*tan(pi/5))
    # Since sin(pi) = 0, y is exactly h - x_vert
    y_bottom = h - x_vert
    
    # 4. Calculate Segment Norms
    # A. Horizontal Segment
    # Spans along y_bottom between the red line (-x) and purple line (+x).
    # Because it is symmetric around the y-axis, the length is 2 * (x-coordinate on purple line).
    x_right_horiz = x_purple.subs(y, y_bottom)
    norm_horizontal = 2 * x_right_horiz
    
    # B. Slanted Segment
    # Lies along the purple line (slope = 1), bounded by y_bottom and x_vert.
    # The length of a segment with slope 1 is sp.sqrt(2) * (delta x).
    norm_slanted = sp.sqrt(2) * (x_vert - x_right_horiz)
    
    # 5. Solve for h
    equation = sp.Eq(norm_horizontal, norm_slanted)
    h_solution = sp.solve(equation, h)[0]
    
    # 6. Find the Exact Radical for the Norm
    # Substitute the exact h back into the norm equation
    exact_norm = norm_horizontal.subs(h, h_solution)
    
    # 7. Output & Verification
    print("=== Exact Solution for h ===")
    h_latex = sp.latex(sp.simplify(h_solution))
    print(f"${h_latex}$")

    print("\n=== Exact Radical for the Norm of the Segments ===")
    simplified_norm = sp.simplify(exact_norm)
    normalized_norm = sp.simplify(sp.sqrtdenest(sp.radsimp(simplified_norm / (2 * sp.sin(sp.pi / 5)))))
    norm_latex = sp.latex(normalized_norm)
    print(f"${norm_latex}$")
    print(f"\nNumerical value of the norm: {normalized_norm.evalf()}")

    num_simp = (4 + sp.sqrt(5))*sp.sqrt(5 - sp.sqrt(5)) + (5 - sp.sqrt(5))/sp.sqrt(2)
    den_simp = (sp.sqrt(2) + 2) * (1 + sp.sqrt(10 - 4*sp.sqrt(5)))

    expr_simp = num_simp / den_simp
    expr_orig = normalized_norm
    
    # 3. Compare them using .equals() (Checks mathematical equivalence)
    is_equivalent = expr_orig.equals(expr_simp)
    print(f"Are the expressions mathematically equivalent? {is_equivalent}")

    # 4. Verify with high-precision numerical evaluation (50 decimal places)
    val_orig = expr_orig.evalf(50)
    val_simp = expr_simp.evalf(50)
    difference = val_orig - val_simp

    print("\n--- Numerical Verification ---")
    print(f"Original:   {val_orig}")
    print(f"Simplified: {val_simp}")
    print(f"Difference: {difference}")

    sp.pprint(sp.latex(expr_simp))
    print(expr_simp.evalf(50))

if __name__ == "__main__":
    main()