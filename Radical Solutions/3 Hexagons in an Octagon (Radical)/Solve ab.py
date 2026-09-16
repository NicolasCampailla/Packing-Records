import sympy as sp

def solve_hexagon_lines():
    # Define primary unknown variables
    a, b = sp.symbols('a b', real=True)
    x, y = sp.symbols('x y', real=True)

    # Basic mathematical constants and functions
    pi = sp.pi
    sin = sp.sin
    cos = sp.cos
    sqrt = sp.sqrt

    # 1. Center of the left hexagon (token 85)
    cx = -sqrt(2)/2 * (cos(pi/3) + sin(pi/3)) + sp.Rational(1, 2)
    cy = -sqrt(2)/2 * (sin(2*pi/3) - cos(2*pi/3)) - sin(2*pi/6)

    # 2. Line 82 (Blue line passing through A and B)
    # Passes through k=3 (index 4) and k=4 (index 5) of token 87
    k3_angle = 2*pi*3/6 + pi/12
    k4_angle = 2*pi*4/6 + pi/12

    v3_x = cx + cos(k3_angle)
    v3_y = cy + sin(k3_angle)
    v4_x = cx + cos(k4_angle)
    v4_y = cy + sin(k4_angle)

    # Equation of Line 82 using cross multiplication to avoid division by zero
    line82_eq = sp.Eq((y - v3_y) * (v4_x - v3_x), (x - v3_x) * (v4_y - v3_y))

    # 3. Point A (Intersection of Line 82 and Purple Line)
    # Purple line eq: y - cy = x - cx
    purple_line_eq = sp.Eq(y - cy, x - cx)
    pt_A = sp.solve([line82_eq, purple_line_eq], (x, y))
    Ax, Ay = pt_A[x], pt_A[y]

    # 4. Point B (Intersection of Line 82 and Red Line y = a)
    pt_B = sp.solve([line82_eq, sp.Eq(y, a)], (x, y))
    Bx, By = pt_B[x], pt_B[y]

    # 5. Point C (Intersection of Red Line y = a and Green Line y = x + b)
    pt_C = sp.solve([sp.Eq(y, a), sp.Eq(y, x + b)], (x, y))
    Cx, Cy = pt_C[x], pt_C[y]

    # 6. Point D (Intersection of Green Line y = x + b and Vertical Blue Line 83)
    # Center of right hexagon (token 88)
    cx88 = sp.Rational(1, 2) + sqrt(3)/2
    
    # Vertical line passes through k=1 (index 2) of token 88
    # Note: the JSON defines token 88 with sin() for X and cos() for Y
    x_vert = cx88 + sin(2*pi*1/6)
    line83_eq = sp.Eq(x, x_vert)

    pt_D = sp.solve([line83_eq, sp.Eq(y, x + b)], (x, y))
    Dx, Dy = pt_D[x], pt_D[y]

    # 7. Formulate distance equations
    # Using 1D projections based on the known slopes to keep the system linear
    dist_AB = sqrt(2) * (Ay - a)
    dist_BC = Cx - Bx
    dist_CD = sqrt(2) * (Dx - Cx)

    # Required equalities: 2*||A-B|| == ||B-C|| and ||B-C|| == ||C-D||
    eq1 = sp.Eq(2 * dist_AB, dist_BC)
    eq2 = sp.Eq(dist_BC, dist_CD)

    # 8. Solve the linear system for a and b
    solution = sp.solve([eq1, eq2], (a, b))
    (a_sol,b_sol) = solution.values()
    s = sp.simplify(dist_CD.subs({a: a_sol,b : b_sol}))
    return s

if __name__ == "__main__":
    sol = solve_hexagon_lines()
    
    print("Exact Analytical Solutions:")
    print((sol))
        
    print("\nNumerical Approximations:")
    print(sol.evalf(9))