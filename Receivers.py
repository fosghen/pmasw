"""Класс системы наблюдений расстановки приёнмиков."""


import numpy as np


class Receivers:
    """
    Класс системы наблюдений расстановки приёнмиков.

    Класс содержтт в себе координаты приёмников относительно
    оси X и относительно оси Y. Используется совместно с PMASW.

    ...

    Attributes
    ----------
    x : ndarray[dtype: float64, dim = 1]
        Координаты приёмников относительно оси X.

    y : ndarray[dtype: float64, dim = 1]
        Координаты приёмников относительно оси Y.

    """

    def __init__(self, x_rec, y_rec):
        """
        Установление координат приёмников.

        Parametres
        ----------
        x : ndarray[dtype: float64, dim = 1]
            Координаты приёмников относительно оси X.

        y : ndarray[dtype: float64, dim = 1]
            Координаты приёмников относительно оси Y.

        """
        self.x = x_rec
        self.y = y_rec


    @property
    def x(self):
        """
        Возвращает координат приёмников относительно оси X.

        Returns
        -------
        x : ndarray[dtype: float64, dim = 1]
            Координаты приёмников относительно оси X в м.

        """
        return self._x


    @x.setter
    def x(self, value):
        """
        Устанавливает координат приёмников относительно оси X.

        Parameters
        ----------
        value : ndarray[dtype: float64 | int32, dim = 1]
            Координаты приёмников относительно оси X в м.

        """
        if not isinstance(value, np.ndarray):
            raise ValueError("Подаваемый массив должен быть типа"
                             "numpy.ndarray")

        if len(value) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if (value.dtype != np.int32) and (value.dtype != np.float64):
            raise ValueError("Подаваемый массив должен состоять из типов"
                             "данных float64 или int32")

        if len(value.shape) != 1:
            raise ValueError("Размер массива должен быть равен 1")

        self._x = np.float64(value)


    @property
    def y(self):
        """
        Возвращает координат приёмников относительно оси Y.

        Returns
        -------
        y : ndarray[dtype: float64, dim = 1]
            Координаты приёмников относительно оси Y в м.

        """
        return self._y


    @y.setter
    def y(self, value):
        """
        Устанавливает координат приёмников относительно оси Y.

        Parameters
        ----------
        value : ndarray[dtype: float64 | int32, dim = 1]
            Координаты приёмников относительно оси Y в м.

        """
        if not isinstance(value, np.ndarray):
            raise ValueError("Подаваемый массив должен быть типа"
                             "numpy.ndarray")

        if len(value) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if (value.dtype != np.int32) and (value.dtype != np.float64):
            raise ValueError("Подаваемый массив должен состоять из типов"
                             "данных float64 или int32")

        if len(value.shape) != 1:
            raise ValueError("Размер массива должен быть равен 1")

        self._y = np.float64(value)
