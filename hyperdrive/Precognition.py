import numpy as np
from sklearn.decomposition import PCA
from FileOps import FileReader
from Calculus import Calculator


class Oracle:
    def __init__(self):
        self.reader = FileReader()
        self.calc = Calculator()

    def load_model_pickle(self, name):
        filename = f'models/latest/{name}.pkl'
        return self.reader.load_pickle(filename)

    def predict(self, data):
        model = self.load_model_pickle('model')
        return model.predict(data)

    def visualize(self, refinement, dimensions, X, increase_percent=0):
        # recommended in the range [4, 100]
        num_points = refinement
        reducer = PCA(n_components=dimensions)
        X_transformed = reducer.fit_transform(X)

        component_x, component_y, *rest = X_transformed.T
        component_z = rest[0] if rest else []
        all_coords = np.concatenate((component_x, component_y, component_z))
        # or method='mean'
        centroid = self.calc.calc_centroid(X_transformed, method='extrema')
        super_min = min(all_coords)
        super_min -= abs(super_min) * increase_percent
        super_max = max(all_coords)
        super_max += abs(super_max) * increase_percent
        radius = (super_max - super_min) / 2
        lins = [np.linspace(
            component - radius,
            component + radius,
            num_points
        ) for component in centroid]
        # generalize everything below for # of dims!!!!!!!!!
        xx, yy, zz = np.meshgrid(*lins)
        xs = xx.flatten()
        ys = yy.flatten()
        zs = zz.flatten()

        reduced = np.array([xs, ys, zs]).T
        unreduced = reducer.inverse_transform(reduced)
        preds = self.predict(unreduced)
