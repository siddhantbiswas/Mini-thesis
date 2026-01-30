from pymatgen.io.vasp import Poscar
import os

parent_directory = os.getcwd()
dirs = [f"{x[0][2:]}" for x in os.walk(".")]

print(dirs)
for dir in dirs:
    poscar_path = os.path.join(dir, "POSCAR")

    if not os.path.exists(poscar_path):
        print(f"Skipping {dir}")
    else:
        print("working : ", dir)
        poscar = Poscar.from_file(f"{poscar_path}")
        structure = poscar.structure

        for x in range(-2,2):              # 80 to 110%
            for y in range(-2,2):
                for z in range(-2,2):
                    strain_array = [x/10.0, y/10.0, z/10.0]
                    strain_array_string = f"{x/10.0:.1f}_{y/10.0:.1f}_{z/10.0:.1f}"
                    original = structure.copy() 
                    strained_structure = original.apply_strain(strain_array)
                    os.chdir(f"{dir}")
                    os.mkdir(f"{dir}_{strain_array_string}")
                    os.chdir(f"{dir}_{strain_array_string}")
                    strained_structure.to(fmt = "poscar", filename = "POSCAR")
                    os.chdir(f"{parent_directory}")
