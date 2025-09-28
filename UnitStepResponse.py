import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction, step

# --- Parameters ---
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

# Time vector for simulation
t = np.linspace(0, 0.5, 1000)

# Step response
t_out, y_out = step(sys, T=t)

# Plot
plt.figure(figsize=(8,4))
plt.plot(t_out, y_out, linewidth=2)
plt.title('Unit Step Response')
plt.xlabel('Time [s]')
plt.ylabel('Response')
plt.grid(True)
plt.show()
