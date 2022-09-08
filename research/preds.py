import plotly.graph_objects as go
import pickle
import numpy as np
from sklearn.decomposition import PCA

with open('research/X.pkl', 'rb') as file:
    X = pickle.load(file)

with open('research/y.pkl', 'rb') as file:
    y = pickle.load(file)


# def predict(data):
#     filename = 'research/models/latest/model.pkl'

#     with open(filename, 'rb') as file:
#         model = pickle.load(file)
#         return model.predict(data)

# num_points = 50
# reducer = PCA(n_components=3)
# X_transformed = reducer.fit_transform(X)
# component_x, component_y, component_z = X_transformed.T
# min_x, max_x = min(component_x), max(component_x)
# min_y, max_y = min(component_y), max(component_y)
# min_z, max_z = min(component_z), max(component_z)
# lin_x = np.linspace(min_x, max_x, num_points)
# lin_y = np.linspace(min_y, max_y, num_points)
# lin_z = np.linspace(min_z, max_z, num_points)
# xx, yy, zz = np.meshgrid(lin_x, lin_y, lin_z)
# xs = xx.flatten()
# ys = yy.flatten()
# zs = zz.flatten()


# reduced = np.array([xs, ys, zs]).T
# unreduced = reducer.inverse_transform(reduced)
# preds = predict(unreduced)

# with open('research/xs.pkl', 'wb') as file:
#     pickle.dump(xs, file)

# with open('research/ys.pkl', 'wb') as file:
#     pickle.dump(ys, file)

# with open('research/zs.pkl', 'wb') as file:
#     pickle.dump(zs, file)

# with open('research/preds.pkl', 'wb') as file:
#     pickle.dump(preds, file)

# with open('research/component_x.pkl', 'wb') as file:
#     pickle.dump(component_x, file)

# with open('research/component_y.pkl', 'wb') as file:
#     pickle.dump(component_y, file)

# with open('research/component_z.pkl', 'wb') as file:
#     pickle.dump(component_z, file)


# pts = np.loadtxt(np.DataSource().open(
#     'https://raw.githubusercontent.com/plotly/datasets/master/mesh_dataset.txt'))
# x, y, z = pts.T
with open('research/xs.pkl', 'rb') as file:
    xs = pickle.load(file)

with open('research/ys.pkl', 'rb') as file:
    ys = pickle.load(file)

with open('research/zs.pkl', 'rb') as file:
    zs = pickle.load(file)

with open('research/preds.pkl', 'rb') as file:
    preds = pickle.load(file)

with open('research/component_x.pkl', 'rb') as file:
    component_x = pickle.load(file)

with open('research/component_y.pkl', 'rb') as file:
    component_y = pickle.load(file)

with open('research/component_z.pkl', 'rb') as file:
    component_z = pickle.load(file)

# xs_buy = [_ for idx, _ in enumerate(xs) if preds[idx]]
# ys_buy = [_ for idx, _ in enumerate(ys) if preds[idx]]
# zs_buy = [_ for idx, _ in enumerate(zs) if preds[idx]]

# fig = go.Figure(data=[go.Mesh3d(x=xs_buy, y=ys_buy, z=zs_buy,
#                                 # alphahull=5,
#                                 opacity=0.4,
#                                 color='cyan')])
# fig = go.Figure(data=[go.Mesh3d(x=xs, y=ys, z=zs,
#                                 alphahull=5,

#                                 intensity=preds.astype(int),
#                                 opacity=0.4,
#                                 colorscale=['magenta', 'cyan']
#                                 # =['cyan']*len(xs)
#                                 )
#                       ]
#                 )

# fig.show()


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
