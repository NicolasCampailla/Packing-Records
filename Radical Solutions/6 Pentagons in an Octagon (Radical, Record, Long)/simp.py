from sympy import sqrt, cos, pi, simplify, sqrtdenest, nsimplify, trigsimp

# 1. Define the numerator and denominator
num = (sqrt(35 - 15*sqrt(5))/2 + 5*sqrt(7 - 3*sqrt(5))/2 + 
       sqrt(25 - 5*sqrt(5)) + 4*sqrt(5 - sqrt(5)))
den = (sqrt(2) + 2*sqrt(5 - 2*sqrt(5)) + 2 + 2*sqrt(2)*sqrt(5 - 2*sqrt(5)))
expr = num / den

# --- Method A: Algebraic Denesting ---
# sqrtdenest attempts to un-nest double radicals (e.g. sqrt(a + b*sqrt(c)))
# radsimp rationalizes the denominator.
alg_simplified = simplify(sqrtdenest(expr))
print("Algebraic Simplification:", alg_simplified)

# --- Method B: Trigonometric Substitution ---
# Nested radicals of 5 correspond to trigonometric values of a pentagon.
# We know that cos(pi/5) = (1 + sqrt(5)) / 4, so sqrt(5) = 4*cos(pi/5) - 1.
# Substituting this allows SymPy's trigsimp to collapse the terms.
expr_trig = expr.subs(sqrt(5), 4*cos(pi/5) - 1)
trig_simplified = trigsimp(expr_trig)
print("Trig Simplification:", trig_simplified)

# --- Method C: Numeric-Algebraic Recognition (Usually the shortest) ---
# nsimplify evaluates the expression numerically to high precision and 
# finds the simplest exact algebraic equivalent.
shortest_expr = nsimplify(expr)
print("Absolute Shortest (nsimplify):", shortest_expr)