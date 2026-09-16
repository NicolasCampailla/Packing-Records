import sympy as sp

def main():
    pi = sp.pi
    
    # Pentagon side length (inscribed in a unit circle)
    L = 2 * sp.sin(pi / 5)
    
    # Exact value of 'a' 
    a = (5 + 3*sp.sqrt(5))/4 - sp.sqrt((25 + 11*sp.sqrt(5))/8)
    
    # Exact value of 'd' from the tangential touch condition
    numerator_d = sp.cos(pi/5) * (
        (sp.Rational(3,2) - a)*sp.sin(pi/5) + 
        sp.cos(pi/5) + 
        sp.cos(pi/5)**2 - 
        sp.Rational(3,2)*sp.sin(2*pi/5)
    )
    denominator_d = 1 + sp.sin(2*pi/5)
    d = numerator_d / denominator_d
    
    # X-coordinates of the bounding box based on Tokens 9 and 11
    x9 = sp.cos(4*pi/5)
    x11 = sp.cos(4*pi/5 + pi) + 2 - d * sp.tan(pi/5)
    
    # Bounding box side length (width of the square)
    side_length = x11 - x9
    
    # Normalize by the pentagon side length
    normalized_side = side_length / L
    
    # Simplify the radical expression
    exact_normalized = sp.simplify(normalized_side)
    simplified_expr = ((8 + 5*sp.sqrt(5)) / 2) * sp.sqrt(5 + 2*sp.sqrt(5)) - (55 + 23*sp.sqrt(5)) / 4

    # Verify they are mathematically identical
    difference = sp.simplify(exact_normalized - simplified_expr)

    print(f"Original Expression == Simplified Expression?")
    print(f"Mathematical proof (Difference simplifies to 0): {difference == 0}")
    
    print("\n--- Exact Normalized Square Side Length ---")
    print(sp.latex(simplified_expr))
    print(f"\nDecimal Approximation: {simplified_expr.evalf():.8f}")


if __name__ == "__main__":
    main()