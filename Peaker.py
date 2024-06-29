"""
Модуль для пикировная дисперсионных кривых.

Модуль выполняет пикирование дисперсионных кривых по
массиву енергии в зависимости от скорости и частоты в некоторых пределах.
"""

import numpy as np
from scipy.interpolate import interp1d


class Peaker:
    """Класс для пикировки дисперисонных кривых."""

    def __init__(self,
                 v_p,
                 f_p,
                 v_step_low_freq,
                 v_step_high_freq):
        """
        Установка диапазонов пикирования.

        Parameters
        ----------
        v_p : ndarray[dtype : float, dim=1]
            Скорости, по которым определяется
            максимум амплитуды.

        f_p : ndarray[dtype : float, dim=1]
            Диапазон частот, в доль которых определяется
            максимум амплитуды.

        v_step_low_freq : int | float
            Диапазон для поиска по скоростям на минимальной частоте.

        v_step_high_freq : int | float
            Диапазон для поиска по скоростям на максимальной частоте.
        """
        self.v_p = v_p
        self.f_p = f_p
        self.v_step_high_freq = v_step_high_freq
        self.v_step_low_freq = v_step_low_freq
        self._interpolator = None

        self._interpolation_vf()


    @property
    def v_p(self):
        """
        Возвращает диапазон фазовых скоростей.

        Returns
        -------
        v_p : ndarray[dtype: float64, dim = 1]
            Массив фазовых скоростей.

        """
        return self._v_p


    @v_p.setter
    def v_p(self, value):
        """
        Устанавливает набор фазовых скоростей.

        Parameters
        ----------
        value : ndarray[dtype: float64 | int32, dim = 1]
            Массив фазовых скоростей.

        """
        if not isinstance(value, np.ndarray):
            raise ValueError("Подаваемый массив должен быть типа"
                             "numpy.ndarray")

        if len(value) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if (value.dtype != np.int32) and (value.dtype != np.float64):
            raise ValueError("Подаваемый массив должен состоять из типов"
                             "данных float64 или int32")

        if any(value <= 0):
            raise ValueError("Подаваемый массив должен состоять из "
                             "положительных чисел")

        if len(value.shape) != 1:
            raise ValueError("Размер массива должен быть равен 1")

        self._v_p = value


    @property
    def v_p_interp(self):
        """
        Возвращает диапазон фазовых скоростей.

        Returns
        -------
        v_p_interp : ndarray[dtype: float64, dim = 1]
            Массив интерполированных фазовых скоростей.

        """
        return self._v_p_interp


    @property
    def v_step_low_freq(self):
        """
        Возвращает минимальную фазовую скорость.

        Returns
        -------
        v_step_low_freq : float
            Минимальная фазовая скорость.

        """
        return self._v_step_low_freq


    @v_step_low_freq.setter
    def v_step_low_freq(self, value):
        """
        Устанавливает минимальную фазовую скорость.

        Parameters
        ----------
        value : float
            Минимальная фазовая скорость.

        """
        if not isinstance(value, (int, float)):
            raise ValueError("Шаг по фазовой скорости должн быть числом")

        elif value <= 0:
            raise ValueError("Шаг по фазовой скорости должна быть"
                             " положительным числом")

        self._v_step_low_freq = float(value)


    @property
    def v_step_high_freq(self):
        """
        Возвращает минимальную фазовую скорость.

        Returns
        -------
        v_step_high_freq : float
            Минимальная фазовая скорость.

        """
        return self._v_step_high_freq


    @v_step_high_freq.setter
    def v_step_high_freq(self, value):
        """
        Устанавливает минимальную фазовую скорость.

        Parameters
        ----------
        value : float
            Минимальная фазовая скорость.

        """
        if not isinstance(value, (int, float)):
            raise ValueError("Шаг по фазовой скорости должн быть числом")

        elif value <= 0:
            raise ValueError("Шаг по фазовой скорости должна быть"
                             " положительным числом")

        self._v_step_high_freq = float(value)


    @property
    def f_p(self):
        """
        Возвращает диапазон частот.

        Returns
        -------
        f_p : ndarray[dtype: float64, dim = 1]
            Массив частот.

        """
        return self._f_p


    @f_p.setter
    def f_p(self, value):
        """
        Устанавливает набор частот.

        Parameters
        ----------
        value : ndarray[dtype: float64 | int32, dim = 1]
            Массив частот.

        """
        if not isinstance(value, np.ndarray):
            raise ValueError("Подаваемый массив должен быть типа"
                             "numpy.ndarray")

        if len(value) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if (value.dtype != np.int32) and (value.dtype != np.float64):
            raise ValueError("Подаваемый массив должен состоять из типов"
                             "данных float64 или int32")

        if any(value <= 0):
            raise ValueError("Подаваемый массив должен состоять из "
                             "положительных чисел")

        if len(value.shape) != 1:
            raise ValueError("Размер массива должен быть равен 1")

        self._f_p = value


    @property
    def f_p_interp(self):
        """
        Возвращает диапазон фазовых скоростей.

        Returns
        -------
        f_p_interp : ndarray[dtype: float64, dim = 1]
            Массив интерполированных частот.

        """
        return self._f_p_interp


    def _interpolation_vf(self):
        """Создание интерполятора."""
        self._interpolator = interp1d(self._f_p, self._v_p)


    def peak_dispersuon_curve(self, vf, velocities, freqs):
        """
        Определение максимум амплитуды массива vf вдоль оси freq.

        По введённым пользователем v_p и f_p выполняется интерполяция
        для получения границ поиска максимума энергии вдоль частот freqs.

        Parameters
        ----------
        vf : ndarray[dtype : float64, dim=2]
            Массив распределения энергии в зависимости от скоростей и частот.
            [vel_axis, freq_axis]

        velocities : ndarray[dtype : float64, dim=1]
            Массив скоростей соответствующих скоростоям в vf.

        freqs: ndarray[dtype : float64, dim=1]
            Массив частот соответствующих частотам в vf.

        """
        # Выбираем частоты в указанном диапазоне
        self._f_p_interp = freqs[(self._f_p.min() <= freqs) * \
                                 (freqs <= self._f_p.max())]

        # Интерполятор диапазона скоростей
        self._interpolator_v_step = interp1d(self._f_p[[0, -1]],
                                             [self._v_step_low_freq,
                                              self._v_step_high_freq])

        # Интерполируем скорости
        self._v_p_interp = self._interpolator(self._f_p_interp)

        # Интерполируем диапазон скоростей
        self._v_step = self._interpolator_v_step(self._f_p_interp)

        # Определяем верхнюю границу скоростей
        v_p_interp_upper = np.clip(self._v_p_interp + self._v_step,
                                   a_max=velocities.max(),
                                   a_min=velocities.min())

        # Определяем нижнюю границу скоростей
        v_p_interp_lower = np.clip(self._v_p_interp - self._v_step,
                                   a_max=velocities.max(),
                                   a_min=velocities.min())

        # Орпеделяем индексы верхней границы скоростей
        upper_indexes = np.argmin(np.abs(velocities - \
                            v_p_interp_upper[np.newaxis].T),
                                  axis=1)

        # Определяем индексы нижней границы скоростей
        lower_indexes = np.argmin(np.abs(velocities - \
                            v_p_interp_lower[np.newaxis].T),
                                  axis=1)

        f_0 = np.where(freqs == self._f_p_interp[0])[0][0]

        ind_max = np.array([np.argmax(vf[lower_indexes[f_i] :\
                                         upper_indexes[f_i], f_0 + f_i]) + \
                lower_indexes[f_i] for f_i in range(len(self._f_p_interp))])

        return (self._f_p_interp,
               v_p_interp_lower,
               v_p_interp_upper,
               velocities[ind_max])
