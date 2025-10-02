import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, step

# --- System parameters ---
J = 5.9e-4
K_vp = 111.55
B = 0.006
K_vi = 3.0019e5
L = 0.0375
R = 6.5
K_t = 0.72
K_b = 0.4173
S_g = 0.887

# --- Transfer function numerator and denominator ---
num = [S_g*K_t*K_vp, S_g*K_t*K_vi]
den = [J*L,
       J*(R+K_vp) + B*L,
       J*K_vi + B*(R+K_vp) + K_t*K_b,
       B*K_vi]

# Create transfer function
sys = TransferFunction(num, den)

# Apply scaling
scale = B / (S_g*K_t)
sys_scaled = TransferFunction(np.array(sys.num)*scale, sys.den)

# --- Ramp response (divide by s → multiply denominator by [1, 0]) ---
ramp_den = np.polymul(sys_scaled.den, [1, 0])
sys_ramp = TransferFunction(sys_scaled.num, ramp_den)

# Time vector
t = np.linspace(0, 10, 1000)

# Step response of sys_ramp = ramp response of sys
t_out, y_out = step(sys_ramp, T=t)

# Ideal ramp input
ramp_input = t_out

# Error signal
error = ramp_input - y_out

# Steady-state error (average over last 10% of samples)
n = len(t_out)
last_10_percent = int(0.1 * n)
ss_error = np.mean(error[-last_10_percent:])

print(f"Estimated steady-state ramp error ≈ {ss_error:.4f}")

# --- Plot ---
plt.figure(figsize=(10,6))
plt.plot(t_out, ramp_input, 'k--', label='Ramp Input r(t)')
plt.plot(t_out, y_out, 'b', label='System Output y(t)')
plt.plot(t_out, error, 'r', label='Error e(t)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title(f'Ramp Response and Steady-State Error\nError ≈ {ss_error:.4f}')
plt.legend()
plt.grid(True)
plt.show()

