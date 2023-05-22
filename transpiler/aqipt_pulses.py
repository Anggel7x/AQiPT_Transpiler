import numpy as np
import AQiPT.AQiPTcore as aqipt
from AQiPT.modules.control import AQiPTcontrol as control
from typing import Optional, Any
from math import pow


T_MAX = 10
ARGS = {'sampling':int(5e3), 'bitdepth':16, 'time_dyn': T_MAX}
PULSE_PARAMS = aqipt.general_params(ARGS)

class GaussianPulse():
    def __init__(self,
                t_o: Optional[float] = None, 
                t_start: Optional[float] = None,
                t_end: Optional[float]  = None,
                amp: Optional[int] = 1, 
                g_std: Optional[float] = np.pi/40,
                tp_window: Optional[int] = PULSE_PARAMS.dyn_time ,
                name: Optional[str] = None, 
                color: Optional[str] = None, 
                type: Optional[str] = None,
                area: Optional[float] = None
                
        ):
        self.t_o = t_o
        self.t_start = t_start
        self.t_end = t_end

        self.g_center = t_o
        self.g_Amp = amp
        self.g_std = g_std
        self.area = area

        self.tp_window = tp_window
        self.name = name
        self.color = color
        self.type = type
        
        self._set_parameters()
        self.function = self._function()
        self.width = self.t_end - self.t_start
    
    
    
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
            self.g_center = self.t_o
            self.g_std = self.width/4
            self.area = self.g_std*pow(4*np.pi, 1/2)*np.abs(self.g_Amp)
            
        elif self.area != None and self.t_start != None: # Segundo modo
            self.g_std = (self.area/(pow(4*np.pi, 1/2)*np.abs(self.g_Amp)))
            self.width = self.g_std*4
            self._std_adjustment()
            self.width = self.g_std*4
            self.t_o = self.t_start + self.width
            self.g_center = self.t_o
            self.t_end = self.t_start + 2*self.width
        
    def _function(self):
            
        args_list = {'g_Amp': self.g_Amp,
                    'g_center': self.g_center,
                    'g_std': self.g_std,
                    'tp_window': self.tp_window,
                    'name': self.name,
                    'color': self.color,
                    'type': self.type}

        tp = np.linspace(0, self.tp_window, int((self.tp_window - 0)*PULSE_PARAMS.sampling/PULSE_PARAMS.dyn_time));
        func = control.function(tp, args_list).gaussian()
        return func

    def info(self):
        return f'Gaussian Pulse ({self.name}) - Amp:{self.g_Amp:0.5f}, Center: {self.g_center:0.2f}, Std: {self.g_std:0.5f}'

    def _std_adjustment(self):

        while self.width < 0.06:
            self.g_std *= 3
            self.width = self.g_std*4
            #self.g_Amp /= 2
            
        while self.width > 1:
            self.g_std /= 3
            self.width = self.g_std*4
            #self.g_Amp *= 2
            
