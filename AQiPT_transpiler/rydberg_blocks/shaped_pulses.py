from typing import Optional
import numpy as np
from AQiPT.modules.control import AQiPTcontrol as control
from ..config.core import BackendConfig, default_backend


class ShapedPulse:
    r"""CLase que contiene los parametros de un pulso."""

    def __init__(
        self,
        t_o: Optional[float] = None,
        t_start: Optional[float] = None,
        t_end: Optional[float] = None,
        amp: float = 1,
        width: float = 0,
        name: Optional[str] = None,
        color: Optional[str] = None,
        area: Optional[float] = None,
        **kwargs,
    ):
        self.t_o = t_o
        self.t_start = t_start
        self.t_end = t_end
        self.width = width
        self.tg = 2.0 * self.width
        self.amp = amp
        self.name = name
        self.color = color
        self.type = None
        self.area = area
        self.args = None
        self.function = None

        if "backend" in kwargs:
            backend_config = kwargs["backend"]
            assert isinstance(backend_config, BackendConfig)

            self.backend_config = backend_config

        else:
            self.backend_config = default_backend

        simulation_config = self.backend_config.simulation_config
        t_max = simulation_config.time_simulation

        self.tp_window = t_max

    def info(self):
        """Imprime la información completa del pulso."""
        print(
            f"{self.type} ({self.name}) - Amp:{self.amp:0.5f}, Center: {self.t_o:0.2f}, Gate time: {self.tg:0.5f}"
        )


class GaussianPulse(ShapedPulse):
    r"""Pulse de forma Gaussiana."""

    def __init__(
        self,
        t_o: Optional[float] = None,
        t_start: Optional[float] = None,
        t_end: Optional[float] = None,
        amp: int = 1,
        g_std: float = np.pi / 40,
        name: Optional[str] = None,
        color: Optional[str] = None,
        area: Optional[float] = None,
        **kwargs,
    ):
        super().__init__(
            t_o, t_start, t_end, amp, 4 * g_std, name, color, area, **kwargs
        )
        self.type = "Gaussian Pulse"
        self.g_std = g_std

        self._set_parameters()
        self.function = self._function()

    def _set_parameters(self):
        """Genera los parametros del pulso.

        -- 1er modo: Se le da un tiempo inicial 't_start' y un tiempo final 't_end'.
            En este caso el ancho del pulso, el centro y el área ya están determinados.

        -- 2do modo: Se le da un área 'area' y un tiempo inicial 't_start'.
            En este caso se determina la desviación estandar y el ancho (que debe ser ajustado), luego
            se calcula el tiempo central del pulso y los demas parámetros.
        """
        if self.t_start is not None and self.t_end is not None:  # Primer modo
            self.width = (self.t_end - self.t_start) / 2
            self.t_o = self.t_start + self.width
            self.g_std = self.width / 4
            self.area = self.g_std * np.power(5 * np.pi, 1 / 2) * np.abs(self.amp)

        elif self.area is not None and self.t_start is not None:  # Segundo modo
            self.g_std = self.area / (np.power(5 * np.pi, 1 / 2) * np.abs(self.amp))
            self.width = self.g_std * 4
            self.t_o = self.t_start + self.width
            self.t_end = self.t_start + 2 * self.width
            self.tg = self.t_end - self.t_start

    def _function(self):
        args_list = {
            "g_Amp": self.amp,
            "g_center": self.t_o,
            "g_std": self.g_std,
            "tp_window": self.tp_window,
            "name": self.name,
            "color": self.color,
            "type": self.type,
        }
        self.args = args_list

        simulation_config = self.backend_config.simulation_config
        sampling = simulation_config.sampling
        t_max = simulation_config.time_simulation

        self.tp_window = t_max

        t_p = np.linspace(
            0, self.tp_window, int((self.tp_window - 0) * sampling / t_max)
        )
        func = control.function(t_p, args_list).gaussian()
        return func


class SquarePulse(ShapedPulse):
    r"""Pulso de forma cuadrada"""

    def __init__(
        self,
        t_o: Optional[float] = None,
        t_start: Optional[float] = None,
        t_end: Optional[float] = None,
        amp: float = 1,
        width: float = 0,
        name: Optional[str] = None,
        color: Optional[str] = None,
        area: Optional[float] = None,
        **kwargs,
    ):
        super().__init__(t_o, t_start, t_end, amp, width, name, color, area, **kwargs)
        self.type = "Square Pulse"

        self._set_parameters()
        self.function = self._function()

    def _set_parameters(self):
        """Genera los parametros del pulso.

        -- 1er modo: Se le da un tiempo inicial 't_start' y un tiempo final 't_end'.
            En este caso el ancho del pulso, el centro y el área ya están determinados.

        -- 2do modo: Se le da un área 'area' y un tiempo inicial 't_start'.
            En este caso se determina la desviación estandar y el ancho (que debe ser ajustado), luego
            se calcula el tiempo central del pulso y los demas parámetros.
        """
        # Times setting (t_start and t_end)

        # The area carries a factor of 1/2 over the calculations given the form of the Hamiltonian

        if self.t_start is not None and self.t_end is not None:
            self.width = (self.t_end - self.t_start) / 2
            self.t_o = self.t_start + self.width
            self.tg = self.width * 2
            self.area = self.tg * np.abs(self.amp)

        # Area and starting setting
        elif self.area is not None and self.t_start is not None:
            self.width = 1 / 2 * (self.area / (np.abs(self.amp)))
            self.t_o = self.t_start + self.width
            self.tg = self.width * 2
            self.t_end = self.t_start + self.tg

    def _function(self):
        args_list = {
            "amp": self.amp,
            "t_o": self.t_o,
            "width": self.width,
            "tp_window": self.tp_window,
            "name": self.name,
            "color": self.color,
            "type": self.type,
        }

        self.args = args_list
        simulation_config = self.backend_config.simulation_config
        sampling = simulation_config.sampling
        t_max = simulation_config.time_simulation

        self.tp_window = t_max

        t_p = np.linspace(
            0, self.tp_window, int((self.tp_window - 0) * sampling / t_max)
        )

        func = control.function(t_p, args_list).step()
        return func


# Constant Pulses
CERO_FUNCTION = SquarePulse(t_start=0, t_end=0, amp=0)
