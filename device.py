import numpy as np
import time
import subprocess
import os
import time
import matplotlib.pyplot as plt 

class RRAM_:
    conductance = 0                     # Conductance of the selected element of matrix

    def __init__(
        self,
        maxConductance,
        minConductance,
        AM_or_QM,
        error_range_AM,
        num_Bit,
        sigma_QW
    ):
        self.maxConductance = maxConductance                # Maximum cell conductance (S)
        self.minConductance = minConductance                # Minimum cell conductance (S)
        self.AM_or_QM = AM_or_QM                            # Analog model or quantized model
        self.error_range_AM = error_range_AM                # error range in analog model
        self.num_Bit = num_Bit                              # number of bits in quantized model
        self.num_level = 2 ** num_Bit                       # number of levels in quantized model
        self.sigma_QW = sigma_QW                            # sigma of device variation in quantized model
        self.local_gen = np.random.default_rng()

    def Write(
        self,
        matrix_value,
        max_value,
        min_value
    ):
        # normalized_value = (matrix_value - min_value) / (max_value - min_value) 
        normalized_value = matrix_value / max_value

        if self.AM_or_QM:
            # self.conductance = (normalized_value - 0) * (self.maxConductance - self.minConductance) / (1 - 0) + self.minConductance
            # self.conductance = normalized_value * (self.maxConductance - self.minConductance) + self.minConductance
            self.conductance = normalized_value * self.maxConductance
            if self.conductance < self.minConductance:
                self.conductance = self.minConductance
            self.conductance = self.local_gen.normal(self.conductance, self.error_range_AM)
        else:
            conductance_interval = (self.maxConductance - self.minConductance) / (self.num_level - 1)
            quantized_index = int(round(normalized_value * (self.num_level - 1)))
            self.conductance = self.minConductance + quantized_index * conductance_interval
            self.conductance = self.local_gen.normal(self.conductance, self.sigma_QW)

        # Ensure the conductance is within the valid range 
        if self.conductance > self.maxConductance:
            self.conductance = self.maxConductance
        elif self.conductance < self.minConductance:
            self.conductance = self.minConductance

        return self.conductance
    