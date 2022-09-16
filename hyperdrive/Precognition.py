from FileOps import FileReader


class Oracle:
    def __init__(self):
        self.reader = FileReader()

    def load_model_pickle(self, name):
        filename = f'models/latest/{name}.pkl'
        return self.reader.load_pickle(filename)

    def predict(self, data):
        model = self.load_model_pickle('model')
        return model.predict(data)
