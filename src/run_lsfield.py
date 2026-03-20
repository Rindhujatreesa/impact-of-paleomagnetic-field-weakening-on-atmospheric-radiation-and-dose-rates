# Create a python automation that runs the ./ls_field to obtain the field intensity values dynamically

import os
import subprocess
import pandas as pd


def run_lsfield( lat, lon, model=2, output_file = "temp_output", ls_directory = "data/LSMOD2/LSMOD2"):
    """
    The function has LSMOD.2 set as default model.
    The output columns Age, D, I, anf F will be saved to temp_output file
    """

    # Ensure absolute path
    ls_directory = os.path.abspath(ls_directory)

    # Full path to executable
    executable = os.path.join(ls_directory, "ls_field")

    # Remove old output file if exists
    output_path = os.path.join(ls_directory, output_file)
    if os.path.exists(output_path):
        os.remove(output_path)

    temp_input = f"{model}\n{output_file}\n{lat}\n{lon}"

    with open("temp_input.txt", "w") as file:
        file.write(temp_input)

    process = subprocess.run(
        [executable],
        input=temp_input,
        text=True,
        cwd=ls_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Check if program executed successfully
    if process.returncode != 0:
        print("STDOUT:\n", process.stdout)
        print("STDERR:\n", process.stderr)
        raise RuntimeError("LSfield execution failed.")
    
    # Check if output file was created
    if not os.path.exists(output_path):
        raise FileNotFoundError("Output file was not created.")
    
    # Read the output file
    df = pd.read_csv(
        output_path,
        sep = '\s+',
        skiprows=1
    )

    df.columns = ["Age_ka", "D_deg", "I_deg", "F_microT"]

    return df