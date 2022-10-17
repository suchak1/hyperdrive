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


def mesh_plot(vertices, faces):
    # colored
    gm = go.Mesh3d(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
                   i=faces[:, 0], j=faces[:, 1], k=faces[:, 2])
    return gm


def wireframe_plot(vertices, faces):
    # black outline
    Xe = np.concatenate((vertices[faces, 0], np.full((faces.shape[0], 1), None)),
                        axis=1).ravel()
    Ye = np.concatenate((vertices[faces, 1], np.full((faces.shape[0], 1), None)),
                        axis=1).ravel()
    Ze = np.concatenate((vertices[faces, 2], np.full((faces.shape[0], 1), None)),
                        axis=1).ravel()

    gm = go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', name='',
                      line=dict(color='rgb(40,40,40)', width=1))
    return gm


def calc_shortest_dist(points):
    point1 = points[0]
    dists = [math.dist(point1, point) for point in points[1:]]
    return min(dists)


def get_plane_pts(points):
    points = [tuple(point) for point in points]
    shortest_dist = calc_shortest_dist(points)
    plane_sets = set()
    for i, pt1 in enumerate(points):
        for j, pt2 in enumerate(points):
            for k, pt3 in enumerate(points):
                # further optimizations by making sure k >= j and j >= i
                if i == j or j == k or i == k or k < j or j < i:
                    continue
                A_2_B = math.dist(pt1, pt2)
                B_2_C = math.dist(pt2, pt3)
                C_2_A = math.dist(pt3, pt1)

                is_planar_set = (
                    np.isclose(A_2_B, B_2_C)
                    and np.isclose(B_2_C, C_2_A)
                    and np.isclose(A_2_B, C_2_A)
                    and np.isclose(A_2_B, shortest_dist)
                )
                if is_planar_set:
                    plane_set = (pt1, pt2, pt3)
                    perms = permutations(plane_set)
                    if any([perm in plane_sets for perm in perms]):
                        continue
                    plane_sets.add(plane_set)

    return list(plane_sets)


def same_plane_side(pt1, pt2, coeffs):
    pt1_side = calc.eval_plane(pt1, coeffs)
    pt2_side = calc.eval_plane(pt2, coeffs)
    plane_side = (
        pt1_side == abs(pt1_side)) == (
        pt2_side == abs(pt2_side)
    )
    return plane_side


def check_pt_in_shape(point, vertices):
    centroid = calc.find_centroid(vertices)
    plane_pts = get_plane_pts(vertices)
    planes = [calc.find_plane(*pts) for pts in plane_pts]
    for plane in planes:
        if not same_plane_side(centroid, point, plane):
            return False
    return True


def generate_icosphere(radius, center, refinement):
    vertices, faces = icosphere.icosphere(refinement)
    length = norm(vertices, axis=1).reshape((-1, 1))
    vertices = vertices / length * radius + center
    return vertices, faces

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
unit_normal = normal / math.dist(center, normal)
# print(math.dist(center, unit_normal))
q1 = p1
q2 = center + np.cross(unit_normal, p1 - center)
angles = np.linspace(0, 2 * math.pi, 360)
xs = [center[0] + math.cos(theta) * (p1[0] - center[0]) +
      math.sin(theta) * (q2[0] - center[0]) for theta in angles]
ys = [center[1] + math.cos(theta) * (p1[1] - center[1]) +
      math.sin(theta) * (q2[1] - center[1]) for theta in angles]
zs = [center[2] + math.cos(theta) * (p1[2] - center[2]) +
      math.sin(theta) * (q2[2] - center[2]) for theta in angles]

# method 2: https://math.stackexchange.com/a/73242
radius = math.dist(center, p1)

q1 = q1 / math.dist(center, q1)
q2 = center + np.cross(q1, unit_normal)

xs = [center[0] + radius *
      math.cos(theta) * q1[0] + radius * math.sin(theta) * q2[0] for theta in angles]
ys = [center[1] + radius *
      math.cos(theta) * q1[1] + radius * math.sin(theta) * q2[1] for theta in angles]
zs = [center[2] + radius *
      math.cos(theta) * q1[2] + radius * math.sin(theta) * q2[2] for theta in angles]


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
