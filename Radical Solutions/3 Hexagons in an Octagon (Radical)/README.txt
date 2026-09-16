Hello Erich! This is the fixed version of whatever I sent you. As usual here is the desmos geometry link https://www.desmos.com/geometry/mlokji5mfs, where you may find some of the steps that lead to the solution: 
In a word, I found the equation y=-x+q, with q such that the line passes through two outer edges of the bottom hexagon. 
I then found the equation x=k, with k such that the line passes through the two rightmost edges of the right hexagon, then plotted the bisector of the system (the red dashed line) and set up the system of equations:
y = x+b
y = a
along with all of the conditions such that the norms of the segments created would be equal (you can find more info in the file "Solve ab.py"). After finding the solutions of a and b, we find the norm, and reflect all of the lines about the point in the centre of the system (the intersection of the red and blue dotted lines), and save the image.
