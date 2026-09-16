import sympy as sp

# Define symbolic angles
pi = sp.pi
p5 = pi / 5
p6 = pi / 6

# 1. Exact value for parameter h
# Matching the tangency condition from the Desmos geometry construction
h_sym = (2 + 2 * sp.cos(p5)) * sp.tan(p6) / (1 + sp.tan(p5) * sp.tan(p6))

# 2. Upper line equation:
# y - sin(2*pi/5) = tan(pi/6) * (x + cos(2*pi/5) + cos(pi/5))
# Let line equation be y = m * (x - x0) + y0
x0 = -(sp.cos(2*p5) + sp.cos(p5))
y0 = sp.sin(2*p5)
m = sp.tan(p6)

# Point A: Intersection of upper sloped line with the x-axis (y = 0)
# 0 = m * (x_A - x0) + y0  =>  x_A = x0 - y0 / m
x_A = x0 - y0 / m

# Point B: Point on upper sloped line at the vertical line x = x_bound
x_bound = 2 * sp.cos(p5) + 2 - h_sym * sp.tan(p5)
y_B = m * (x_bound - x0) + y0

# The segment length along a line inclined at angle theta = pi/6:
# L = (x_bound - x_A) / cos(pi/6)
segment_length = (x_bound - x_A) / sp.cos(p6)

# 3. Normalized side length: divide by pentagon side length 2*sin(pi/5)
unit_side = 2 * sp.sin(p5)
normalized_side = sp.simplify(segment_length / unit_side)

print(f"Exact h: {sp.simplify(h_sym)}")
print(f"Numerical h: {float(h_sym.evalf()):.6f}")
print(f"\nExact Bounding Segment Length: {sp.simplify(segment_length)}")
print(f"Exact Normalized Side Length: {sp.latex(normalized_side)}")
print(f"Numerical Normalized Side Length: {float(normalized_side.evalf()):.9f}")