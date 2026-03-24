# Python wrapper that extracts the coefficients from LSMOD.2 using ./ls_coefs

import subprocess
import os
import numpy as np
import time


def get_coeffs_at_age(age, model_number = 2):
    
    """
    LScoefs expects:
    age
    model number (this is set to 2 by default (LSMOD.2 model))
    """
    # LS_DIR = "data/LSMOD2/LSMOD2"
    
    # Ensure relative paths work well
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LS_DIR = os.path.join(BASE_DIR, "..", "data", "LSMOD2", "LSMOD2")
    LS_DIR = os.path.abspath(LS_DIR)

    # Full path to executable
    executable = os.path.join(LS_DIR, "./ls_coefs")
    output_file = "coefs.dat" # This file has four columns - SH_degree, SH_order, g(nT), and h(nT0)
    input_content = f"{age}\n{model_number}\n"


    result = subprocess.run(
        [executable],
        input=input_content,
        text=True,
        cwd=LS_DIR,
        capture_output=True
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE
    )

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
        
    g_dict = {}
    h_dict = {}
    
    with open(os.path.join(LS_DIR, output_file), "r") as f:
        next(f)
        for line in f:
            parts = line.split()
            
            n = int(parts[0])
            m = int(parts[1])
            g = float(parts[2])
            h = float(parts[3])
            
            g_dict[(n, m)] = g
            h_dict[(n, m)] = h
    print(f"Running ls_coefs for age: {age}")

    return g_dict, h_dict

# if __name__ == "__main__":
#     import sys

#     age = float(sys.argv[1])

#     g, h = get_coeffs_at_age(age)

#     print("Done. Example coefficient:", list(g.items())[:5])