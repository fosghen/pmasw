"""
Класс считывания сейсмических данных.

Класс позволяет считывать сейсмические данные форматов:
    segy, baykal.
"""

import numpy as np
from segyio import dt as dt_
from segyio import open as open_


class DataLoader:
    """
    Класс считывания сейсмических данных.

    Класс считывает данные форматов segy, baykal.

    ...

    Attributes
    ----------
    path : str
        Путь до файла.

    format : str
        Формат данных.

    n_components : str
            Количество компонент.

    component : str | None
            Компонетна данных.

    Methods
    -------


    """

    def __init__(self, path,
                 format,
                 n_components="3C",
                 component="Z"):

        self.path = path
        self.format = format
        self.n_components = n_components
        self.component = component


    @property
    def path(self):
        """
        Возвращает путь до файла.

        Returns
        -------
        path : str
            Путь до файла.

        """
        return self._path


    @path.setter
    def path(self, value):
        """
        Принимает путь до файла.

        Parameters
        ----------
        value : str
            Путь до файла.

        """
        if not isinstance(value, str):
            raise ValueError("Путь должен быть строкой")

        self._path = value


    @property
    def format(self):
        """
        Возвращает формат загружаемых данных.

        Returns
        -------
        format : str
            Формат данных.

        """
        return self._format


    @format.setter
    def format(self, value):
        """
        Принимает формат загружаемых данных.

        Parameters
        ----------
        value : str
            Формат данных.

        """
        if not isinstance(value, str):
            raise ValueError("Формат должен быть строкой")

        if value not in {"segy", "baykal"}:
            raise ValueError("Формат должен быть 'segy' или 'baykal'")
        self._format = value


    @property
    def n_components(self):
        """
        Возвращает количество компонент.

        Returns
        -------
        n_components : str
            Количество компонент.

        """
        return self._n_components


    @n_components.setter
    def n_components(self, value):
        """
        Принимает количество компонент.

        Parameters
        ----------
        value : str
            Количество компонент.

        """
        if not isinstance(value, str):
            raise ValueError("Количество компонент должно быть строкой")

        if value not in {"3C", "1C"}:
            raise ValueError("Количество компонент должено быть"
                             " 'segy' или 'baykal'")

        self._n_components = value


    @property
    def component(self):
        """
        Возвращает компоненту записи данных.

        Returns
        -------
        component : str | None
            Компонетна данных.

        """
        return self._component


    @component.setter
    def component(self, value):
        """
        Принимает компонентну записи данных.

        Parameters
        ----------
        value : str | None
            Компонента данных.

        """
        if not isinstance(value, str):
            raise ValueError("Компонента должна быть строкой")


        if value not in ("Z", "X", "Y"):
            raise ValueError("Компонента должена быть"
                             " 'Z' или 'X', или 'Y'")

        self._component = value


    @staticmethod
    def read_segy(path):
        """
        Читает файлы формата segy.

        Чтение файлов формата segy, используется библиотека segyio

        Parameters
        ----------
        path : srt
            Путь до файла.

        Returns
        -------
        data : ndarray[dtype: float64, dim = 2]
            Двумерный массив данных.

        dt : float
            Время дексретизации в секундах.

        """
        try:
            segy_file = open_(path, ignore_geometry=True, endian='big')
        except: # Выяснить какой тип ошибки соответсвует неверному endian
            segy_file = open_(path, ignore_geometry=True, endian='little')
        data = np.array([np.copy(tr) for tr in segy_file.trace[:]],
                        dtype=np.float64).T
        dt = dt_(segy_file) * 1e-6
        return data, dt
