from sympy.abc import x, y, r
from sympy import solve

def radius_of_curvature(p0, p1, p2):
    """
    Calculates the radius of curvurature of a circle where p0, p1, and p2 are on the circumference of the circle. 
    """
    solutions = solve([
            (p0[0] - x)**2 + (p0[1] - y)**2 - r**2,
            (p1[0] - x)**2 + (p1[1] - y)**2 - r**2,
            (p2[0] - x)**2 + (p2[1] - y)**2 - r**2
        ], (r, x, y), dict=True)
    for solution in solutions:
        if solution[r] > 0:
            return solution[r]
    
