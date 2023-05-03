import qutip as qt
import matplotlib.pyplot as plt
from AQiPT.modules.emulator import AQiPTemulator as emulator
from .aqipt_pulses import *
from typing import Any, List, Dict, Optional
from itertools import product

RED_HUE = ['firebrick','lightcoral','coral','chocolate']
BLUE_HUE = ['turquoise', 'paleturquoise','darkturquoise','skyblue']
PURPLE_HUE = ['slateblue', 'plum','violet','mediumorchid']

def merge_pulses(pulses :dict, name: str):
            coupling = {}
            done = []
            k = 0

            values = list(pulses.values())
            for i in range(len(values)):
                if i in done: continue
                v1 = values[i]

                for j in range(len(values)):
                    
                    if i == j: continue
                    
                    v2 = values[j]

                    # Matching the same levels of coupling
                    if v2[0] == v1[0]:
                        v1 = [v1[0], v1[1], np.add(v1[2], v2[2])]
                        values[i] = v1
                        done.append(j)

                coupling[name+str(k)] = v1
                done.append(i)
                k += 1

            return coupling


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
                        color = BLUE_HUE, phase=True, amp=True):
        
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
                    angl_pulse = np.angle(pulse)/2
                    
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
            else :
                for pulse, omega in p_pulses[key] :
                    factor = omega / (2*np.pi)
                    max_amp = np.max(np.abs(pulse))
                    
                    abs_pulse = np.abs(pulse)
                    angl_pulse = np.angle(pulse)/2
                    
                    # correction of the phase when pi 
                    angl_pulse[ angl_pulse == np.angle(np.exp(+1j*2*np.pi))/2] = np.pi
                    
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
            color = RED_HUE):

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
        color_coup = BLUE_HUE, 
        color_det= RED_HUE):

        self.plot_couplings(xmin, xmax, name=name, color=color_coup)
        self.plot_detunings(xmin,xmax, name=name, color=color_det)

class RydbergQubit():

    def __init__(self,
        nr_levels: int = 2,
        rydberg_states: Dict[str, Any] = {'RydbergStates': [1], 'l_values':[0, 1]}, 
        dissipators: Dict[str, Any] = {'Dissipator0': [[0,0], 0]},
        initial_state: Optional[int] = 0,
        name: Optional[str] = 'qubit',
        schedule: Optional[RydbergQubitSchedule] = None,
        complex = True
    ):
        self.nr_levels = nr_levels
        self.rydberg_states = rydberg_states
        self.dissipators = dissipators
        self.initial_state = initial_state
        self.name = name
        self.atomic_register = False
        self.schedule = schedule
        self.atom = None
        self.complex = complex

    def build(self):

        Nrlevels = self.nr_levels
        psi0 = self.initial_state

        times = self.schedule.times

        couplings_q = self.schedule.coupling_pulses
        detunings_q = self.schedule.detuning_pulses
        dissipators_q = self.dissipators
        rydbergstates_q = self.rydberg_states

        sim_params_q = {
                'couplings': couplings_q, 
                'detunings': detunings_q, 
                'dissipators': dissipators_q,
                'rydbergstates': rydbergstates_q}; #wrapping dynamic params in dictionary

        pulsed_qubit = emulator.atomicModel(times, Nrlevels, psi0, sim_params_q, name=self.name)
        pulsed_qubit.modelMap(plotON=False)

        pulsed_qubit.buildTHamiltonian()
        if not self.complex: pulsed_qubit.buildLindbladians()
        pulsed_qubit.buildObservables()

        pulsed_qubit.playSim(mode='control')

        self.atom = pulsed_qubit

    def __str__(self):
        print('{self.name}')
    
    def plot_results(self , color = PURPLE_HUE):
        simRes = self.atom.getResult()
        
        states = simRes.expect
        sl = len(states)

        fig, axis = plt.subplots(sl, figsize=(16, 2*sl))

        plt.setp(axis, yticks=[0, 0.5, 1])
        times = self.schedule.times
        for i in range(sl):
            state = states[i]
            
            axis[i].plot(times, state, color=color[i % 4])
            axis[i].set_ylabel(f'State {i}', fontsize=14)
            axis[i].set_ylim(0,1)
            axis[i].vlines(x = range(0,12,2), ymin = 0, ymax =1, color = 'silver', linestyle='dotted')
            axis[i].spines['top'].set_visible(False)
            axis[i].spines['right'].set_visible(False)
            if i != sl-1:
                axis[i].get_xaxis().set_visible(False)
                
                
            plt.yticks([0,0.5,1])

        fig.suptitle('Population evolution', fontsize=24)
        fig.supxlabel('Time', fontsize=18)
        plt.show()