class SquarePulse():
    def __init__(self,
        t_o: Optional[float] = None, 
        t_start: Optional[float] = None,
        t_end: Optional[float]  = None,
        amp: Optional[float] = 1,
        width: Optional[int] = 0,
        tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
        name: Optional[str] = None, 
        color: Optional[str] = None, 
        type: Optional[str] = None,
        area: Optional[float] = None,
        omega: Optional[float] = None,
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
        self.type = type
        self.area = area
        self.omega = omega

       
        self._set_parameters()
        
        self.function = self._function()

        
    def _set_parameters(self):
        
        #Times setting (t_start and t_end)
        
        # The area carries a factor of 1/2 over the calculations given the form of the Hamiltonian
        
        if self.t_start != None and self.t_end != None:
            self.width = (self.t_end - self.t_start)/2
            self.t_o = self.t_start + self.width
            self.tg = self.width * 2
            self.area = self.tg*np.abs(self.amp)
        
        # Area and starting setting
        elif self.area != None and self.t_start != None:
            self.area = self.area
            self.width = 1/2*(self.area/(np.abs(self.amp)))
          #  self._width_adjustment()
            self.t_o = self.t_start + self.width
            self.tg = self.area
            self.t_end = self.t_start + self.tg
    
    def _width_adjustment(self):
        
        while self.width < 0.06:
            self.width *= 3
            #self.amp /= 2
            
        while self.width > 1:
            self.width /= 3
            #self.amp *= 2
            
        
    def _function(self):

        args_list = {'amp': self.amp,
                    't_o': self.t_o,
                    'width' : self.width,
                    'tp_window': self.tp_window,
                    'name': self.name,
                    'color': self.color,
                    'type': self.type}
        
        tp = np.linspace(0, self.tp_window, int((self.tp_window-0)*PULSE_PARAMS.sampling/PULSE_PARAMS.dyn_time)); #time domain function
        func = control.function(tp, args_list).step()
        return func

    def info(self):
        return f'Square Pulse ({self.name}) - Amp:{self.amp:0.5f}, Center: {self.t_o:0.2f}, Width: {self.width:0.5f}'


class CarrierPulse():

    def __init__(self,
        Amp: Optional[float] = 1,
        freq: Optional[float] = 20/(2*np.pi),
        phase: Optional[float] = 0,
        tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
        name: Optional[str] = None, 
        color: Optional[str] = None, 
        type: Optional[str] = None
    ):
        self.Amp = Amp
        self.freq = freq,
        self.phase = phase
        self.tp_window = tp_window
        self.name = name
        self.color = color
        self.type = type
        

    def function(self):

        args_list = {'Amp': self.Amp,
                    'freq': self.freq,
                    'phase' : self.phase,
                    'tp_window': self.tp_window,
                    'name': self.name,
                    'color': self.color,
                    'type': self.type}
        
        tp = np.linspace(0, self.tp_window, PULSE_PARAMS.sampling);
        func = control.function(tp, args_list).sinusoidal();
        return func

    def info(self):
        return f'Square Pulse ({self.name}) - Amp:{self.amp:0.5f}, Center: {self.t_o:0.2f}'
 
#Common Pulses

class X180GaussianPulse(GaussianPulse):
    def __init__(self,
                t_o: Optional[float] = None, 
                t_start: Optional[float] = None,
                amp: Optional[int] = 1, 
                g_std: Optional[float] = np.pi/40,
                tp_window: Optional[int] = PULSE_PARAMS.dyn_time ,
                name: Optional[str] = None, 
                color: Optional[str] = None, 
                type: Optional[str] = None,
                
                
        ):

        super().__init__(t_o = t_o,
            t_start=t_start,
            amp = amp,
            g_std = g_std,
            tp_window = tp_window,
            name = name,
            color = color,
            type = type,
            area = np.pi  #Constant Area 
            )

class X90GaussianPulse(GaussianPulse):
    def __init__(self,
                t_o: Optional[float] = None, 
                t_start: Optional[float] = None,
                amp: Optional[int] = 1, 
                g_std: Optional[float] = np.pi/40,
                tp_window: Optional[int] = PULSE_PARAMS.dyn_time ,
                name: Optional[str] = None, 
                color: Optional[str] = None, 
                type: Optional[str] = None,
            
        ):

        super().__init__(t_o = t_o,
            t_start=t_start,
            amp = amp,
            g_std = g_std,
            tp_window = tp_window,
            name = name,
            color = color,
            type = type,
            area = np.pi/2  #Constant Area
            )

class X360GaussianPulse(GaussianPulse):
    def __init__(self,
                t_o: Optional[float] = None, 
                t_start: Optional[float] = None,
                amp: Optional[int] = 1, 
                g_std: Optional[float] = np.pi/40,
                tp_window: Optional[int] = PULSE_PARAMS.dyn_time ,
                name: Optional[str] = None, 
                color: Optional[str] = None, 
                type: Optional[str] = None,     
        ):

        super().__init__(t_o = t_o,
            t_start=t_start,
            amp = amp,
            g_std = g_std,
            tp_window = tp_window,
            name = name,
            color = color,
            type = type,
            area = 2*np.pi  #Constant Area 
            )

class ConstantPulse(SquarePulse):
    def __init__(self,
        amp: Optional[float] = 1,
        tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
        name: Optional[str] = None, 
    ):  
        super().__init__(
            t_o = 1,
            t_start = None,
            amp = amp,
            tp_window = tp_window,
            name = name, 
            color  = None , 
            type = None,
            area = 10000
        ) 

class X180SquarePulse(SquarePulse):
    def __init__(self,
        t_o: Optional[float] = None, 
        t_start: Optional[float] = None,
        amp: Optional[float] = 1,
        tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
        name: Optional[str] = None, 
        color: Optional[str] = None, 
        type: Optional[str] = None,
    ):  

        super().__init__(
            t_o = t_o,
            t_start=t_start,
            amp =  amp,
            tp_window = tp_window,
            name = name, 
            color  = color , 
            type = type,
            area = np.pi
        ) 

class X90SquarePulse(SquarePulse):
    def __init__(self,
        t_o: Optional[float] = None, 
        t_start: Optional[float] = None,
        amp: Optional[float] = 1,
        tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
        name: Optional[str] = None, 
        color: Optional[str] = None, 
        type: Optional[str] = None,
    ):  

        super().__init__(
            t_o = t_o,
            t_start=t_start,
            amp =  amp,
            tp_window = tp_window,
            name = name, 
            color  = color , 
            type = type,
            area = np.pi/2
        ) 

class X360SquarePulse(SquarePulse):
    def __init__(self,
        t_o: Optional[float] = None, 
        t_start: Optional[float] = None,
        amp: Optional[float] = 1,
        tp_window: Optional[int] = PULSE_PARAMS.dyn_time,
        name: Optional[str] = None, 
        color: Optional[str] = None, 
        type: Optional[str] = None,
    ):  

        super().__init__(
            t_o = t_o,
            t_start=t_start,
            amp =  amp,
            tp_window = tp_window,
            name = name, 
            color  = color , 
            type = type,
            area = 2*np.pi
        ) 

# Constant Pulses
CERO_FUNCTION = SquarePulse(t_start = 0, t_end=0, amp=0)


