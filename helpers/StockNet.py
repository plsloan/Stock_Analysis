import tensorflow as tf
from tensorflow import keras


class StockNet(keras.Model):
    def __init__(self):
        self.model = keras.models.Sequential()

    def fit(self, X, Y, batch_size=8, epochs=1, validation_data=None, verbose=1):
        history = self.model.fit(
            x=X,
            y=Y,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=validation_data,
            verbose=verbose
        )
        return history

    def predict(self, X):
        predictions = self.model.predict(X)
        return predictions
