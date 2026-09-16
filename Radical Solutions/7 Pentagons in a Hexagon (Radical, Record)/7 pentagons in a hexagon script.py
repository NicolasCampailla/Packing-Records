import sympy as sp

def calculate_normalized_green_segment():
    # 1. Define the geometric constants based on the Desmos state
    a = -sp.pi / 3
    
    # Exact value of 'b' for the single-point contact derived previously (Expression 16)
    b = (3*sp.sqrt(30 + 6*sp.sqrt(5)) + 7*sp.sqrt(5) - 7) / \
        (2*(sp.sqrt(15) + sp.sqrt(3) + sp.sqrt(10 - 2*sp.sqrt(5))))

    # 2. Extract intersection points with the green line
    # The green line (Expression 12) is at y = cos(8pi/5 + pi/5 + pi) = cos(14pi/5)
    y_green = sp.cos(14 * sp.pi / 5)

    # --- Intersection with Purple Line 2 (Expression 17) ---
    # The line anchor is y = cos(pi/5 + pi) = cos(6pi/5).
    # Since cos(14pi/5) is identically equal to cos(6pi/5), the green line 
    # intersects Purple Line 2 exactly at its anchor's x-coordinate.
    x2 = sp.sin(sp.pi / 5 + sp.pi)

    # --- Intersection with Purple Line 1 (Expression 13) ---
    # Purple Line 1 anchor coordinates:
    y_anchor_1 = sp.cos(14*sp.pi/5 + a) - sp.cos(6*sp.pi/5 + a) + sp.cos(14*sp.pi/5)
    x_anchor_1 = sp.sin(14*sp.pi/5 + a) + b
    
    # Solve Expression 13 for x1 at y = y_green: 
    # y_green - y_anchor_1 = tan(pi/3) * (x1 - x_anchor_1)
    x1 = x_anchor_1 + (y_green - y_anchor_1) / sp.tan(sp.pi / 3)

    # 3. Calculate segment length and normalize
    # Circumradius is 1, so the side length of the regular pentagon is 2*sin(pi/5)
    pentagon_side = 2 * sp.sin(sp.pi / 5)
    
    green_segment_length = x1 - x2
    normalized_length = green_segment_length / pentagon_side

    # 4. Radically simplify the result
    # We use trigsimp and radsimp to heavily condense the nested roots
    exact_radical = sp.simplify(normalized_length)
    exact_radical = sp.radsimp(exact_radical)
    
    return exact_radical, exact_radical.evalf()

if __name__ == "__main__":
    exact_val, dec_val = calculate_normalized_green_segment()
    simplified_val = (2*sp.sqrt(5) - 1 + sp.sqrt(15 - 6*sp.sqrt(5))) / 2
    print("\n--- Exact Normalized Length ---")
    print(sp.latex(exact_val))
    print(f"\nDecimal Approximation: {dec_val}")
    difference = exact_val - simplified_val

    # Verify that the difference mathematically simplifies to 0
    is_zero = sp.simplify(difference) == 0

    print("Original Expression == Simplified Expression?")
    print(f"Mathematical proof (Difference simplifies to 0): {is_zero}")
    print(sp.latex(simplified_val))