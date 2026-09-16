import sympy as sp

def calculate_normalized_square_side():
    # 1. Exact value for 'b' from the current graph state
    b = (4*sp.sqrt(5) + 2 + sp.sqrt(10 - 2*sp.sqrt(5))) / \
        (2*sp.sqrt(8 + 2*sp.sqrt(10 - 2*sp.sqrt(5))))

    # 2. Extract the bounding box limits based on graph expressions
    # Left bound (Expression 34): x = cos(2pi/5 + pi/5 + pi/4)
    x_left = sp.cos(2*sp.pi/5 + sp.pi/5 + sp.pi/4)
    
    # Right bound (Expression 40): x = cos(6pi/5 + 2pi/5 + pi/4) + b
    x_right = sp.cos(6*sp.pi/5 + 2*sp.pi/5 + sp.pi/4) + b

    # (Symmetry check: Top and bottom bounds give the identical distance)

    # 3. Calculate absolute square side length
    square_side = x_right - x_left

    # 4. Normalize by the regular pentagon's side length
    # Circumradius is 1, so the side length is 2*sin(pi/5)
    pentagon_side = 2 * sp.sin(sp.pi / 5)
    
    normalized_side = square_side / pentagon_side

    # 5. Output and simplify the results
    
    # sp.simplify combined with sp.radsimp condenses the nested radicals
    exact_normalized = sp.radsimp(sp.simplify(normalized_side))
    
    return exact_normalized, exact_normalized.evalf()

if __name__ == "__main__":
    exact_val, dec_val = calculate_normalized_square_side()
    simplified_expr = ((3 - sp.sqrt(5))*sp.sqrt(5 - sp.sqrt(5)) + 7*sp.sqrt(10) + sp.sqrt(2)) / 8

    # Verify they are mathematically identical
    difference = sp.simplify(exact_val - simplified_expr)

    print(f"Original Expression == Simplified Expression?")
    print(f"Mathematical proof (Difference simplifies to 0): {difference == 0}")
    
    print("\n--- Exact Normalized Square Side Length ---")
    print(sp.latex(simplified_expr))
    print(f"\nDecimal Approximation: {dec_val}")