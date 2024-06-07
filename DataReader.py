"""
Класс считывания сейсмических данных.

Класс позволяет считывать сейсмические данные форматов:
    segy, baykal.
"""

from pathlib import Path
from struct import unpack
from warnings import catch_warnings, simplefilter

import numpy as np
from segyio import dt as dt_
from segyio import open as open_

from .PassiveData import PassiveData


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
    read_segy(path)
        Читение файлы формата segy.

    read_baykal(path)
        Чтение файлов формата baykal.

    read_data(path)
        Чтение файла сейсмических данных.

    """

    def __init__(self, path,
                 format,
                 n_components="3C",
                 component="Z"):
        """
        Установка необходимых параметров для считыания данных.

        Parameters
        ----------
        path : str
            Путь до файла с данными.

        format : str
            Формат считываемого файла.

        n_components : str, default = "3C"
            Количество компонент в записи данных.
            {"3C", "1C"}

        component : str, default = "Z"
            Компонента данных.
            {"Z", "X", "Y"}

        """
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
    def _open_check_warn(path):
        """
        Перехватывает предупреждение.

        Перехватывание предупреждения о том, что endian неверен и
        открываем с другим endian.

        Parameters
        ----------
        path : srt
            Путь до файла.

        Returns
        -------
        segy_file : segyio.SegyFile
            Открытый segy-файл.

        """
        with catch_warnings(record=True) as w:
            simplefilter("always")
            try:
                segy_file = open_(path, ignore_geometry=True, endian='big')
            except Exception as e: # Выяснить какой тип ошибки соответсвует
                                   # неверному endian
                print(f"Исключение: {e}")
                segy_file = open_(path, ignore_geometry=True, endian='little')
            if w:
                segy_file = open_(path, ignore_geometry=True, endian='little')
        return segy_file


    @staticmethod
    def read_segy(path):
        """
        Читает файлы формата segy.

        Чтение файлов формата segy с использованием
        библиотеки segyio.

        Parameters
        ----------
        path : srt
            Путь до файла.

        Returns
        -------
        data : ndarray[dtype: float64, dim = 2]
            Двумерный массив данных.
            [tempor_axis, spatial_axis]

        dt : float
            Время дексретизации в секундах.

        """
        segy_file = DataLoader._open_check_warn(path)
        data = np.array([np.copy(tr) for tr in segy_file.trace[:]],
                        dtype=np.float64).T
        dt = dt_(segy_file) * 1e-6
        return data, dt


    @staticmethod
    def read_baykal(path):
        """
        Читает файлы формата baykal.

        Чтение файлов формата baykal, выполняется чтение байтов
        файла.

        Parameters
        ----------
        path : srt
            Путь до файла.

        Returns
        -------
        data : ndarray[dtype: float64, dim = 2]
            Двумерный массив данных.
            [tempor_axis, spatial_axis]

        dt : float
            Время дексретизации в секундах.

        """
        with Path(path).open('rb') as f:
            channels = unpack('H', f.read(2))[0] # Колличество каналов
            f.read(2)
            _ = unpack('H', f.read(2))[0] # Версия
            _ = unpack('H', f.read(2))[0] # День
            _ = unpack('H', f.read(2))[0] # Месяц
            _ = unpack('H', f.read(2))[0] # Год
            f.read(6)
            _ = unpack('H', f.read(2))[0] # Разрядность АЦП
            f.read(2)
            freq = unpack('H', f.read(2))[0] # Частота дискретизации
            f.read(8)
            station_name = unpack('9s7c', f.read(16))[0] # Название станции
            station_name = str(station_name).replace('b', '')
            station_name = station_name.replace("'", '')
            f.read(24)
            _ = unpack('d', f.read(8))[0] # Широта
            _ = unpack('d', f.read(8))[0] # Долгота
            f.read(16)
            _ = unpack('Q', f.read(8))[0] # Начальное время
            f.read(8)
            channels_number = [] # номер канала
            channels_name = [] # имя канала
            sensors_type = [] # тип сенсора
            channels_coef = [] # коэффициент канала
            for i in range(channels):
                # Номер канала
                channels_number.append(unpack('H', f.read(2))[0])
                f.read(6)
                # Имя канала
                channels_name.append(unpack('6i', f.read(24))[0])
                # Тип сенсора
                sensors_type.append(unpack('6i', f.read(24))[0])
                # Коэффициент канала
                channels_coef.append(unpack('d', f.read(8))[0])
                f.read(8)

            data = np.fromfile(f, dtype = 'int')
            data = np.reshape(data, [channels, len(data) // channels],
                              order='F')
            dt = 1 / freq
            return data.T, dt


    def read_data(self):
        """
        Считывание сейсмических данных.

        Считывание выполняется на основе иницализированных
        параметров: формата, количества компонент и компоненты.

        Returns
        -------
        data : PassiveData
            Сейсмические данные.

        """
        if self._format == "segy":
            try:
                data, dt = DataLoader.read_segy(self._path)
            except RuntimeError:
                raise ValueError("Неверный тип данных")

        if self._format == "baykal":
            try:
                data, dt = DataLoader.read_baykal(self._path)
            except ValueError:
                raise ValueError("Неверный тип данных")

        if self._n_components == '3C':
            if self._component == 'Z':
                data = data[:,0::3]
            elif self._component == 'X':
                data = data[:,1::3]
            elif self._component == 'Y':
                data = data[:,3::3]

        return PassiveData(data = data,
                           dt = dt)

