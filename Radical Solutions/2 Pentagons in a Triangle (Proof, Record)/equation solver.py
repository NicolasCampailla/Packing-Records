import sympy as sp

# Define the variables
x1, y1, x2, y2 = sp.symbols('x1 y1 x2 y2', real=True)

# Define h based on previous derivations
h = sp.sqrt(5) * sp.tan(sp.pi / 30)

# Define the first system of equations (for intersection 1: y1, x1)
eq1_1 = sp.Eq(y1, sp.tan(11 * sp.pi / 30) * (x1 - 1))
eq1_2 = sp.Eq(y1 + h, sp.tan(-3 * sp.pi / 10) * (x1 - (-1 + 2 * sp.cos(4 * sp.pi / 5))))

# Define the second system of equations (for intersection 2: y2, x2)
eq2_1 = sp.Eq(y2, sp.tan(11 * sp.pi / 30) * (x2 - 1))
eq2_2 = sp.Eq(y2 - sp.sin(2 * sp.pi / 5), sp.tan(sp.pi / 30) * (x2 - sp.cos(2 * sp.pi / 5)))

# Solve the systems
sol1 = sp.solve((eq1_1, eq1_2), (x1, y1))
sol2 = sp.solve((eq2_1, eq2_2), (x2, y2))

# Extract the coordinates from the solution dictionaries
x1_val = sol1[x1]
y1_val = sol1[y1]
x2_val = sol2[x2]
y2_val = sol2[y2]

# Calculate the norm (distance between the two intersection points)
# ||(x1, y1) - (x2, y2)||
norm = sp.sqrt((x1_val - x2_val)**2 + (y1_val - y2_val)**2)

# Define the side length of the central pentagon
# Center at (0,0) and vertex at (1,0) implies a circumradius R = 1.
# Side length = 2 * R * sin(pi / 5)
pentagon_side = 2 * sp.sin(sp.pi / 5)

# Calculate the final scaled result S
S = norm / pentagon_side

# Simplify the exact expression (this groups the trigonometric terms)
S_exact = sp.simplify(S)

# Evaluate the numerical approximation
S_num = S.evalf()

# Output the results
print("Exact Form (S):") #                  \frac{\sqrt{- 120 \sqrt{6} \sqrt{\sqrt{5} + 5} - 99 \sqrt{5} + 705 + 48 \sqrt{30} \sqrt{\sqrt{5} + 5}}}{3 \sqrt{5 - \sqrt{5}}}
print(sp.latex(S_exact))
print("\nNumerical Approximation (S):") #   4.01077587433033...
print(S_num)