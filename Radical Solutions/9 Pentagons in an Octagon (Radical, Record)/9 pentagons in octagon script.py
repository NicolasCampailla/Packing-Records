import sympy as sp

def calculate_normalized_length():
    # Define exact symbolic constants
    pi = sp.pi
    
    # 1. Base geometric definitions
    def V1(k):
        """Vertices of the red pentagon."""
        return sp.Matrix([sp.sin(2*pi*k/5 - pi/5), sp.cos(2*pi*k/5 - pi/5)])
    
    def V2_base(k):
        """Unshifted rotated vertices of the green pentagon."""
        return sp.Matrix([sp.sin(2*pi*k/5 - pi/5 - pi/4), sp.cos(2*pi*k/5 - pi/5 - pi/4)])
        
    # Constant offset applied to the green pentagon
    offset = sp.Matrix([
        -sp.sin(8*pi/5 - pi/4), 
        -sp.cos(8*pi/5 - pi/4) + sp.cos(3*pi/5) - sp.sin(3*pi/5)
    ])
    
    # Translation parameter
    h = sp.Symbol('h', real=True)
    
    def V2(k, h_val):
        """Vertices of the green pentagon as a function of h."""
        return V2_base(k) + offset + h_val * sp.Matrix([-1, 1])

    # 2. Find h where the green pentagon touches the red pentagon
    # The correct physical touch (avoiding overlap) happens between the rightmost
    # red vertex (k=2) and the top-left green edge (k=0 to k=1).
    red_touch_point = V1(2)
    green_edge_start = V2(0, h)
    
    # The slope between green k=0 and k=1 is exactly 1 based on the rotation angles.
    # Therefore, the line equation is: y - y0 = 1 * (x - x0)
    # We substitute the red vertex into this line to solve for h.
    collision_eq = sp.Eq(red_touch_point[1] - green_edge_start[1], 
                         red_touch_point[0] - green_edge_start[0])
    
    # Solve the linear equation for h
    h_sol = sp.solve(collision_eq, h)[0]
    
    # 3. Calculate the yellow segment length
    # Connecting bottom-left of red (k=4) to the lowest vertex of green (k=4)
    p_start = V1(4)
    p_end = V2(4, h_sol)
    
    # Distance calculation
    dx = p_end[0] - p_start[0]
    dy = p_end[1] - p_start[1]
    
    # Simplify the squared distance to prevent hanging on nested trig roots
    dist_sq = sp.simplify(dx**2 + dy**2)
    segment_length = sp.sqrt(dist_sq)
    
    # 4. Normalize by side length
    # Side length of a regular pentagon with circumradius R=1
    side_length = 2 * sp.sin(pi/5)
    normalized_length = segment_length / side_length
    
    # Fully simplify the final exact expressions
    final_h = sp.simplify(h_sol)
    final_val = sp.simplify(normalized_length)
    
    # Print the exact values formatted as LaTeX radicals
    print("--- Exact Collision Parameter (h) ---")
    print(sp.latex(final_h))
    
    print("\n--- Exact Normalized Yellow Segment Length (LaTeX) ---")
    print(sp.latex(final_val))
    
    print("\n--- Numerical Approximations ---")
    print(f"h ≈ {final_h.evalf(50)}")
    print(f"Normalized Length ≈ {final_val.evalf(50)}")

if __name__ == "__main__":
    calculate_normalized_length()