import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 1. SymPy Calculation for Exact LaTeX String
# Define constants symbolically
a = (1 + sp.sqrt(2)) / 2
y1_sym = (3*sp.sqrt(2) - 6*sp.sqrt(3) - 5*sp.sqrt(6)) / 24

# Solve for L: L = 2*sqrt(3) * (a - y1)
L_sym = sp.expand(2 * sp.sqrt(3) * (a - y1_sym))

# Convert the SymPy expression to a LaTeX string
# We wrap it in \frac to ensure it looks like a proper fraction
latex_expr = sp.latex(L_sym)
full_title_latex = rf"Outer Polygon Side Length: ${latex_expr} \approx {float(L_sym):.15f}$"

# 2. Numerical Setup for Plotting
L_val = float(L_sym)
h = L_val / (2 * np.sqrt(3))

# Numerical coordinates
c1 = np.array([float((6 + 3*sp.sqrt(2) + 4*np.sqrt(3) + 5*np.sqrt(6)) / 24),
               float(y1_sym)])

def rotate(pt, angle_deg):
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([pt[0]*c - pt[1]*s, pt[0]*s + pt[1]*c])

c2 = rotate(c1, 120)
c3 = rotate(c1, 240)

offset = c1
c1_img, c2_img, c3_img = c1 - offset, c2 - offset, c3 - offset

# 3. Visualization
R = np.sqrt(4 + 2*np.sqrt(2)) / 2

def get_octagon_verts(center, angle_deg):
    angles = np.linspace(np.pi/8, 2*np.pi + np.pi/8, 9)
    verts = np.array([[R * np.cos(a), R * np.sin(a)] for a in angles])
    rad = np.radians(angle_deg)
    rot_mat = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
    return np.dot(verts, rot_mat.T) + center

fig, ax = plt.subplots(figsize=(8, 8))

# Draw Polygons
for center, angle in [(c1_img, 0), (c2_img, 30), (c3_img, 15)]:
    v = get_octagon_verts(center, angle)
    ax.fill(v[:,0], v[:,1], facecolor='#cccccc', edgecolor='black', lw=1, zorder=2)

# Draw Triangle Boundary
T_verts = np.array([[0, 2*h], [-L_val/2, -h], [L_val/2, -h], [0, 2*h]]) - offset
ax.plot(T_verts[:,0], T_verts[:,1], color='black', lw=1, zorder=1)

# Formatting
ax.set_aspect('equal')
ax.set_title(full_title_latex, fontsize=12, pad=20)
ax.axis('off')
print(full_title_latex)
plt.tight_layout()
plt.show()
