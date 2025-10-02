clear;
% Import CSV data into a table, skipping the first 8 rows
data = readtable('C:\Users\kylea\Repos\MECH_467_Labs\Lab1\Data\part b\Scope Project.csv', 'HeaderLines', 8);

% Extract the second column and save it in a table called theta
theta = data(:, 3);
theta = theta{:, 1}(~isnan(theta{:, 1}));

% Apply a low pass filter
% Design a low pass filter
Ts = 0.5/1000;
fs = 1/Ts; % Sampling frequency (adjust as necessary)
fc = 100;   % Cut-off frequency (adjust as necessary)
Wn = fc/(fs/2);
[b, a] = butter(4, 2*100*Ts); % 4th order Butterworth filter

% Apply the filter to the second column data
theta_filtered = filtfilt(b, a, theta(:, 1));

deriv1 = deriv(theta_filtered, Ts);

deriv2 = deriv(deriv1, Ts);

figure;
plot(theta_filtered, 'b');   % first signal in blue
hold on;
plot(deriv1, 'r');             % second signal in red
hold on;
plot(deriv2, 'b');
legend('theta\_filtered','derivative');
xlabel('Sample index');
ylabel('Value');
title('Filtered signal and its derivative');
grid on;

%%
J = 5.9e-4;
K_vp = 111.55;
B = 0.006;
K_vi = 3.0019e5;
L = 0.0375;
R = 6.5;
K_t = 0.72;
K_b = 0.4173;
S_g = 0.887;
B_e = 0.00804;
mew_k = 0.3127;
J_e = 3.5e-4;

v_sig = data{:, 6};
v_sig = v_sig(~isnan(v_sig));

LHS = S_g*K_t*v_sig - B_e*deriv1 - 0.3127*sign(deriv1);
RHS = J* deriv2;

figure;
plot(LHS);
hold on;
plot(RHS);