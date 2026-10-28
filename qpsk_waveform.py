import numpy as np
import matplotlib.pyplot as plt
#QPSK Modulation(greymapping)
def qpsk_mod(bits):
    """
    00 →  +1 + j1
    01 →  -1 + j1
    11 →  -1 - j1
    10 →  +1 - j1
    """
    bits = np.array(bits)
    bits_reshaped = bits.reshape(-1, 2)
    symbols = []

    for b1, b2 in bits_reshaped:
        if b1 == 0 and b2 == 0:
            symbols.append(1 + 1j)
        elif b1 == 0 and b2 == 1:
            symbols.append(-1 + 1j)
        elif b1 == 1 and b2 == 1:
            symbols.append(-1 - 1j)
        else:  # 10
            symbols.append(1 - 1j)

    return np.array(symbols)
# AWGN Channel
def add_awgn(s, EbN0_dB):
    EbN0 = 10 ** (EbN0_dB / 10)
    Eb = 1
    N0 = Eb / EbN0
    sigma2 = N0 / 2
    noise = np.sqrt(sigma2) * (np.random.randn(len(s)) + 1j * np.random.randn(len(s)))
    return s + noise
if __name__ == "__main__":
# mission 1.1 — 10-bit QPSK waveform
    print("\n Mission 1.1")
    # generatiing 10 random bits
    bits = np.random.randint(0, 2, 10)
    print("Bits:", bits)
    # QPSK symbols (baseband)
    s_base = qpsk_mod(bits)
    print("Baseband symbols:", s_base)
    # Passband parameters
    Ts = 1e-3
    fc = 3000
    Fs = 1e6
    Ns = int(Ts * Fs)
    t_wave = []
    x_wave = []
    for i, sym in enumerate(s_base):
        phi = np.angle(sym)
        A = 1
        t_local = np.arange(Ns) / Fs + i * Ts
        x_local = A * np.cos(2*np.pi*fc*t_local + phi)
        t_wave.append(t_local)
        x_wave.append(x_local)

    t_wave = np.concatenate(t_wave)
    x_wave = np.concatenate(x_wave)

    plt.figure(figsize=(12,4))
    plt.plot(t_wave, x_wave)
    plt.title("QPSK Passband Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

    # mission 1.2 — QPSK constellation under AWGN

    print("\n=== Mission 1.2 ===")

    # generating 1 million random bits
    Nbits = 1_000_000
    bits_long = np.random.randint(0, 2, Nbits)

    # ensuring that it has an even length
    if len(bits_long) % 2 != 0:
        bits_long = np.append(bits_long, 0)

    symbols = qpsk_mod(bits_long)

    EbN0_list = [0, 10, 20, 100]

    for snr in EbN0_list:
        r = add_awgn(symbols, snr)
        plt.figure(figsize=(5, 5))
        plt.scatter(r.real[:500000], r.imag[:500000], s=1)
        plt.title(f"QPSK Constellation at Eb/N0 = {snr} dB")
        plt.xlabel("In-Phase")
        plt.ylabel("Quadrature")
        plt.grid(True)
        plt.axis("equal")
        plt.show()

    print("\nMission 1 complete!")
