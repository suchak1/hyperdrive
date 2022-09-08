import math
import pickle
import numpy as np
import icosphere
import numpy as np
from numpy.linalg import norm
import plotly.graph_objects as go
from itertools import permutations
from sklearn.decomposition import PCA
from plotly.subplots import make_subplots

with open('research/X.pkl', 'rb') as file:
    X = pickle.load(file)

with open('research/y.pkl', 'rb') as file:
    y = pickle.load(file)

new_write = True

if new_write:
    def predict(data):
        filename = 'research/models/latest/model.pkl'

        with open(filename, 'rb') as file:
            model = pickle.load(file)
            return model.predict(data)

    num_points = 100
    reducer = PCA(n_components=3)
    X_transformed = reducer.fit_transform(X)
    component_x, component_y, component_z = X_transformed.T
    all_coords = np.concatenate((component_x, component_y, component_z))
    # not going far enough in the -x and -y directions
    super_min = min(all_coords)
    super_min -= abs(super_min) * 0.25
    super_max = max(all_coords)
    super_max += abs(super_max) * 0.25
    lin_x = np.linspace(super_min, super_max, num_points)
    lin_y = np.linspace(super_min, super_max, num_points)
    lin_z = np.linspace(super_min, super_max, num_points)
    xx, yy, zz = np.meshgrid(lin_x, lin_y, lin_z)
    xs = xx.flatten()
    ys = yy.flatten()
    zs = zz.flatten()

    reduced = np.array([xs, ys, zs]).T
    unreduced = reducer.inverse_transform(reduced)
    preds = predict(unreduced)

    with open('research/xs_2.pkl', 'wb') as file:
        pickle.dump(xs, file)

    with open('research/ys_2.pkl', 'wb') as file:
        pickle.dump(ys, file)

    with open('research/zs_2.pkl', 'wb') as file:
        pickle.dump(zs, file)

    with open('research/preds_2.pkl', 'wb') as file:
        pickle.dump(preds, file)

    with open('research/component_x_2.pkl', 'wb') as file:
        pickle.dump(component_x, file)

    with open('research/component_y_2.pkl', 'wb') as file:
        pickle.dump(component_y, file)

    with open('research/component_z_2.pkl', 'wb') as file:
        pickle.dump(component_z, file)

# x, y, z = pts.T
with open('research/xs_2.pkl', 'rb') as file:
    xs = pickle.load(file)

with open('research/ys_2.pkl', 'rb') as file:
    ys = pickle.load(file)

with open('research/zs_2.pkl', 'rb') as file:
    zs = pickle.load(file)

with open('research/preds_2.pkl', 'rb') as file:
    preds = pickle.load(file)

with open('research/component_x_2.pkl', 'rb') as file:
    component_x = pickle.load(file)

with open('research/component_y_2.pkl', 'rb') as file:
    component_y = pickle.load(file)

with open('research/component_z_2.pkl', 'rb') as file:
    component_z = pickle.load(file)


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


# def get_plane_pts(points):
#     shortest_dist = calc_shortest_dist(points)
#     plane_sets = {}
#     for i, point1 in enumerate(points):
#         rest = [i + j + 1 for j, point in enumerate(
#             points[i + 1:]) if math.dist(point1, point) == shortest_dist]

#     pass

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


def eq_plane(pt1, pt2, pt3):
    # this one seems to work
    x1, y1, z1 = pt1
    x2, y2, z2 = pt2
    x3, y3, z3 = pt3

    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)
    # print(a * pt1[0] + b * pt1[1] + c * pt1[2] + d)
    # print(a * pt2[0] + b * pt2[1] + c * pt2[2] + d)
    # print(a * pt3[0] + b * pt3[1] + c * pt3[2] + d)
    # ax + by + cz + d = 0
    return a, b, c, d


def avg(x):
    return sum(x) / len(x)


def calc_centroid(points, method='mean'):
    # points = np.array(points)
    x, y, z = points.T
    if method != 'mean':
        x = [min(x), max(x)]
        y = [min(y), max(y)]
        z = [min(z), max(z)]
    return avg(x), avg(y), avg(z)


def calc_plane(pt, coeffs):
    x, y, z = pt
    a, b, c, d = coeffs
    return a * x + b * y + c * z + d


def same_plane_side(pt1, pt2, coeffs):
    pt1_side = calc_plane(pt1, coeffs)
    pt2_side = calc_plane(pt2, coeffs)
    plane_side = (
        pt1_side == abs(pt1_side)) == (
        pt2_side == abs(pt2_side)
    )
    return plane_side


def check_pt_in_shape(point, vertices):
    centroid = calc_centroid(vertices)
    plane_pts = get_plane_pts(vertices)
    planes = [eq_plane(*pts) for pts in plane_pts]
    for plane in planes:
        if not same_plane_side(centroid, point, plane):
            return False
    return True


