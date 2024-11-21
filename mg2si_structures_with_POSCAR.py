# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:19:14 2024

@author: DELL
"""

import os
from ase import Atoms
from ase.io import write

# Define the lattice parameters for Mg2Si (antifluorite structure)
a = 6.36  # Lattice constant in angstroms

# Define the directory to save the structures
output_directory = r"C:\\Users\\DELL\\Documents\\mg2si_structures"

# Create the directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Define the unit cell for Mg2Si
# Mg positions in fractional coordinates
mg_positions = [
    (0.0, 0.0, 0.0),
    (0.0, 0.5, 0.5),
    (0.5, 0.0, 0.5),
    (0.5, 0.5, 0.0),
    (0.5, 0.5, 0.5),
    (0.0, 0.0, 0.5),
    (0.0, 0.5, 0.0),
    (0.5, 0.0, 0.0)
]

# Si positions in fractional coordinates
si_positions = [
    (0.25, 0.25, 0.25),
    (0.75, 0.25, 0.25),
    (0.25, 0.75, 0.25),
    (0.25, 0.25, 0.75)
]

# Combine positions and symbols
positions = mg_positions + si_positions
symbols = ['Mg'] * len(mg_positions) + ['Si'] * len(si_positions)

# Unified POSCAR file path
poscar_path = os.path.join(output_directory, "unified_POSCAR")

# Open the unified POSCAR file in write mode
with open(poscar_path, "w") as poscar_file:

    # Loop over distortion factors for x, y, and z
    for fx in range(50, 160, 10):  # Factors from 0.5 to 1.5 in steps of 0.1
        for fy in range(50, 160, 10):
            for fz in range(50, 160, 10):
                fractional_modifier_x = fx / 100.0
                fractional_modifier_y = fy / 100.0
                fractional_modifier_z = fz / 100.0

                # Create the unit cell
                unit_cell = Atoms(
                    symbols=symbols,
                    scaled_positions=positions,
                    cell=[
                        (a * fractional_modifier_x, 0, 0),
                        (0, a * fractional_modifier_y, 0),
                        (0, 0, a * fractional_modifier_z)
                    ],
                    pbc=True
                )

                # Define the repetition of the unit cell
                repetition = (2, 2, 2)  # Repeat the unit cell 2x2x2 times

                # Create the supercell
                supercell = unit_cell * repetition

                # Save the supercell to the specified directory
                cif_filename = os.path.join(
                    output_directory,
                    f'mg2si_supercell_{fractional_modifier_x:.2f}_{fractional_modifier_y:.2f}_{fractional_modifier_z:.2f}.cif'
                )
                supercell.write(cif_filename)

                # Append the supercell to the unified POSCAR file
                poscar_file.write(f"# POSCAR for scaling factors: x={fractional_modifier_x:.2f}, y={fractional_modifier_y:.2f}, z={fractional_modifier_z:.2f}\n")
                write(poscar_file, supercell, format="vasp")

                # Print status
                print(f"Saved CIF: {cif_filename}")
                print(f"Appended to POSCAR: Scaling factors x={fractional_modifier_x:.2f}, y={fractional_modifier_y:.2f}, z={fractional_modifier_z:.2f}")
