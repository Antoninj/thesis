import numpy as np
from scipy.integrate import cumtrapz
from features import CopFeatures
from scipy.signal import welch
from utils import load_config

config = load_config("process")


class FrequencyFeatures(CopFeatures):
    """ Class that implements the frequency domain features derived from the COP positions """

    # Constants
    fs = config["fs"]
    nperseg = config["nperseg"]

    def __init__(self, filepath):
        super(FrequencyFeatures, self).__init__(filepath)
        self.spectral_density = self.compute_rd_power_spectral_density()
        self.frequency_features = self.compute_frequency_features()

    def compute_power_spectral_density(self, array):
        (f, psd) = welch(array, fs=self.fs, nperseg=self.nperseg)

        return (f, psd)

    def compute_rd_power_spectral_density(self):
        (f, psd) = self.compute_power_spectral_density(self.cop_rd)

        return (f, psd)

    def compute_ml_power_spectral_density(self):
        (f, psd) = self.compute_power_spectral_density(self.cop_ml)

        return (f, psd)

    def compute_ap_power_spectral_density(self):
        (f, psd) = self.compute_power_spectral_density(self.cop_ap)

        return (f, psd)

    def compute_rd_total_power(self):
        (f, psd) = self.compute_rd_power_spectral_density()
        power = cumtrapz(psd, f)

        return power

    def compute_rd_f_peak(self):
        (f, psd) = self.compute_rd_power_spectral_density()
        p_max_index = psd.argmax()
        f_peak = f[p_max_index]

        return f_peak

    def compute_rd_power_frequency(self, threshold):
        power = self.compute_total_power()
        (f, psd) = self.compute_rd_power_spectral_density()
        f_power_index = np.where(power >= (threshold * power[-1]))
        f_power = f[f_power_index[0][0]]

        return f_power

    def compute_frequeny_features(self):
        """ Function to compute all the frequency features and store them in a dictionary """

        features = {}
        features["Rd Total power"] = self.compute_rd_total_power()

        return features

    def summary(self):
        """ Function to print out a summary of the hybrid features """

        for key, value in self.frequency_features.items():
            print("{}: {}".format(key, value))