def generate_icosphere(radius, center, refinement):
    vertices, faces = icosphere.icosphere(refinement)
    length = norm(vertices, axis=1).reshape((-1, 1))
    vertices = vertices / length * radius + center
    return vertices, faces

    # def eq_plane2(pt1, pt2, pt3):
    #     # this one seems to be wrong
    #     # These two vectors are in the plane
    #     pt1, pt2, pt3 = np.array(pt1), np.array(pt2), np.array(pt3)
    #     v1 = pt3 - pt1
    #     v2 = pt2 - pt1

    #     # the cross product is a vector normal to the plane
    #     cp = np.cross(v1, v2)
    #     a, b, c = cp

    #     # This evaluates a * x3 + b * y3 + c * z3 which equals d
    #     d = np.dot(cp, pt3)
    #     # print(a * pt1[0] + b * pt1[1] + c * pt1[2] + d)
    #     # print(a * pt2[0] + b * pt2[1] + c * pt2[2] + d)
    #     # print(a * pt3[0] + b * pt3[1] + c * pt3[2] + d)
    #     return a, b, c, d

    # DONE
    # 1. get each set of 3 points - each set corresponds to a plane
    # 2. get plane equation for each plane
    # MAY BE UNNECESSARY - planes returns list of A, B, C coefficients of plane equation Ax + By + Cz?
    # 3. get center point using vertices
    # (0, 0, 0),
    # (0, 1, 0),
    # (1, 0, 0),
    # (1, 1, 0)

    # (0, 0, 1),
    # (0, 1, 1),
    # (1, 0, 1),
    # (1, 1, 1)

    # 4. check if two points are on same side of plane (signs?)
    # 5. iterate thru planes for each plane ^ checking if point is in convex solid
    # 6. use generate_icosphere fx src code to modify center and size of icosphere
    # 7. increase linspace sample area for prediction

    # TO DO
    # 8. plot cube without boundaries
    # 9. plot icosphere touching edges of cube
    # 10. finally, plot predictions icosphere
    # 11. try cube predictions
    # 12. try octahedron preds
    # 13. commit to git and add to model creation automation
    # 14. start working on js


# need this to create icosphere center

X_transformed = np.array((component_x, component_y, component_z)).T
centroid = calc_centroid(X_transformed)

nu = 1
vertices, faces = generate_icosphere(
    radius=(max(xs) - min(xs)) / 2,
    center=centroid,
    refinement=nu
)

fig = go.Figure(data=[
    go.Scatter3d(
        x=[datum for idx, datum in enumerate(component_x) if y[idx]],
        y=[datum for idx, datum in enumerate(component_y) if y[idx]],
        z=[datum for idx, datum in enumerate(component_z) if y[idx]],
        mode='markers',
        marker_color='cyan',
        marker={'line': {'color': 'black', 'width': 1},
                },
        showlegend=True,
        text='market surge',
        name='BUY'
    ),
    go.Scatter3d(
        x=[datum for idx, datum in enumerate(component_x) if not y[idx]],
        y=[datum for idx, datum in enumerate(component_y) if not y[idx]],
        z=[datum for idx, datum in enumerate(component_z) if not y[idx]],
        mode='markers',
        marker_color='magenta',
        marker={'line': {'color': 'black', 'width': 1},
                },
        showlegend=True,
        text='market decline',
        name='SELL'
    ),
    # try creating isosphere instead!
    # or octahedron!
    # or perfect cube!
    go.Isosurface(
        x=xs,
        y=ys,
        z=zs,
        opacity=0.15,
        value=preds.astype(int),
        colorscale=['magenta', 'cyan'],
    )
]
)

fig.show()

quit()
fig = go.Figure()

fig.add_trace(mesh_plot(vertices, faces))
fig.add_trace(wireframe_plot(vertices, faces))
# fig.add_trace(go.Scatter3d(
#     x=vertices.T[0][:3], y=vertices.T[1][:3], z=vertices.T[2][:3], mode='markers', marker={'color': 'red'}))


fig.update_layout(title_text='Icosphere', height=600, width=600)
fig.show()

# fig = make_subplots(rows=2, cols=3,
#                     specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}],
#                            [{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]])

# for i in range(2):
#     for j in range(3):

#         nu = 1 + j + 3*i
#         vertices, faces = icosphere.icosphere(nu)
#         print(faces)
#         fig.add_trace(mesh_plot(vertices, faces), row=i+1, col=j+1)
#         fig.add_trace(wireframe_plot(vertices, faces), row=i+1, col=j+1)
#         fig.add_trace(go.Scatter3d(
#             x=vertices.T[0], y=vertices.T[1], z=vertices.T[2], mode='markers', marker={'color': 'red'}))

# fig.update_layout(title_text='Different values of nu',
#                   height=600, width=800, showlegend=False)
# fig.show()

# fig = go.Figure(data=[
#     go.Isosurface(
#         x=vertices[:, 0],
#         y=vertices[:, 1],
#         z=vertices[:, 2],
#         opacity=0.15,
#         value=[1 for i in range(len(vertices[:, 0]))],
#         # value=preds.astype(int),
#         colorscale=['magenta', 'cyan'],
#     )
# ]
# )

# fig.show()
# x = vertices.T[0]
# xs = []
# for i in range(50):
#     xs.append(x * i)
# xs = np.concatenate(xs)
# # print(xs)

# y = vertices.T[1]
# ys = []
# for i in range(50):
#     ys.append(y * i)
# ys = np.concatenate(ys)

# z = vertices.T[2]
# zs = []
# for i in range(50):
#     zs.append(z * i)
# zs = np.concatenate(zs)

# fig = go.Figure(data=[
#     go.Isosurface(
#         x=xs,
#         y=ys,
#         z=zs,
#         opacity=0.15,
#         value=[1 for _ in range(len(zs))],
#         # value=preds.astype(int),
#         colorscale=['magenta', 'cyan'],
#     )
#     # go.Scatter3d(x=vertices.T[0], y=vertices.T[1],
#     #              z=vertices.T[2], mode='markers')
# ]
# )

# fig.show()
