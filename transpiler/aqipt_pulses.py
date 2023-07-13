import numpy as np
import AQiPT.AQiPTcore as aqipt
from AQiPT.modules.control import AQiPTcontrol as control
from typing import Optional, Any
from math import pow


T_MAX = 10
ARGS = {'sampling':int(5e3), 'bitdepth':16, 'time_dyn': T_MAX}
PULSE_PARAMS = aqipt.general_params(ARGS)

class ShapedPulse():
    def __init__(self,
                t_o: Optional[float] = None, 
                t_start: Optional[float] = None,
                t_end: Optional[float]  = None,
                amp: Optional[float] = 1,
                width: Optional[int] = 0,
                tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
                name: Optional[str] = None, 
                color: Optional[str] = None, 
                area: Optional[float] = None,
            ):  
        
            self.t_o = t_o
            self.t_start = t_start
            self.t_end = t_end
            self.width = width
            self.tg = 2*self.width
            self.amp = amp
            self.tp_window = tp_window
            self.name = name
            self.color = color
            self.type = None
            self.area = area
            self.args = None
            self.function = None
    
    def info(self):
        return f'{self.type} ({self.name}) - Amp:{self.amp:0.5f}, Center: {self.t_o:0.2f}, Gate time: {self.tg:0.5f}'
            
class GaussianPulse(ShapedPulse):
    def __init__(self,
                t_o: Optional[float] = None, 
                t_start: Optional[float] = None,
                t_end: Optional[float]  = None,
                amp: Optional[int] = 1, 
                g_std: Optional[float] = np.pi/40,
                tp_window: Optional[int] = PULSE_PARAMS.dyn_time ,
                name: Optional[str] = None, 
                color: Optional[str] = None, 
                area: Optional[float] = None
        ):
        
        super().__init__(t_o, t_start, t_end, amp, 4*g_std, tp_window, name, color, area)
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
        if self.t_start != None and self.t_end !=  None: # Primer modo
            self.width = (self.t_end - self.t_start)/2
            self.t_o = self.t_start + self.width
            self.g_std = self.width/4
            self.area = self.g_std*pow(4*np.pi, 1/2)*np.abs(self.amp)
            
        elif self.area != None and self.t_start != None: # Segundo modo
            self.g_std = (self.area/(pow(4*np.pi, 1/2)*np.abs(self.amp)))
            self.width = self.g_std*4
            self.t_o = self.t_start + self.width
            self.t_end = self.t_start + 2*self.width
            self.tg = self.t_end - self.t_start
    
    
        
    
    def _function(self):
            
        args_list = {'g_Amp': self.amp,
                    'g_center': self.t_o,
                    'g_std': self.g_std,
                    'tp_window': self.tp_window,
                    'name': self.name,
                    'color': self.color,
                    'type': self.type}
        self.args = args_list
        tp = np.linspace(0, self.tp_window, int((self.tp_window - 0)*PULSE_PARAMS.sampling/PULSE_PARAMS.dyn_time));
        func = control.function(tp, args_list).gaussian()
        return func
            
class SquarePulse(ShapedPulse):
    def __init__(self,
        t_o: Optional[float] = None, 
        t_start: Optional[float] = None,
        t_end: Optional[float]  = None,
        amp: Optional[float] = 1,
        width: Optional[int] = 0,
        tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
        name: Optional[str] = None, 
        color: Optional[str] = None, 
        area: Optional[float] = None,
    ):  
        super().__init__(t_o,  t_start, t_end, amp, width, tp_window, name, color, area )
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
        #Times setting (t_start and t_end)
        
        # The area carries a factor of 1/2 over the calculations given the form of the Hamiltonian
        
        if self.t_start != None and self.t_end != None:
            self.width = (self.t_end - self.t_start)/2
            self.t_o = self.t_start + self.width
            self.tg = self.width * 2
            self.area = self.tg*np.abs(self.amp)
        
        # Area and starting setting
        elif self.area != None and self.t_start != None:
            self.width = 1/2*(self.area/(np.abs(self.amp)))
            self.t_o = self.t_start + self.width
            self.tg = self.area
            self.t_end = self.t_start + self.tg
            
    def _function(self):

        args_list = {'amp': self.amp,
                    't_o': self.t_o,
                    'width' : self.width,
                    'tp_window': self.tp_window,
                    'name': self.name,
                    'color': self.color,
                    'type': self.type}
        
        self.args = args_list
        tp = np.linspace(0, self.tp_window, int((self.tp_window-0)*PULSE_PARAMS.sampling/PULSE_PARAMS.dyn_time)); #time domain function
        func = control.function(tp, args_list).step()
        return func

# Constant Pulses
CERO_FUNCTION = SquarePulse(t_start = 0, t_end=0, amp=0)


