import gensound as gs
from gensound.transforms import ADSR
from gensound.filters import SimpleLPF
from gensound.curve import SineCurve

import time
import threading as th
import random

import src.globals as g




def hiloAudio():
    lastLight1 = 0
    lastLight2 = 0
    lastProx1 = 0
    lastProx2 = 0
    
    while True:
        duracion = random.randint(5,10)
        cambioLuz(duracion)
        time.sleep(duracion)

    

def cambioLuz(duracion=4e3):
    th.Thread(target=lanzarHiloLuz, daemon=True).start()

def cambioProx():
    th.Thread(target=lanzarHiloProx, daemon=True).start()

def noCambioLuz():
    pass 
    #th.Thread(target=lanzarHiloLuz, daemon=True).start()

def lanzarHiloLuz():
    val = int((g.lightVaina1[2]+g.lightVaina2[2])/2) + 40
    luzSynth(val, 6e3).play()
    time.sleep(5)

def lanzarHiloProx():
    val = int((g.proxVaina1+g.proxVaina2)/2)
    proxSynth(val, 0.01e3).play()
    time.sleep(2)


def luzSynth(frequency, duration):
    return gs.Sawtooth(frequency, duration)*ADSR(attack=2e3, decay=0.03e3, sustain=0.9, release=6e3)

def proxSynth(frequency, duration):
    s = gs.Sawtooth(frequency, duration)*ADSR(attack=0.02e3, decay=0.03e3, sustain=0.9, release=4e3)
    n = gs.WhiteNoise(1e3) * ADSR(attack=0.02e3, decay=0.03e3, sustain=0.8, release=1e3)
    out = 0.3*s + 0.1*n 
    return out



# def droneLoop(flag:bool):
#     MySignal(110, 4e3).play()
#     time.sleep(4.5)
#     flag = False

def crujiditos():
    c = 0.3 * gs.Square(12000,0.01e3)
    while True:
        c.play()
        time.sleep(random.random()*0.5) 


def camaCrujiditos():
    th.Thread(target=crujiditos, daemon=True).start()


# loopAactive = False
# loopBactive = False
# while True:
#     MySignal(60, 4e3).play()
#     time.sleep(4.5)

    

    # n = gs.WhiteNoise(1e3) * ADSR(attack=2e3, decay=0.03e3, sustain=0.8, release=2e3)
    # n.play()
    # time.sleep(2)

# while True:
#   detuned_array("D4", duration=5.0e3, width=40, amount=30)*ADSR(100,0,1.0,0).play() # many
#   time.sleep(2)



# ds = gs.Sine("D", duration=1e3)*ADSR(attack=0.002e3, decay=0.03e3, sustain=0.8, release=0.2e3)
# ds = gs.Sine("220.0", 1e3) #*ADSR(attack=2, decay=30, sustain=0.8, release=500)
# ds.play()
# Sine, Triangle, Square, Sawtooth with this feature.

# def detuned_array(pitch, duration, width, amount):
#   # amount = how many oscillators in the array
#   # width = the difference in cents between the highest and lowest oscillators in the array
#   all_cents = [i*width/amount - width/2 for i in range(amount)] # how much to detune each signal in the array
#   return gs.mix([ gs.Square(f"{pitch}{round(cents):+}", duration) for cents in all_cents ])

# def beep(pitch, duration:float, amp=0.5, mod=0.01, mod_freq=10.0):
#     fm = SineCurve(frequency=mod_freq, depth=mod, baseline=pitch, duration=duration)
#     signal = gs.Sine(fm, duration)*ADSR(attack=0.002e3, decay=0.03e3, sustain=0.8, release=0.2e3)
#     return signal