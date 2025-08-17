function project2_4fsk
% Plot theory and simulation curves for 4-FSK (coherent and non-coherent
% detection)

M = 4;
EsN0 = [0, 2, 4, 6, 8, 10, 12];
EbN0 = EsN0/log2(M);

EsN0_linear = 10.^(EsN0/10);

MFSK_coherent_theory = (M-1)*qfunc( sqrt(EsN0_linear) )*(M/2)/(M-1);

f = @(M, j) (-1).^j*nchoosek(M, j)*exp(EsN0_linear/j);
term_sum = sum(cell2mat(arrayfun(@(k) f(M, k), 2:M, 'un', 0)'));
MFSK_noncoherent_theory = (1/M)*exp(-EsN0_linear).*term_sum;

MFSK_coherent_exp_noise = 10.^([-0.69, -0.82, -1.03, -1.34, -1.77, -2.39, -3.3]);
MFSK_noncoherent_exp_noise = 10.^([-0.478, -0.574, -0.745, -1.01, -1.46, -2.2, -3.45]);

figure(1);
clf;
hold on;

plot(EbN0, MFSK_coherent_theory, 'Color', [1 1 0 0.5], 'LineWidth', 5);
plot(EbN0, MFSK_noncoherent_theory, 'Color', [1 1 0.5 0.5], 'LineWidth', 5);
plot(EbN0, MFSK_coherent_exp_noise, 'x-');
plot(EbN0, MFSK_noncoherent_exp_noise, 'x-');
legend('Theory - Coherent 4FSK', 'Theory - Non-coherent 4FSK', 'Simulation - Coherent 4FSK', 'Simulation - Non-coherent 4FSK');
xlabel('Eb/N0 [dB]');
ylabel('BER (P_B)');
yscale log;
grid on;
axis([0 6 1e-5 1]);
title('BER vs Eb/N0 curves for 4-FSK');

end