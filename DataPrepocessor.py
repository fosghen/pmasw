"""Класс для предобработки данных."""


import numpy as np
from scipy.signal import butter, detrend, filtfilt


class DataPreprocessor:
    """
    Класс для предобработки данных.

    Класс используется для подготовки данных перед
    ипользованием класса PMASW.

    ...

    Methods
    -------
    decimation(fs_decim)
        Прореживание данных.

    detrending()
        Удаление линейного тренда из данных.

    """

    def __init__(self, data):
        """
        Принимает данные для обработки.

        Parameters
        ----------
        data : PassiveData
            Сейсмические пассивные данные.

        """
        self._data = data


    def decimation(self, f_max):
        """
        Прореживание пассивных сейсмических данных.

        Прореживание матрицы данных по времени относительно заданой
        граничной частоты обработки. Включает в себя полосовую
        фильтрацию и прореживание временных отсчетов данных.

        Parameters
        ----------
        f_max: int
            Граничная частота обработки (Гц).

        """
        # определение фактора прореживания относительно текущей частоты
        # Найквиста и заданной граничной частоты обработки
        fn = self.data.fs // 2
        resamp = int(fn / f_max)
        fs_decim = int(self.data.fs / resamp)

        # антиалясинговый (полосой) фильтр для частот в диапазоне
        # [1: fs_decim - 1]
        b, a = butter(5, np.array([1, fs_decim - 1]),
                      btype='band',
                      analog=False,
                      fs=self.data.fs)

        filtered_data = np.array([filtfilt(b, a, self.data.seismogram[:, ii]) \
                                  for ii in range(self.data.nx)]).T

        # прореживание временных отсчетов в данных
        data_decim = filtered_data[:: resamp, :] * resamp

        self.data.seismogram = data_decim
        self.data.fs = fs_decim


    def detrending(self):
        """Удаление линейного тренда из данных."""
        detrended_data = np.array([detrend(self.data.seismogram[:, ii]) \
                                   for ii in range(self.data.nx)]).T

        self.data.seimsmogram = detrended_data
