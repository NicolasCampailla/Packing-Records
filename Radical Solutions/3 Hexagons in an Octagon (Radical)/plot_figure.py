import numpy as np
import matplotlib.pyplot as plt

pi = np.pi
k = np.arange(7)

# Calculate nested root point 85
x85 = -(np.sqrt(2)/2)*(np.cos(pi/3) + np.sin(pi/3)) + 0.5
y85 = -(np.sqrt(2)/2)*(np.sin(2*pi/3) - np.cos(2*pi/3)) - np.sin(2*pi/6)

# The generated hexagons
x86 = np.cos(2*pi*k/6)
y86 = np.sin(2*pi*k/6)
x87 = np.cos(2*pi*k/6 + pi/12) + x85
y87 = np.sin(2*pi*k/6 + pi/12) + y85
x_P1 = 0.5 + np.sqrt(3)/2 + np.sin(2*pi*k/6)
y_P1 = -0.5 - np.sqrt(3)/2 + np.cos(2*pi*k/6)

# Calculate x192 boundary
x192 = (0.5 + np.sqrt(3)) - (np.sqrt(3)/2 - (-1.5*np.sqrt(3) - np.sqrt(2) + 1))

# --- Calculate the Octagon Vertices ---
lines = []
lines.append((y87[4] - y87[3], -(x87[4] - x87[3]), x87[3]*(y87[4] - y87[3]) - y87[3]*(x87[4] - x87[3])))
lines.append((y86[1] - y86[2], -(x86[1] - x86[2]), x86[2]*(y86[1] - y86[2]) - y86[2]*(x86[1] - x86[2])))
lines.append((0, 1, -1.5*np.sqrt(3) - np.sqrt(2) + 1))
lines.append((1, -1, np.sqrt(6) + 1.5 + np.sqrt(3)/2 - np.sqrt(2)/2))
lines.append((1, 0, 0.5 + np.sqrt(3)))
lines.append((1, 0, x192))
lines.append((1, -1, -np.sqrt(6) - 0.5 + np.sqrt(3)/2 + np.sqrt(2)/2))
lines.append((1, 1, np.sqrt(6) - np.sqrt(3)/2 - 1.5*np.sqrt(2) + 2.5))

cx = (x192 + 0.5 + np.sqrt(3)) / 2
cy = (np.sqrt(3)/2 + (-1.5*np.sqrt(3) - np.sqrt(2) + 1)) / 2

std_lines = []
for A, B, C in lines:
    if A*cx + B*cy > C:
        std_lines.append((-A, -B, -C))
    else:
        std_lines.append((A, B, C))

vertices = []
for i in range(len(std_lines)):
    for j in range(i+1, len(std_lines)):
        A1, B1, C1 = std_lines[i]
        A2, B2, C2 = std_lines[j]
        det = A1*B2 - A2*B1
        if abs(det) > 1e-9:
            ix = (C1*B2 - C2*B1) / det
            iy = (A1*C2 - A2*C1) / det
            if all(A*ix + B*iy <= C + 1e-5 for A, B, C in std_lines):
                if not any(np.hypot(ix-vx, iy-vy) < 1e-5 for vx, vy in vertices):
                    vertices.append((ix, iy))

vertices.sort(key=lambda p: np.arctan2(p[1]-cy, p[0]-cx))
vertices.append(vertices[0])
oct_x, oct_y = zip(*vertices)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')

# Plot filled hexagon objects with transparency
ax.fill(x86, y86, color='#CCCCCC', edgecolor='black', label='86', linewidth=1)
ax.fill(x87, y87, color='#CCCCCC', edgecolor='black', label='87', linewidth=1)
ax.fill(x_P1, y_P1, color='#CCCCCC', edgecolor='black', label='P1', linewidth=1)

# Plot the bounded regular octagon (as outline)
plt.plot(oct_x, oct_y, color='#000000', label='Octagon', linewidth=1)

# Formatting
plt.xlim(-2, 2.5)
plt.ylim(-3.5, 1)
plt.gca().set_aspect('equal', adjustable='box')
plt.title("s = -2*sqrt(3) - 2*sqrt(2) + 3 + 2*sqrt(6) ≈ 1.60645075")

# Removed plt.grid(...)
plt.show()