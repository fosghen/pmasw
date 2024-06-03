"""Класс обработки методом PMASW."""

import numpy as np

from fast_pmasw import compute_energy_

PI = 3.1415926535897932384626433832


class PMASW:
    """
    Класс обработки сейсмических данных.

    Класс обработки сейсмических данных с помощью
    метода пассивного многоканального анализа
    поверхностных волн (PMASW).

    ...

    Attributes
    ----------
    dt : float
        Время дескретизации сигнала.

    v_min : float
        Минимальная фазовая скорость.

    v_max : float
        Максимальная фазовая скорость.

    v_step : float
        Шаг по фазовым скоростям.

    f_min : float
        Минимальная частота.

    f_max : float
        Максимальная частота.

    theta_min : float
        Минимальный азимут в градусах.

    theta_max : float
        Максимальный азимут в градусах.

    theta_step : float
        Шаг по азимутам в градусах.

    nt : int
        Количество обрабатываемых отсчётов.

    Methods
    -------
    define_velocities()
        Устанавливает набор фазовых скоростей.

    define_thetas()
        Устанавливает набор азимутов.

    define_freqs()
        Устанавливает набор частот.

    compute_energy(data, recievers)
        Вычисление энергии для всех скоростей, частот, азимутов.

    """

    def __init__(self, dt, nt, v_max, f_max):
        """
        Создание необходимых параметров для обработки.

        Parameters
        ----------
        dt : float | int
            Время дескретизации сигнала.

        nt : int
            Количество обрабатываемых отсчётов.

        v_max : float | int
            Максимальная фазовая скорость.

        f_max : float | int
            Максимальная частота.

        """
        # Установка значений по умолчанию
        self._f_min = 0.
        self._v_min = 1.
        self._v_step = 10.
        self._theta_min = PI * (0 / 180)
        self._theta_max = PI * (180 / 180)
        self._theta_step = PI * (10 / 180)
        self._freqs = np.array([])
        self._velocities = np.array([])
        self._thetas = np.array([])
        self._dt = 1.
        self._nt = 100.
        self._v_max = 100.
        self._f_max = 100.
        self._energy = np.array([])
        self._en_vel_freq = np.array([])
        self._en_f_theta = np.array([])

        self.dt = dt
        self.nt = nt
        self.v_max = v_max
        self.f_max = f_max
        self.define_thetas()


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

        if value <= 0:
            raise ValueError("Время дескретизации должно быть"
                             " положительным числом")

        self._dt = float(value)
        self.define_freqs()


    @property
    def v_min(self):
        """
        Возвращает минимальную фазовую скорость.

        Returns
        -------
        v_min : float
            Минимальная фазовая скорость.

        """
        return self._v_min


    @v_min.setter
    def v_min(self, value):
        """
        Устанавливает минимальную фазовую скорость.

        Parameters
        ----------
        value : float
            Минимальная фазовая скорость.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Минимальная фазовая скорость должна быть числом")

        if value <= 0:
            raise ValueError("Минимальная фазовая скорость должна быть"
                             " положительным числом")

        if value >= self._v_max:
            raise ValueError("Минимальная фазовая скорость должна быть"
                             " меньше максимальной фазовой скорости")

        self._v_min = float(value)
        self.define_velocities()


    @property
    def v_max(self):
        """
        Возвращает максимальную фазовую скорость.

        Returns
        -------
        v_max : float
            Максимальная фазовая скорость.

        """
        return self._v_max


    @v_max.setter
    def v_max(self, value):
        """
        Устанавливает максимальную фазовую скорость.

        Parameters
        ----------
        value : float | int
            Максимальная фазовая скорость.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Максимальная фазовая скорость должна"
                             " быть числом")

        if value <= 0:
            raise ValueError("Максимальная фазовая скорость должна быть"
                             " положительным числом")

        if value <= self._v_min:
            raise ValueError("Максимальная фазовая скорость должна быть"
                             " больше минимальной фазовой скорости")

        self._v_max = float(value)
        self.define_velocities()


    @property
    def v_step(self):
        """
        Возвращает шаг по фазовым скоростям.

        Returns
        -------
        v_step : float
            Шаг по фазовым скоростям.

        """
        return self._v_step


    @v_step.setter
    def v_step(self, value):
        """
        Устанавливает шаг по фазовым скоростям.

        Parameters
        ----------
        value : float | int
            Шаг по фазовым скоростям.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Шаг по фазовым скоростям должен быть числом")

        if value <= 0:
            raise ValueError("Шаг по фазовым скоростям должен быть"
                             " положительным числом")

        self._v_step = float(value)
        self.define_velocities()


    @property
    def f_min(self):
        """
        Возвращает минимальную частоту.

        Returns
        -------
        f_min : float
            Минимальная частота.

        """
        return self._f_min


    @f_min.setter
    def f_min(self, value):
        """
        Устанавливает минимальную частоту.

        Parameters
        ----------
        value : float | int
            Минимальная частота.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Минимальная частота должна быть числом")

        if value <= 0:
            raise ValueError("Минимальная частота должна быть"
                             " положительным числом")

        if value >= self._f_max:
            raise ValueError("Минимальная частота должна быть"
                             " меньше максимальной частоты")

        self._f_min = float(value)
        self.define_freqs()


    @property
    def f_max(self):
        """
        Возвращает максимальную частоту.

        Returns
        -------
        f_max : float
            Максимальная частота.

        """
        return self._f_max


    @f_max.setter
    def f_max(self, value):
        """
        Устанавливает максимальную частоту.

        Parameters
        ----------
        value : float | int
            Максимальная частота.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Максимальная частота должна быть числом")

        if value <= 0:
            raise ValueError("Максимальная частота должна быть"
                             " положительны мчислом")

        if value > 1 / 2 / self._dt:
            raise ValueError("Максимальная частота должна быть ниже"
                            " частоты Найквиста")

        if value <= self._f_min:
            raise ValueError("Максимальная частота должна быть больше"
                            " минимальной частоты")

        self._f_max = float(value)
        self.define_freqs()


    @property
    def theta_min(self):
        """
        Возвращает минимальный азимут в градусах.

        Returns
        -------
        theta_min : float
            Минимальный азимут в градусах.

        """
        theta_min_deg = 180 * (self._theta_min / PI)

        return theta_min_deg


    @theta_min.setter
    def theta_min(self, value):
        """
        Устанавливает минимальный азимут в градусах.

        Parameters
        ----------
        value : float | int
            Минимальный азимут в градусах.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Минимальный азимут должен быть числом")

        if PI * (value % 360 / 180) > self._theta_max:
            raise ValueError("Минимальный азимут должен быть меньше"
                             " либо равен максимальному азимуту")

        self._theta_min = PI * (value % 360 / 180)
        self.define_thetas()


    @property
    def theta_max(self):
        """
        Возвращает максимальный азимут в градусах.

        Returns
        -------
        theta_max : float
            Максимальный азимут в градусах.

        """
        theta_max_deg = 180 * (self._theta_max / PI)

        return theta_max_deg


    @theta_max.setter
    def theta_max(self, value):
        """
        Устанавливает максимальный азимут в градусах.

        Parameters
        ----------
        value : float | int
            Максимальный азимут в градусах.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Максимальный азимут должен быть числом")

        if PI * (value % 360 / 180) < self._theta_min:
            raise ValueError("Максимальный азимут должен быть больше"
                             " либо равен минимальному азимуту")

        self._theta_max = PI * (value % 360 / 180)
        self.define_thetas()


    @property
    def theta_step(self):
        """
        Возвращает шаг по азимутам в градусах.

        Returns
        -------
        theta_step : float
            Шаг по азимутам в градусах.

        """
        theta_step_deg = 180 * (self._theta_step / PI)

        return theta_step_deg


    @theta_step.setter
    def theta_step(self, value):
        """
        Устанавливает шаг по азимутам в градусах.

        Parameters
        ----------
        value : float | int
            Шаг по азимутам в градусах.

        """
        if (not isinstance(value, float)) and (not isinstance(value, int)):
            raise ValueError("Шаг по азимутам должен быть числом")

        self._theta_step = PI * (value % 360 / 180)
        self.define_thetas()


    @property
    def nt(self):
        """
        Возвращает количество обрабатываемых отсчётов.

        Returns
        -------
        nt : int
            Количество обрабатываемых отсчётов.

        """
        return self._nt


    @nt.setter
    def nt(self, value):
        """
        Устанавливает количество обрабатываемых отсчётов.

        Parameters
        ----------
        value : int
            Количество обрабатываемых отсчётов.

        """
        if not isinstance(value, int):
            raise ValueError("Количество обрабатываемых отсчётов должно"
                             " быть целым числом")

        if value <= 0:
            raise ValueError("Количество обрабатываемых отсчётов должно"
                             " быть положительным числом")

        self._nt = value
        self.define_freqs()


    @property
    def velocities(self):
        """
        Возвращает набор фазовых скоростей.

        Returns
        -------
        velocities : ndarray[dtype: float64, dim = 1]
            Массив фазовых скоростей.

        """
        return self._velocities


    @velocities.setter
    def velocities(self, value):
        """
        Устанавливает набор фазовых скоростей в ручном режиме.

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

        self._velocities = value


    def define_velocities(self):
        """
        Устанавливает набор фазовых скоростей.

        Установка фазовых скоростей выполняется на основе
        заданых параметров v_max, v_min, v_step.
        """
        self._velocities = np.arange(self._v_min,
                                     self._v_max + self._v_step,
                                     self._v_step,
                                     dtype=np.float64)


    @property
    def thetas(self):
        """
        Возвращает набор азимутов.

        Returns
        -------
        thetas : ndarray[dtype: float64, dim = 1]
            Массив азимутов в градусах.

        """
        thetas_deg = 180 * (self._thetas / PI)
        return thetas_deg


    @thetas.setter
    def thetas(self, value):
        """
        Устанавливает набор азимутов в ручном режиме.

        Parameters
        ----------
        value : ndarray[dtype: float64 | int32, dim = 1]
            Массив азимутов в градусах.

        """
        if not isinstance(value, np.ndarray):
            raise ValueError("Подаваемый массив должен быть типа"
                             "numpy.ndarray")

        if len(value) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if (value.dtype != np.int32) and (value.dtype != np.float64):
            raise ValueError("Подаваемый массив должен состоять из типов"
                             "данных float64 или int32")

        self._thetas = PI * (value % 360 / 180)


    def define_thetas(self):
        """
        Устанавливает набор азимутов.

        Установка азимутов выполняется на основе
        заданых параметров theta_max, theta_min, theta_step.
        """
        self._thetas = np.arange(self._theta_min,
                                     self._theta_max,
                                     self._theta_step,
                                     dtype=np.float64)


    @property
    def freqs(self):
        """
        Возвращает набор частот.

        Returns
        -------
        thetas : ndarray[dtype: float64, dim = 1]
            Массив частот в Гц.

        """
        return self._freqs


    @freqs.setter
    def freqs(self, value):
        """
        Устанавливает набор частот в ручном режиме.

        Parameters
        ----------
        value : ndarray[dtype: float64 | int32, dim = 1]
            Массив частот в Гц.

        """
        if not isinstance(value, np.ndarray):
            raise ValueError("Подаваемый массив должен быть типа"
                             "numpy.ndarray")

        if len(value) == 0:
            raise ValueError("Подаваемый массив не должен быть пустым")

        if (value.dtype != np.int32) and (value.dtype != np.float64):
            raise ValueError("Подаваемый массив должен состоять из типов"
                             "данных float64 или int32")

        if any(value < 0):
            raise ValueError("Подаваемый массив должен состоять из "
                             "неотрицательных чисел")

        if any(value > 1 / self._dt / 2):
            raise ValueError("Подаваемый массив должен состоять из "
                             "частот меньших частоты Найквиста")

        self._freqs = value


    def define_freqs(self):
        """
        Устанавливает набор частот.

        Установка азимутов выполняется на основе
        заданых параметров f_max, f_min, dt, nt.

        """
        self._df = 1 / self._dt / self._nt
        self._freqs = np.arange(self._f_min,
                                self._f_max + self._df,
                                self._df,
                                dtype=np.float64)


    @property
    def energy(self):
        """
        Возвращает энергию для всех скоростей, частот, азимутов.

        Returns
        -------
        energy: ndarray[dtype: float64, dim = 3]
            Энергия для всех скоростей, частот, азимутов.
            [vel_axis, freq_axis, azi_axis]

        """
        return self._energy


    def compute_energy(self, data, recievers):
        """
        Вычисляет энергии для всех скоростей, частот, азимутов.

        Вычисление выполняется по скоростям: velocities
                                  частотам: freqs
                                  азимутам: thetas
        в окнах шириной nt. Трассы сейсмограммы через индексы связаны
        с координатами приёмников.

        Parameters
        ----------
        data : PassiveData
            Экземпляр класса PassiveData, который несёт в себе
            информацию о данных сейсмической записи.

        recievers : Recievers
            Экземпляр класса Recievers, который несёт в себе
            информацию о приёмниках.

        """
        seismogram = data.get_seismogram()
        data_length = data.nt
        data_num_rec = data.nt
        position_rec_x = recievers.x
        position_rec_y = recievers.y

        if data_num_rec != len(position_rec_x):
            raise ValueError("Количество трасс в сейсмограмме должно "
                             "быть равным количеству приёмников")

        energy = np.zeros((self._velocities.size,
                           self._freqs.size,
                           self._thetas.size))

        for window_i in range(int(data_length // self._nt)):
            seismogram_window = seismogram[window_i * self._nt: \
                                           (window_i + 1) * self._nt, :]
            energy += np.abs(compute_energy_(seismogram_window, self._freqs,
                                           self._velocities, self._thetas,
                                           position_rec_x, position_rec_y))

        self._energy = energy


    @property
    def vf(self):
        """
        Возвращает зависимость энергии от скоростей и частот.

        Суммирование энергии по всем азуимутам и возвращение зависимости
        энергии от скоростей и частот.

        Returns
        -------
        vf : ndarray[dtype: float64, dim = 2]
            Энергия для скоростей и частот.
            [vel_axis, freq_axis]

        """
        if len(self._energy.shape) == 0:
            raise ValueError("Энергия не была посчитана")

        self._en_vel_freq = np.sum(self._energy, axis=2)

        return self._en_vel_freq


    @property
    def ftheta(self):
        """
        Возвращает зависимость энергии от частот и азимутов.

        Суммирование энергии по всем скоростям и возвращение
        зависимости от частот и азимутов.

        Returns
        -------
        ftheta : ndarray[dtype: float64, dim = 2]
            Энергия для частот и азимутов.
            [freq_axis, azi_axis]

        """
        if len(self._energy.shape) == 0:
            raise ValueError("Энергия не была посчитана")

        self._en_f_theta = np.sum(self._energy, axis=0)

