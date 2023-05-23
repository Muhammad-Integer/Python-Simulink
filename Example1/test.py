from rtwtypes import *

## dllModel.h in Python: using ctypes.Structure to re-create all of dllModel.h structure
class B_dllModel_T(ctypes.Structure):
    """Simulink.Parameter SimulinkGlobals"""

    _fields_ = [
        ("SimulationSignal1", real_T),
        ("SignalOut3", real32_T),
        ("SignalOut2", uint16_T),
    ]


class ExtU_dllModel_T(ctypes.Structure):
    """SimulinkGlobal Inputs to Model"""

    _fields_ = [("SignalIin2", uint16_T)]


class ExtY_dllModel_T(ctypes.Structure):
    """SimulinkGlobal Outputs from Model"""

    _fields_ = [("OutputPort2", real32_T)]


class P_dllModel_T(ctypes.Structure):
    """SimulinkGlobal Parameters"""

    _fields_ = [("K2", uint16_T)]


class Timing(ctypes.Structure):
    """Timing Structure"""

    _fields_ = [
        ("clockTick0", uint32_T),
        ("clockTickH0", uint32_T),
    ]


class tag_RTM_dllModel_T(ctypes.Structure):
    """ tag RTM """

    _fields_ = [
        ("errorStatus", ctypes.c_char_p),
        ("Timing", Timing),
    ]

import os

dll_path = os.path.abspath("Example1\dllModel_win64.dll")
dll = ctypes.windll.LoadLibrary(dll_path)

# Block paramters (default storage)
dllModel_P = P_dllModel_T.in_dll(dll, "dllModel_P")
# Block signals (default storage)
dllModel_B = B_dllModel_T.in_dll(dll, "dllModel_B")
# External inputs (root inport signals with default storage)
dllModel_U = ExtU_dllModel_T.in_dll(dll, "dllModel_U")
# External outputs (root outports fed by signals with default storage)
dllModel_Y = ExtY_dllModel_T.in_dll(dll, "dllModel_Y")

"""
 * Exported Global Signals
 *
 * Note: Exported global signals are block signals with an exported global
 * storage class designation.  Code generation will declare the memory for
 * these signals and export their symbols.
 """
SignalIn = real32_T.in_dll(dll, "SignalIn")
SimulationSignal2 = real_T.in_dll(dll, "SimulationSignal2")
SignalOut = real32_T.in_dll(dll, "SignalOut")
"""
 * Exported Global Parameters
 *
 * Note: Exported global parameters are tunable parameters with an exported
 * global storage class designation.  Code generation will declare the memory for
 * these parameters and exports their symbols.
"""
K = real32_T.in_dll(dll, "K")

# Model entry point functions
dllModel_initialize = dll.dllModel_initialize
dllModel_step = dll.dllModel_step
dllModel_terminate = dll.dllModel_terminate

# Real-time Model object
dllModel_M = ctypes.POINTER(tag_RTM_dllModel_T).in_dll(dll, "dllModel_M")



## Running Model
dllModel_initialize();

print(dllModel_step())

print([dllModel_B.SimulationSignal1, SimulationSignal2])

print([dllModel_P.K2])

dllModel_step()

print([dllModel_B.SimulationSignal1, SimulationSignal2])

dllModel_step()

## Manipulating Signals
#SignalIn.value = float(2)
#print(SignalOut)

#dllModel_step()
#print(SignalOut)

#print([dllModel_B.SignalOut2, dllModel_B.SignalOut3, SignalOut])

#dllModel_U.SignalIin2 = 1

#dllModel_step()
#print([dllModel_B.SignalOut2, dllModel_B.SignalOut3, SignalOut])

#print(dllModel_M.contents.Timing.clockTick0)

#step = dllModel_step()
#assert dllModel_M.contents.Timing.clockTick0 == step