class RydbergQuantumRegister():

    def __init__(self,
        qubits: List[RydbergQubit],
        layout,
        init_state: str = None,
        name: str = 'Quantum Register',
        connectivity: Optional[List[Any]] = ['All', []],
        c6: float = 0,
        c3: float = 0,
        times = PULSE_PARAMS.timebase()
    ):

        self.qubits = qubits
        self.layout = layout
        self.init_state = str(0).zfill(len(qubits)) if init_state == None else init_state
        self.name = name
        self.connectivity = connectivity
        self.c6 = c6
        self.c3 = c3
        self.times = times

        self.atomic_register = None
        self.schedule = {}
        
    def atoms(self):

        atoms = []
        for qubit in self.qubits:
            
            if qubit.atom == None:
                qubit.build()
            atom = qubit.atom

            atoms.append(atom)        
        
        return atoms

    def _build(self, nsteps=10000, rtol=1e-6, max_steps=10e-6):

        atomic_register = emulator.atomicQRegister(
            physicalRegisters= self.atoms(),
            initnState = self.init_state,
            name = self.name,
            connectivity= self.connectivity,
            layout = self.layout
        )

        atomic_register.buildTNHamiltonian()
        try:
            atomic_register.buildNLindbladians()
        except:
            pass
        atomic_register.buildNObservables()
        atomic_register.buildNinitState()
        

        atomic_register.simOpts = qt.Options(nsteps=nsteps, rtol=rtol, max_step=max_steps)
        atomic_register.registerMap(plotON=False)
        return atomic_register

    def compile(self, nsteps=10000, rtol=1e-6, max_steps=10e-6):
        atomic_register = self._build(nsteps=nsteps, rtol=rtol, max_steps=max_steps)
        atomic_register.compile()
        atomic_register.buildInteractions(c6=self.c6, c3=self.c3)
        atomic_register.playSim(mode='control')

        self.atomic_register = atomic_register

    def _schedule(self):
        couplings = []
        detunings = []

        for qubit in self.qubits:

            coupling = qubit.schedule.coupling_pulses
            detuning = qubit.schedule.detuning_pulses

            couplings.append(coupling)
            detunings.append(detuning)

        self.schedule['Couplings'] = couplings
        self.schedule['Detunings'] = detunings

    def plot_schedule(self, xmin=0, xmax=T_MAX, couplings=True, detunings=False, color_coup =BLUE_HUE, color_det=RED_HUE):

        if couplings:
            for i in range(len(self.qubits)):
                qubit = self.qubits[i]
                qubit.schedule.plot_couplings(xmin, xmax, name=f' {qubit.name}', color=color_coup)
                
                
        
        if detunings:
            for i in range(len(self.qubits)):
                qubit = self.qubits[i]
                qubit.schedule.plot_detunings(xmin, xmax, name=f' {qubit.name}', color=color_det)

    def plot_results(self , color = PURPLE_HUE):
        simRes = self.atomic_register.getResult()
        
        states = simRes.expect
        sl = len(states)

        levels = self.qubits[0].rydberg_states['l_values']
        perm_lev = list(product(levels, repeat=len(self.qubits)))


        fig, axis = plt.subplots(sl, figsize=(16, 1.7*sl))

        plt.setp(axis, yticks=[0, 0.5, 1])
        times = self.times
        for i in range(sl):
            state = states[i]
            
            axis[i].plot(times, state, color=color[i%4])
            axis[i].set_ylabel(f'State {perm_lev[i]}', fontsize=14)
            axis[i].set_ylim(0,1)
            axis[i].vlines(x = range(0,12,2), ymin = 0, ymax =1, color = 'silver', linestyle='dotted')
            axis[i].spines['top'].set_visible(False)
            axis[i].spines['right'].set_visible(False)
            if i != sl-1:
                axis[i].get_xaxis().set_visible(False)
                
                
            plt.yticks([0,0.5,1])

        fig.suptitle('Population evolution', fontsize=24)
        fig.supxlabel('Time', fontsize=18)
        plt.show()

