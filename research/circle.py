import sys
import math
import numpy as np
import icosphere
import numpy as np
from numpy.linalg import norm
import plotly.graph_objects as go
from itertools import permutations
sys.path.append('hyperdrive')
from Calculus import Calculator  # noqa

calc = Calculator()

# points of circle
# { x: 0.1, y: 0.1, z: 2.15 },
# { x: 1.25, y: 1.25, z: 1.25 }, // distance from (0, 0, 0) ~ 2.16
# { x: 1.53, y: 1.53, z: 0.1 },
# { x: 1.25, y: 1.25, z: -1.25 },
# { x: 0.1, y: 0.1, z: -2.15 },


x = [0.1, 1.25, 1.53, 1.25, 0.1]
y = [0.1, 1.25, 1.53, 1.25, 0.1]
z = [2.15, 1.25, 0.1, -1.25, -2.15]

# parametric equations for a circle in 3D
# https://math.stackexchange.com/a/2375120
# https://math.stackexchange.com/a/73242


# # can't use this bc this infinite number of planes exist on this line
# plane = eq_plane([0, 0, 0], [0, 0, 2], [0, 0, -2])
# print(plane)

# method 1: https://math.stackexchange.com/a/2375120
center = np.array([0, 0, 0])
p1 = np.array([1.25, 1.25, 1.25])
p2 = np.array([1.25, 1.25, -1.25])
plane = calc.find_plane(center, p1, p2)
print(plane)
normal = np.array(plane[0:3])
# print(norm(()))

x0, y0, z0 = center
x1, y1, z1 = p1
x2, y2, z2 = p2

ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]

u_cross_v = [uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx]

point = np.array(center)
normal = np.array(np.cross(u, v))

d = -p2.dot(normal)

print(normal)
print(d)
# unit_normal = normal / math.dist(center, normal)
# # print(math.dist(center, unit_normal))
# q1 = p1
# q2 = center + np.cross(unit_normal, p1 - center)
# angles = np.linspace(0, 2 * math.pi, 360)
# xs = [center[0] + math.cos(theta) * (p1[0] - center[0]) +
#       math.sin(theta) * (q2[0] - center[0]) for theta in angles]
# ys = [center[1] + math.cos(theta) * (p1[1] - center[1]) +
#       math.sin(theta) * (q2[1] - center[1]) for theta in angles]
# zs = [center[2] + math.cos(theta) * (p1[2] - center[2]) +
#       math.sin(theta) * (q2[2] - center[2]) for theta in angles]

# # method 2: https://math.stackexchange.com/a/73242
# radius = math.dist(center, p1)

# q1 = q1 / math.dist(center, q1)
# q2 = center + np.cross(q1, unit_normal)

# xs = [center[0] + radius *
#       math.cos(theta) * q1[0] + radius * math.sin(theta) * q2[0] for theta in angles]
# ys = [center[1] + radius *
#       math.cos(theta) * q1[1] + radius * math.sin(theta) * q2[1] for theta in angles]
# zs = [center[2] + radius *
#       math.cos(theta) * q1[2] + radius * math.sin(theta) * q2[2] for theta in angles]


# fig = go.Figure(data=[
#     go.Scatter3d(
#         x=x,
#         y=y,
#         z=z,
#         mode='markers',
#         marker_color='cyan',
#         marker={'line': {'color': 'black', 'width': 1},
#                 },
#         showlegend=True,
#         text='market surge',
#         name='BUY'
#     ),
#     go.Scatter3d(
#         x=[0],
#         y=[0],
#         z=[0],
#         mode='markers',
#         marker_color='magenta',
#         marker={'line': {'color': 'black', 'width': 1},
#                 },
#         showlegend=True,
#         text='center',
#         name='center'
#     ),
#     go.Scatter3d(
#         x=xs,
#         y=ys,
#         z=zs,
#         mode='markers',
#         marker_color='lime',
#         marker={'line': {'color': 'black', 'width': 1},
#                 },
#         showlegend=True,
#         text='center',
#         name='center',
#         opacity=0.25
#     )
# ]
# )

# fig.show()
