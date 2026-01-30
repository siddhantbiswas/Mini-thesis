import os
import numpy as np
from pymatgen.core import Structure
from pymatgen.io.vasp.inputs import Kpoints
import shutil

def write_KPOINTS(directories):
    print("directories : ", directories)
    skip = open("Removed_files", "w")
    bad_files = []
    for directory in directories:
        poscar_path = os.path.join(directory, "POSCAR")
        if not os.path.exists(poscar_path):
            print("No POSCAR")
            continue
        else:
                
            # Load the structure from the POSCAR file
            structure = Structure.from_file(poscar_path)

            try:
                # Define desired k-point densities along each reciprocal atom (in Å⁻¹)
                kppra = 1000
                #lengths = [30, 30, 30] # 1000KPPRA
                kpoints = Kpoints.automatic_density(structure, kppra)
                print("KPOINTS file generated using automatic_density =", kppra, "kppra")
                open(f"{directory}/KPOINTS", "w")

                # Write the KPOINTS file
                kpoints.write_file(f"{directory}/KPOINTS")

            except Exception as e:
                print(str(e))
                print(f"Bad file : {directory}")
                bad_files.append(directory)
                skip.write(f"{directory[2:]}\n")
                shutil.rmtree(directory)
                pass
               
                #density_kppra = 1000
                # Generate the KPOINTS object using automatic_density_by_lengths
                #kpoints = Kpoints.automatic_density(structure, density_kppra)
                #print("KPOINTS file generated using automatic_density =", density_kppra, "kppra")

            
    print(bad_files)

def main():
    #path = os.getcwd()
    #print("Parent : ", path)
    dirs = [f"{x[0]}" for x in os.walk(".")]
    #check = [f"{x}" for x in os.walk(path)]
    #print(dirs[1])

    write_KPOINTS(dirs)


if __name__ == "__main__":
    main()
