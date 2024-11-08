# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 08:50:46 2024

@author: DELL
"""

import numpy as np
import os
import re
import pandas as pd
from collections import defaultdict
from math import gcd
from functools import reduce

# Replace this with the full path to your file
file_path = r'C:\Users\DELL\Documents\train.data'  # Update with the actual path

with open(file_path, 'r') as file:
    content = file.read()
    print("File content successfully read.")

# Function to parse the crystal structures and group by lattice type
def parse_crystal_structures_by_lattice(file_path):
    blocks = re.split(r'\n(?=begin)', content.strip())
    lattice_groups = defaultdict(list)

    # Process each block
    for block in blocks:
        if 'begin' in block and 'end' in block:
            lines = block.splitlines()
            elements_count = defaultdict(int)
            lattice_type, lattice_vectors = extract_lattice_type_and_vectors(lines)
            
            for line in lines:
                if line.startswith('atom'):
                    parts = line.split()
                    if len(parts) > 5:
                        element = parts[4]  # Get the element symbol
                        elements_count[element] += 1
            
            if lattice_type:
                lattice_groups[lattice_type].append((block, elements_count, lattice_vectors))

    return lattice_groups

# Function to extract lattice type and lattice vectors from the block lines
def extract_lattice_type_and_vectors(lines):
    lattice_lines = [line for line in lines if line.startswith('lattice')]
    
    if len(lattice_lines) >= 3:
        # Extracting the lattice parameters
        try:
            a_vector = [float(x) for x in lattice_lines[0].split()[1:4]]
            b_vector = [float(x) for x in lattice_lines[1].split()[1:4]]
            c_vector = [float(x) for x in lattice_lines[2].split()[1:4]]
            
            lattice_type = classify_lattice(a_vector, b_vector, c_vector)
            return lattice_type, (a_vector, b_vector, c_vector)
        except (ValueError, IndexError):
            return None, None  # Handle cases where parsing fails
    return None, None

# Function to classify the lattice type based on parameters
def classify_lattice(a_vector, b_vector, c_vector):
    a = np.linalg.norm(a_vector)
    b = np.linalg.norm(b_vector)
    c = np.linalg.norm(c_vector)
    alpha = np.dot(a_vector, b_vector) / (a * b)
    beta = np.dot(b_vector, c_vector) / (b * c)
    gamma = np.dot(a_vector, c_vector) / (c * a)
    
    if a == b == c and alpha == beta == gamma == 0:
        return 'Cubic'
    elif a != b and b != c and alpha == beta == gamma == 0:
        return 'Orthorhombic'
    elif a == b and b != c:
        return 'Tetragonal'
    elif a != b != c and alpha != 0 and beta != 0 and gamma != 0:
        return 'Monoclinic'
    elif alpha == beta == gamma == np.cos(np.deg2rad(120)):
        return 'Hexagonal'
    else:
        return 'Other'  # Fallback case

# Parse the structures and group them by lattice type
lattice_groups = parse_crystal_structures_by_lattice(file_path)

# Display unique lattice types with their counts
print("\nUnique Lattice Types with Counts:")
for index, (lattice_type, structures) in enumerate(lattice_groups.items(), start=1):
    count = len(structures)  # Count of structures for each lattice type
    print(f"{index}: {lattice_type} (Count: {count})")

# Allow user to select a lattice type to save
selected_index = int(input("\nEnter the index of the lattice type you want to save: ")) - 1
selected_lattice_type = list(lattice_groups.keys())[selected_index]

# Prepare data for saving to CSV and POSCAR
csv_data = []
structures = lattice_groups[selected_lattice_type]

# Create a DataFrame for CSV
for structure, elements_count, lattice_vectors in structures:
    csv_data.append({'Lattice Type': selected_lattice_type, 'Structure': structure})

# Create a DataFrame for CSV
df = pd.DataFrame(csv_data)

# Specify the path where you want to save the CSV
csv_save_path = f'C:\\Users\\DELL\\Documents\\Selected_grouped_structures\\selected_lattice_{selected_lattice_type}.csv'

# Try saving to CSV and handle errors
try:
    df.to_csv(csv_save_path, index=False)
    print(f"Selected structures for lattice type '{selected_lattice_type}' saved to '{csv_save_path}'.")
except Exception as e:
    print(f"An error occurred while saving the CSV: {e}")

# Generate POSCAR file content
poscar_save_path = f'C:\\Users\\DELL\\Documents\\Selected_grouped_structures\\selected_lattice_{selected_lattice_type}.vasp'
try:
    with open(poscar_save_path, 'w') as poscar_file:
        for structure, elements_count, lattice_vectors in structures:
            # Prepare POSCAR content for each structure
            poscar_content = f"{selected_lattice_type} Structure\n1.0\n"
            # Add actual lattice vectors
            poscar_content += "  " + "  ".join(f"{v:.6f}" for v in lattice_vectors[0]) + "\n"
            poscar_content += "  " + "  ".join(f"{v:.6f}" for v in lattice_vectors[1]) + "\n"
            poscar_content += "  " + "  ".join(f"{v:.6f}" for v in lattice_vectors[2]) + "\n"

            # Element types
            element_types = " ".join(elements_count.keys())
            poscar_content += f"{element_types}\n"
            # Element counts
            element_counts = " ".join(str(count) for count in elements_count.values())
            poscar_content += f"{element_counts}\n"
            
            # Coordinate format
            poscar_content += "Direct\n"
            
            # Extract atomic coordinates (this is a placeholder; adjust as necessary)
            lines = structure.splitlines()
            for line in lines:
                if line.startswith('atom'):
                    parts = line.split()
                    if len(parts) > 5:
                        coords = parts[1:4]  # Get x, y, z coordinates
                        poscar_content += f"  {'  '.join(coords)}\n"

            # Write the POSCAR block to the file
            poscar_file.write(poscar_content)
            poscar_file.write("\n")  # Separate blocks with a newline
            
    print(f"POSCAR file for lattice type '{selected_lattice_type}' saved to '{poscar_save_path}'.")
except Exception as e:
    print(f"An error occurred while saving the POSCAR file: {e}")
