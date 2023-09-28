"A wrapper around matplotlib to simplify common operations."
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
plt.show
class Graph():
    def __init__(self) -> None:
        self._figure = plt.figure()
        self._axes:plt.Axes = self._figure.add_subplot(111, projection='3d')
        self._axes.legend()
    def show(self, blocking=True):
        # self._figure.show() # @note it appears running this directly is unsupported?
        plt.show()
        # import time
        # while True:
        #     time.sleep(100)
    def addPoint(self, point: list, color:str="red"):
        self._axes.scatter(*point, c=color)
    def addShape(self, shape: list[list]):
        "First parameter expects a list of vectors"
        self._axes.add_collection3d(Poly3DCollection([shape], facecolors=["red"]))