
import matplotlib.pyplot as plt
from transpiler.rydberg_blocks.shaped_pulses import *
from typing import Any, List
from transpiler.utils.schedules_utils import *

from transpiler.config.core import backend

simulation_config = backend.simulation_config
T_MAX = simulation_config.time_simulation

pulse_config = backend.pulse_config
PULSE_PARAMS = backend.simulation_config.PULSE_PARAMS

coupling_color = pulse_config.DEFAULT_COLORS['coupling']
detuning_color = pulse_config.DEFAULT_COLORS['detuning']
other_color = pulse_config.DEFAULT_COLORS['other']
style = pulse_config.ploting_style

plt.style.use(style)




class RydbergQubitSchedule():
    def __init__(self,
        coupling_pulses: Any,
        detuning_pulses: Any, 
        times = PULSE_PARAMS.timebase()
    ):

        self.coupling_pulses = coupling_pulses
        self.detuning_pulses = detuning_pulses
        self.times = times
        
        self._merge_pulses()
        self.q_schedule = self

    def _merge_pulses(self):


        self.coupling_pulses = merge_pulses(self.coupling_pulses, 'Coupling')
        self.detuning_pulses = merge_pulses(self.detuning_pulses, 'Detuning')
        
    def add_function(self, funct: np.ndarray, where : str, type = "coupling"):
        
        if type == "coupling":
            schedule1 = self.coupling_pulses
        elif type == "detuning":
            schedule1 = self.detuning_pulses
        funct_1 = schedule1[where][2]
        
        funct_1 += funct
        
        schedule1[where][2] = funct_1
        
    def add_coupling(self, schedule2: dict, what : str, type = "coupling"):
        if type == "coupling":
            schedule1 = self.coupling_pulses
        elif type == "detuning":
            schedule1 = self.detuning_pulses
            
        val = schedule2[what]
        schedule1[what] = val    

    def plot_couplings(self, xmin: float = 0, xmax: float =T_MAX, plot:bool=True, name:str='', 
                        color = coupling_color, phase=True, amp=True):
        
        times = self.times
        p_pulses = {}
        
        

        for key in self.coupling_pulses.keys():
            pair = self.coupling_pulses[key][0]
            p_pulses[str(pair)] = []

        for key in self.coupling_pulses.keys():
            pair = self.coupling_pulses[key][0]
            pulse = self.coupling_pulses[key][-1]
            omega = self.coupling_pulses[key][1]
            p_pulses[str(pair)].append((pulse,omega))
    
        L = len(p_pulses.keys())
        fig, axis = plt.subplots(L, figsize=(16,2*L))

        for i in range(L):
            
            key = list(p_pulses.keys())[i]
        
            if L == 1:
                for pulse, omega in p_pulses[key] :
                    
                    factor = omega / (2*np.pi)
                    max_amp = np.max(np.abs(pulse))
                    
                    abs_pulse = np.abs(pulse)/max_amp
                    angl_pulse = -np.angle(pulse)
                    
                    if phase:
                        axis.plot(times, angl_pulse, color=color[i+1 % 4], label="$\phi (t)$")
                        axis.fill_between(times, angl_pulse, color=color[i+1 % 4], alpha=0.2)
                    if amp:
                        axis.plot(times, abs_pulse, color=color[i % 4], label="$\Omega (t)$")
                        axis.fill_between(times, abs_pulse, color=color[i % 4], alpha=0.3)

                    if factor != 1:
                        axis.text(.01, .99, f'$\Omega = 2\pi{factor:0.2f}$', ha='left', va='top', transform=axis.transAxes)

                axis.set_ylabel(f'{key}')
                axis.set_xlim(xmin, xmax)
                
                axis.legend()
            else :
                for pulse, omega in p_pulses[key] :
                    factor = omega / (2*np.pi)
                    max_amp = np.max(np.abs(pulse))
                    
                    abs_pulse = np.abs(pulse)
                    angl_pulse = -np.angle(pulse)
                    
                    if phase:
                        axis[i].plot(times, angl_pulse, color=color[1], label="$\phi (t)$")
                        axis[i].fill_between(times, angl_pulse, color=color[1], alpha=0.2)
                    if amp:
                        axis[i].plot(times, abs_pulse, color=color[0], label="$\Omega (t)$")
                        axis[i].fill_between(times, abs_pulse, color=color[0], alpha=0.3)

                    
                    axis[i].text(.01, .99, f'$\Omega = 2\pi{factor:0.2f}$', ha='left', va='top', transform=axis[i].transAxes)

                axis[i].set_ylabel(f'{key}')
                axis[i].set_xlim(xmin, xmax)
                axis[i].legend()
               
        fig.suptitle(f'Couplings {name}', fontsize=16)
        
        if not plot: return fig, axis

        plt.show()

    def plot_detunings(self, 
            xmin: float = 0, 
            xmax: float = T_MAX, 
            plot: bool = True,
            name: str = '',
            color = detuning_color):

            times = self.times
            p_pulses = {}

            for pulse in self.detuning_pulses.keys():
                pair = self.detuning_pulses[pulse][0]
                p_pulses[str(pair)] = []
            
            for key in self.detuning_pulses.keys():
                pair = self.detuning_pulses[key][0]
                pulse = self.detuning_pulses[key][-1]
                p_pulses[str(pair)].append(pulse)

            L = len(p_pulses.keys())
            fig, axis = plt.subplots(L, figsize=(16,2*L))

            for i in range(len(p_pulses.keys())):
                
                key = list(p_pulses.keys())[i]
            
                if len(p_pulses.keys()) == 1:
                    for pulse in p_pulses[key] :
                        axis.plot(times, pulse, color=color[0])
                        axis.fill_between(times, pulse, color=color[0], alpha=0.3)
                        axis.set_ylabel(f'{key}')
                        axis.set_xlim(xmin, xmax)
                else :
                    for pulse in p_pulses[key] :
                        axis[i].plot(times, pulse, color=color[i])
                        axis[i].fill_between(times, pulse, color=color[i], alpha=0.3)
                        axis[i].set_ylabel(f'{key}')
                        axis[i].set_xlim(xmin, xmax)

            fig.suptitle(f'Detunings {name}', fontsize=16)
            if not plot: return fig, axis

            plt.show()

    def plot_all(self, 
        xmin: float = 0, 
        xmax: float = T_MAX, 
        name='', 
        color_coup = coupling_color, 
        color_det= detuning_color):

        self.plot_couplings(xmin, xmax, name=name, color=color_coup)
        self.plot_detunings(xmin,xmax, name=name, color=color_det)

class RydbergRegisterSchedule():
    
    def __init__(
        self,
        schedules: List[RydbergQubitSchedule],
        times = PULSE_PARAMS.timebase()
    ):
        
        self.schedules = schedules
        self.times = times
        self.n_qubits = len(schedules)
        
    def plot_schedule(self, xmin=0, xmax=T_MAX, couplings=True, detunings=False, color_coup=coupling_color, color_det=detuning_color):

        
        for i in range(len(self.schedules)):
            schedule = self.schedules[i]
            
            if couplings:
                schedule.plot_couplings(xmin, xmax, name=f' {i}', color=color_coup)
                
            if detunings:
                schedule.plot_detunings(xmin, xmax, name=f' {i}', color=color_coup)
