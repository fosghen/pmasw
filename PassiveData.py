"""Класс пассивых сейсмических данных."""

import numpy as np


class PassiveData:
    """
    Класс пассивных сейсмических данных.

    Класс хранит сейсмическую запись и её
    время дескретизации. Используется совместно
    с DataLoader, PassiveProcesser, PMASW.

    ...

    Attributes
    ----------
    dt : float
        Время дескретизации сигнала.

    seismogram : ndarray[dtype: float64, dim = 2]
            Массив сейсмичсеской записи.
            [tempor_axis, spatial_axis]

    """

    def __init__(self, data, dt):
        """
        Определение сейсмических данных и врмени дескретизации.

        Parameters
        ----------
        data : ndarray[dtype: float64, dim = 2]
            Массив сейсмичсеской записи.
            [tempor_axis, spatial_axis]

        dt : float
            Время десретизации сигнала.

        fs : int
            Частота дескретизации сигнала.

        nt : int
            Количество отсчётов по времени.

        nx : int
            Количество трасс.

        """
        self.seismogram = data
        self.dt = dt
        self._fs = int(1 / dt)


    @property
    def dt(self):
        """
        Возвращает время дескретизации обрабатываемого сигнала.

        Returns
        -------
        dt : float
            Время дескретизации сигнала.

        """
        return self._dt


    @dt.setter
    def dt(self, value):
        """
        Устанавливает время дескретизации обрабатываемого сигнала.

        Parameters
        ----------
        value : float | int
            Время дескретизации сигнала.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Время дескретизации должно быть числом")

        if value < 0:
            raise ValueError("Время дескретизации должно быть"
                             " положительным числом")

        self._dt = float(value)
        self._fs = int(1 / self._dt)


    @property
    def fs(self):
        """
        Возвращает частоту дескретизации.

        Returns
        -------
        fs : int
            Частота дескретизации.

        """
        return int(1 / self._dt)


    @fs.setter
    def fs(self, value):
        """
        Устанавливает частоту дескретизации.

        Parameters
        ----------
        value : int
            Частота дескретизации.

        """
        if not isinstance(value, int):
            raise ValueError("Частота дескретизации должна быть целым числом")

        if value < 0:
            raise ValueError("Частота дескретизации должна быть"
                             " положительным числом")

        self._fs = value
        self._dt = float(1 / self._fs)


    @property
    def nt(self):
        """
        Возвращает количество отсчётов по времени.

        Returns
        -------
        nt : int
            Количество отсчётов по времени.

        """
        return self._nt


    @property
    def nx(self):
        """
        Возвращает количество трасс.

        Returns
        -------
        nx : int
            Количество трасс.

        """
        return self._nx


    @property
    def seismogram(self):
        """
        Возвращает сейсмическую запись.

        Returns
        -------
        seismogram : ndarray[dtype: float64, dim = 2]
            Массив сейсмичсеской записи.
            [tempor_axis, spatial_axis]

        """
        return self._seismogram


    @seismogram.setter
    def seismogram(self, value):
        """
        Устанавливает сейсмическую запись.

        Parameters
        ----------
        value : ndarray[dtype: float64 | int32, dim = 2]
            Массив сейсмичкской записи.
            [tempor_axis, spatial_axis]

        """
        if not isinstance(value, np.ndarray):
            raise ValueError("Подаваемый массив должен быть типа"
                             "numpy.ndarray")

        if len(value) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if (value.dtype != np.int32) and (value.dtype != np.float64):
            raise ValueError("Подаваемый массив должен состоять из типов"
                             "данных float64 или int32")

        if not isinstance(value[0], np.ndarray):
            raise ValueError("Подаваемый массив должен состоять из "
                             "массивов типа numpy.array")

        if len(value[0]) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if len(value.shape) != 2:
            raise ValueError("Размер массива должен быть равен 2")

        self._seismogram = np.float64(value)
        self._nt, self._nx = value.shape

