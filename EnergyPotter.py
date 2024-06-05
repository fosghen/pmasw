"""Класс для отображение энергии после обработки методом PMASW."""

import numpy as np
from matplotlib.ticker import FormatStrFormatter


class EnergyPlotter:
    """
    Класс для отображения энергии после обработки методом PMASW.

    Methods
    -------
    draw_seismogram(ax, data, dt, dx, scale=2, fontsize=18)
        Отображение сеймограмм.

    draw_vf2d(ax, spectrum, vel, freq, norm=True, fontsize=18)
        Отображение зависимости энергии от скорости и частоты.

    draw_f_theta(ax, f_theta, freq, thetas, norm=True, fontsize=18)
        Отображение зависимости энергии от частоты и азимута.

    """

    @staticmethod
    def draw_seismogram(ax, data, dt, dx, scale=2, fontsize=18):
        """
        Отображение сейсмограмм ислользуя matplotlib.

        Parameters
        ----------
        ax : matplotlib.axes._axes.Axes
            Объект Axes, на котором будут отображены сейсмограммы.

        data : ndarray[dtype: float64, dim = 2]
            Массив  сейсмограммы.
            [tempor_axis, spatial_axis]

        dt : float
            Время дескретизации сиганала (в секундах).

        dx : float | int
            Пространственная дескретизация сейсмограммы (в метрах).

        scale : optional | int | float, default = 2
            Коэффициент мастабируемости для трасс.

        fontsize : optional | int | float, default = 2
            Размер шрифта подписей осей и отметок осей.

        """
        nt, nx = data.shape
        receivers = np.arange(0, nx * dx, dx)
        for i in range(nx):
            trace_norm = scale * data[:, i] / np.max(data[:, i])
            tmp_offset = min(receivers) + dx * i
            x = trace_norm + tmp_offset
            time = np.arange(0, nt * dt, dt)[: len(x)]
            ax.plot(x, time, color='k')
        ax.set_ylim([nt * dt, 0])
        ax.set_xlim([min(receivers) - dx, max(receivers) + dx])
        ax.set_xlabel(r"$x$ (м)", fontsize=fontsize)
        ax.set_ylabel(r"$t$ (с)", fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))


    @staticmethod
    def draw_vf2d(ax, spectrum, vel, freq, norm=True, fontsize=18):
        """
        Отображение зависимости энергии от скорости и частоты.

        Parameters
        ----------
        ax : matplotlib.axes._axes.Axes
            Объект Axes, на котором будут отображены сейсмограммы.

        spectrum : ndarray[dtype: float64, dim = 2]
            Энергия для скоростей и частот.
            [vel_axis, freq_axis]

        vel : ndarray[dtype: float64 | int32, dim = 1]
            Массив фазовых скоростей.

        freq : ndarray[dtype: float64 | int32, dim = 1]
            Массив частот в Гц.

        norm : optional | bool, defaul = True
            Флаг нормализаии энергии вдоль оси частот.

        fontsize : optional | int | float, default = 2
            Размер шрифта подписей осей и отметок осей.

        """
        if norm:
            spectrum = spectrum / np.max(spectrum, axis=0)

        ax.imshow(spectrum,
                  aspect='auto',
                  extent=(freq.min(),
                          freq.max(),
                          vel.min(),
                          vel.max()
                          ),
                  cmap='RdYlBu_r',
                  origin='lower',
                  interpolation='gaussian')
        ax.set_xlabel(r"$f$ (Гц)", fontsize=fontsize)
        ax.set_ylabel(r"$V_R$ (м/с)", fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)


    @staticmethod
    def draw_f_theta(ax, f_theta, freq, thetas, norm=True, fontsize=18):
        """
        Отображение зависимости энергии от частоты и азимута.

        Parameters
        ----------
        ax : matplotlib.axes._axes.Axes
            Объект Axes, на котором будут отображены сейсмограммы.

        f_theta : ndarray[dtype: float64, dim = 2]
            Энергия для скоростей и частот.
            [vel_axis, freq_axis]

        freq : ndarray[dtype: float64 | int32, dim = 1]
            Массив частот в Гц.

        thetas : ndarray[dtype: float64 | int32, dim = 1]
            Массив азимутов в градусах.

        norm : optional | bool, defaul = True
            Флаг нормализаии энергии вдоль оси частот.

        fontsize : optional | int | float, default = 2
            Размер шрифта подписей осей и отметок осей.

        """
        if norm:
            f_theta = (f_theta.T / f_theta.T.max(axis=0)).T

        ax.imshow(f_theta,
                  aspect='auto',
                  extent=(thetas.min(),
                          thetas.max(),
                          freq.max(),
                          freq.min()
                          ),
                  cmap='RdYlBu_r',
                  interpolation='gaussian')

        ax.set_xlabel("Азимут, $^o$", fontsize=fontsize)
        ax.set_ylabel("Частота, Гц", fontsize=fontsize)
        ax.tick_params(axis='both', labelsize=fontsize)
        ax.invert_yaxis()

