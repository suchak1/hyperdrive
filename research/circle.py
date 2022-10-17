import sys
import math
import numpy as np
from numpy.linalg import norm
import plotly.graph_objects as go
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

circle = calc.get_3d_circle(center, p1, p2)

xs, ys, zs = circle


fig = go.Figure(data=[
    go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker_color='cyan',
        marker={'line': {'color': 'black', 'width': 1},
                },
        showlegend=True,
        text='market surge',
        name='BUY'
    ),
    go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker_color='magenta',
        marker={'line': {'color': 'black', 'width': 1},
                },
        showlegend=True,
        text='center',
        name='center'
    ),
    go.Scatter3d(
        x=xs,
        y=ys,
        z=zs,
        mode='markers',
        marker_color='lime',
        marker={'line': {'color': 'black', 'width': 1},
                },
        showlegend=True,
        text='center',
        name='center',
        opacity=0.25
    )
]
)

fig.show()
