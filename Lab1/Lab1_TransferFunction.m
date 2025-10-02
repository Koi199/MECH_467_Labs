clear;

k_t = 0.72;
J = 5.90*10^-4;
B = 0.006;

% Define the transfer function
num = [k_t]; % Numerator coefficients
den = [J B]; % Denominator coefficients
sys = tf(num, den);

% Step response
figure;
step(sys);
title('Step Response');
grid on;

% Frequency response
figure;
bode(sys);
title('Frequency Response');
grid on;

% DC Gain
dc_gain = dcgain(sys);
disp("DC Gain: " + num2str(dc_gain));

% Bandwidth
bw = bandwidth(sys);
disp("Bandwidth:" + num2str(bw));

% Rise Time
info = stepinfo(sys);
rise_t = info.RiseTime;
disp("Rise time: " + num2str(rise_t));


%% I_in to I_m
J = 5.9*10^-4;
K_vp = 111.55;
B = 0.006;
K_vi = 3.0019 * 10^5;
L = 0.0375;
R = 6.5;
K_t = 0.72;
K_b = 0.4173;

num = [J*K_vp, (B*K_vp + J*K_vi), B*K_vi];
den = [J*L, (J*(R+K_vp)+B*L), (J*K_vi + B*(R+K_vp) + K_t*K_b), B*K_vi];

sys = tf(num, den);

% Frequency response
figure;
bode(sys);
title('Frequency Response');
grid on;

% DC Gain
dc_gain = dcgain(sys);
disp("DC Gain: " + num2str(dc_gain));

% Bandwidth
bw = bandwidth(sys);
disp("Bandwidth:" + num2str(bw));

% Rise Time
info = stepinfo(sys);
rise_t = info.RiseTime;
disp("Rise time: " + num2str(rise_t));


%% Full transfer Function
J = 5.9*10^-4;
K_vp = 111.55;
B = 0.006;
K_vi = 3.0019 * 10^5;
L = 0.0375;
R = 6.5;
K_t = 0.72;
K_b = 0.4173;
S_g = 0.887;

num = [S_g*K_t*K_vp, S_g*K_t*K_vi];
den = [J*L, (J*(R+K_vp)+B*L), (J*K_vi + B*(R+K_vp) + K_t*K_b), B*K_vi];

sys = tf(num, den);

% Unit Step Response
figure;                 % open new figure window
step(sys);
title('Unit Step Response');
grid on;

% Unit Ramp Response
s = tf('s');
sysramp = sys/s;
figure;                 % open new figure window
step(sysramp);
title('Unit Ramp Response');
grid on;

% DC Gain
dc_gain = dcgain(sys);
disp("DC Gain: " + num2str(dc_gain));

% Bandwidth
bw = bandwidth(sys);
disp("Bandwidth:" + num2str(bw));

% Rise Time
info = stepinfo(sys);
rise_t = info.RiseTime;
disp("Rise time: " + num2str(rise_t));

