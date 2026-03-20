# This file computes the dipole moment using the coefficients obtained from src/lscoefs.py
# Also, calculates the latitude and longitude of the magnetic pole for a given coefficient set

import numpy as np

def compute_dipole_moment(coeff_vec):
    g10 = coeff_vec[0]
    g11 = coeff_vec[1]
    h11 = coeff_vec[2]
    
    return np.sqrt(g10**2 + g11**2 + h11**2)


def get_magnetic_pole_latlon(coeff_vec):
    g10 = coeff_vec[0]
    g11 = coeff_vec[1]
    h11 = coeff_vec[2]

    m = np.array([g11, h11, g10])
    m = m / np.linalg.norm(m)

    lat = np.degrees(np.arcsin(m[2]))
    lon = np.degrees(np.arctan2(m[1], m[0]))

    return lat, lon, m