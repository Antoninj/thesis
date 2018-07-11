from time_features import DistanceFeatures, AreaFeatures, HybridFeatures
from frequency_features import FrequencyFeatures
from utils import load_config
import argparse
from matplotlib import pyplot as plt

if __name__ == "__main__":

    # Load configuration file
    config = load_config("test")

    # WBB data test file
    wbb_cop_data = config["wbb cop data test file"]

    # Command line argument parser to choose between frequency or time domain features
    parser = argparse.ArgumentParser(
        description="")
    parser.add_argument("-f", "--freq", action='store_true', help="Compute frequency features")
    parser.add_argument("-p", "--plot", action='store_true', help="Plot data")

    args = parser.parse_args()
    freq = args.freq
    plot = args.plot

    if not freq:

        # Time features tests
        distance_features = DistanceFeatures(wbb_cop_data)
        distance_features.summary()

        area_features = AreaFeatures(wbb_cop_data)
        area_features.summary()

        hybrid_features = HybridFeatures(wbb_cop_data)
        hybrid_features.summary()

    else:

        # Frequency features tests
        freq_features = FrequencyFeatures(wbb_cop_data)

        (f, pxx) = freq_features.compute_rd_power_spectral_density()
        f_peak = freq_features.compute_rd_f_peak()
        power = freq_features.compute_rd_total_power()
        f_80 = freq_features.compute_rd_power_frequency(threshold=0.8)

        print(f_80)

        if plot:
            plt.semilogy(f, pxx)
            plt.xlabel('frequency [Hz]')
            plt.ylabel('PSD [mm**2/Hz]')
            plt.show()
