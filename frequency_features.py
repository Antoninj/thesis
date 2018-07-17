import numpy as np
from scipy.integrate import cumtrapz
from features import CopFeatures
from scipy.signal import welch
from utils import load_config

config = load_config()


class FrequencyFeatures(CopFeatures):
    """ Class that implements the frequency domain features derived from the COP positions """

    fs = config["frequency_features_parameters"]["sampling_frequency"]
    nperseg = config["frequency_features_parameters"]["nperseg"]

    def __init__(self, cop_x, cop_y):
        super(FrequencyFeatures, self).__init__(cop_x, cop_y)
        self.rd_spectral_density = self.compute_rd_power_spectral_density()
        self.ap_spectral_density = self.compute_ap_power_spectral_density()
        self.ml_spectral_density = self.compute_ml_power_spectral_density()
        self.frequency_features = self.compute_frequency_features()

    def compute_power_spectral_density(self, array):
        (f, psd) = welch(array, fs=self.fs, nperseg=self.nperseg)

        return (f, psd)

    def compute_rd_power_spectral_density(self):
        (f, psd) = self.compute_power_spectral_density(self.cop_rd)

        return (f, psd)

    def compute_ml_power_spectral_density(self):
        (f, psd) = self.compute_power_spectral_density(self.cop_x)

        return (f, psd)

    def compute_ap_power_spectral_density(self):
        (f, psd) = self.compute_power_spectral_density(self.cop_y)

        return (f, psd)

    def compute_rd_power_spectrum_area(self):
        (f, psd) = self.rd_spectral_density
        area = cumtrapz(psd, f)

        return area

    def compute_ml_power_spectrum_area(self):
        (f, psd) = self.ml_spectral_density
        area = cumtrapz(psd, f)

        return area

    def compute_ap_power_spectrum_area(self):
        (f, psd) = self.ap_spectral_density
        area = cumtrapz(psd, f)

        return area

    def compute_rd_total_power(self):
        area = self.compute_rd_power_spectrum_area()

        return area[-1]

    def compute_ml_total_power(self):
        area = self.compute_ml_power_spectrum_area()

        return area[-1]

    def compute_ap_total_power(self):
        area = self.compute_ap_power_spectrum_area()

        return area[-1]

    def compute_rd_f_peak(self):
        (f, psd) = self.rd_spectral_density
        p_max_index = psd.argmax()
        f_peak = f[p_max_index]

        return f_peak

    def compute_ml_f_peak(self):
        (f, psd) = self.ml_spectral_density
        p_max_index = psd.argmax()
        f_peak = f[p_max_index]

        return f_peak

    def compute_ap_f_peak(self):
        (f, psd) = self.ap_spectral_density
        p_max_index = psd.argmax()
        f_peak = f[p_max_index]

        return f_peak

    def compute_rd_power_frequency(self, threshold):
        power_spectrum_area = self.compute_rd_power_spectrum_area()
        (f, psd) = self.rd_spectral_density
        f_power_index = np.where(power_spectrum_area >= (threshold * power_spectrum_area[-1]))
        f_power = f[f_power_index[0][0]]

        return f_power

    def compute_ml_power_frequency(self, threshold):
        power_spectrum_area = self.compute_ml_power_spectrum_area()
        (f, psd) = self.ml_spectral_density
        f_power_index = np.where(power_spectrum_area >= (threshold * power_spectrum_area[-1]))
        f_power = f[f_power_index[0][0]]

        return f_power

    def compute_ap_power_frequency(self, threshold):
        power_spectrum_area = self.compute_ap_power_spectrum_area()
        (f, psd) = self.ap_spectral_density
        f_power_index = np.where(power_spectrum_area >= (threshold * power_spectrum_area[-1]))
        f_power = f[f_power_index[0][0]]

        return f_power

    def compute_frequency_features(self):
        """ Function to compute all the frequency features and store them in a dictionary """

        features = {}
        features["Rd Total power"] = self.compute_rd_total_power()
        features["ML Total power"] = self.compute_ml_total_power()
        features["AP Total power"] = self.compute_ap_total_power()
        features["Rd peak frequency"] = self.compute_rd_f_peak()
        features["ML peak frequency"] = self.compute_ml_f_peak()
        features["AP peak frequency"] = self.compute_ap_f_peak()
        features["50% Rd peak frequency"] = self.compute_rd_power_frequency(0.5)
        features["50% ML peak frequency"] = self.compute_ml_power_frequency(0.5)
        features["50% AP peak frequency"] = self.compute_ap_power_frequency(0.5)
        features["80% Rd peak frequency"] = self.compute_rd_power_frequency(0.8)
        features["80% ML peak frequency"] = self.compute_ml_power_frequency(0.8)
        features["80% AP peak frequency"] = self.compute_ap_power_frequency(0.8)

        return features

    def summary(self):
        """ Function to print out a summary of the frequency features """

        for key, value in self.frequency_features.items():
            print("{}: {}".format(key, value))
