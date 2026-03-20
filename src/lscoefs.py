# Python wrapper that extracts the coefficients from LSMOD.2 using ./ls_coefs

import subprocess
import os
import numpy as np

LS_DIR = "data/LSMOD2/LSMOD2"

def get_coeffs_at_age(age, model_number = 2):
    
    """
    LScoefs expects:
    age
    model number (this is set to 2 by default (LSMOD.2 model))
    """

    output_file = "coefs.dat" # This file has four columns - SH_degree, SH_order, g(nT), and h(nT0)
    input_content = f"{age}\n{model_number}"
    
    subprocess.run(
        ["./ls_coefs"],
        input=input_content,
        text=True,
        cwd=LS_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Read coefficients
    coeffs = []
    with open(os.path.join(LS_DIR, output_file), "r") as f:
        next(f)
        for line in f:
            parts = line.split()

            # skip the first two columns (SH_degree and SH_order)
            g = float(parts[2])
            h = float(parts[3])
            coeffs.append(g)

            if int(parts[1]) != 0:
                coeffs.append(h)
    
    return np.array(coeffs)