# This file computes the dipole moment using the coefficients obtained from src/lscoefs.py
# Also, calculates the latitude and longitude of the magnetic pole for a given coefficient set

import numpy as np

def compute_dipole_field(lat, lon, g, h):
    theta = np.radians(90 - lat)   # colatitude
    phi = np.radians(lon)

    g10 = g[(1,0)]
    g11 = g[(1,1)]
    h11 = h[(1,1)]

    Br = (-2 * g10 * np.cos(theta)
          -2 * g11 * np.sin(theta) * np.cos(phi)
          -2 * h11 * np.sin(theta) * np.sin(phi))

    Btheta = (-g10 * np.sin(theta)
              + g11 * np.cos(theta) * np.cos(phi)
              + h11 * np.cos(theta) * np.sin(phi))

    Bphi = (g11 * np.sin(phi) - h11 * np.cos(phi))

    B = np.sqrt(Br**2 + Btheta**2 + Bphi**2)

    return B


def get_magnetic_pole_latlon(coeff_vec):
    g10 = coeff_vec[0]
    g11 = coeff_vec[1]
    h11 = coeff_vec[2]

    m = np.array([g11, h11, g10])
    m = m / np.linalg.norm(m)

    lat = np.degrees(np.arcsin(m[2]))
    lon = np.degrees(np.arctan2(m[1], m[0]))

    return lat, lon, m