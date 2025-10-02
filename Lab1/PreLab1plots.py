import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, step, bode

# --- Common parameters ---
J = 5.9e-4
K_vp = 111.55
B = 0.006
K_vi = 3.0019e5
L = 0.0375
R = 6.5
K_t = 0.72
K_b = 0.4173
S_g = 0.887

# --- 1. Motor Dynamics ---
num1 = [K_t]
den1 = [J, B]
sys1 = TransferFunction(num1, den1)

# --- 2. I_in to I_m ---
num2 = [J*K_vp, B*K_vp + J*K_vi, B*K_vi]
den2 = [J*L, J*(R+K_vp)+B*L, J*K_vi + B*(R+K_vp) + K_t*K_b, B*K_vi]
sys2 = TransferFunction(num2, den2)

# --- 3. Full Transfer Function ---
num3 = [S_g*K_t*K_vp, S_g*K_t*K_vi]
den3 = den2
sys3 = TransferFunction(num3, den3)

systems = {"Motor Dynamics": sys1, "I_in to I_m": sys2, "Full Transfer Function": sys3}

# --- Step and Ramp Responses ---
t = np.linspace(0, 0.5, 2000)
w = np.logspace(-2, 5, 1000) 

for name, sys in systems.items():
    # Step response
    tout, yout = step(sys, T=t)
    plt.figure()
    plt.plot(tout, yout, label="Output")
    plt.plot(tout, np.ones_like(tout), 'k--', label="Step Input")
    plt.title(f"Step Response: {name}")
    plt.xlabel("Time [s]"); plt.ylabel("Amplitude")
    plt.legend(); plt.grid(True)

    # Ramp response (sys/s)
    ramp_den = np.polymul(sys.den, [1, 0])
    sys_ramp = TransferFunction(sys.num, ramp_den)
    tout, yout = step(sys_ramp, T=t)
    plt.figure()
    plt.plot(tout, yout, label="Output")
    plt.plot(tout, tout, 'k--', label="Ramp Input")
    plt.title(f"Ramp Response: {name}")
    plt.xlabel("Time [s]"); plt.ylabel("Amplitude")
    plt.legend(); plt.grid(True)

    # Bode plot
    w, mag, phase = bode(sys, w = w)
    plt.figure(figsize=(8,6))
    plt.subplot(2,1,1)
    plt.semilogx(w, mag); plt.ylabel("Magnitude [dB]"); plt.grid(True)
    plt.title(f"Bode Plot: {name}")
    plt.subplot(2,1,2)
    plt.semilogx(w, phase); plt.ylabel("Phase [deg]"); plt.xlabel("Frequency [rad/s]"); plt.grid(True)

    # Metrics
    dc_gain = np.polyval(sys.num, 0) / np.polyval(sys.den, 0)
    idx_bw = np.where(mag <= mag[0] - 3)[0]
    bw = w[idx_bw[0]] if len(idx_bw) > 0 else np.nan
    y_final = yout[-1]
    above_10 = np.where(yout >= 0.1*y_final)[0]
    above_90 = np.where(yout >= 0.9*y_final)[0]
    rise_time = tout[above_90[0]] - tout[above_10[0]] if len(above_10)>0 and len(above_90)>0 else np.nan

    print(f"--- {name} ---")
    print(f"DC Gain: {dc_gain:.4g}")
    print(f"Bandwidth: {bw:.4g} rad/s")
    print(f"Rise Time: {rise_time:.4g} s\n")

plt.show()
