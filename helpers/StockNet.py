import tensorflow as tf
from tensorflow import keras


class StockNet(keras.Model):
    def __init__(self):
        self.model = keras.models.Sequential()
