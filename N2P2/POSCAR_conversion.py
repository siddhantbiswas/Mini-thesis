import os
import numpy as np

def read_outcar(outcar_path):
    with open(outcar_path, 'r') as f:
        lines = f.readlines()

    # If OUTCAR contains ionic movement run (e.g. from an MD simulation) multiple
    # configurations may be present. Thus, need to prepare empty lists.
    lattices   = []
    energies   = []
    atom_lists = []

    # Loop over all lines.
    elements = []
    for i in range(len(lines)):
        line = lines[i]
        # Collect element type information, expecting VRHFIN lines like this:
        #
        # VRHFIN =Cu: d10 p1
        #
        if "VRHFIN" in line:
            elements.append(line.split()[1].replace("=", "").replace(":", ""))
        # VASP specifies how many atoms of each element are present, e.g.
        #
        # ions per type =              48  96
        #
        if "ions per type" in line:
            atoms_per_element = [int(it) for it in line.split()[4:]]
        # Simulation box may be specified multiple times, I guess this line
        # introduces the final lattice vectors.
        if "VOLUME and BASIS-vectors are now" in line:
            lattices.append([lines[i+j].split()[0:3] for j in range(5, 8)])
        # Total energy is found in the line with "energy  without" (2 spaces) in
        # the column with sigma->0:
        #
        # energy  without entropy=     -526.738461  energy(sigma->0) =     -526.738365
        #
        if "energy  without entropy" in line:
            energies.append(line.split()[6])
        # Atomic coordinates and forces are found in the lines following
        # "POSITION" and "TOTAL-FORCE".
        if "POSITION" in line and "TOTAL-FORCE" in line:
            atom_lists.append([])
            count = 0
            for ei in range(len(atoms_per_element)):
                for j in range(atoms_per_element[ei]):
                    atom_line = lines[i+2+count]
                    atom_lists[-1].append(atom_line.split()[0:6])
                    atom_lists[-1][-1].extend([elements[ei]])
                    count += 1

    # Sanity check: do all lists have the same length. 
    if not (len(lattices) == len(energies) and len(energies) == len(atom_lists)):
        raise RuntimeError("ERROR: Inconsistent OUTCAR file.")


    return lattices, energies, atom_lists


def write_input_data(directories, output_file):
    open(output_file, 'w')                      #clears output file
    with open(output_file, 'a') as out:
        for d in sorted(directories):
            outcar_path = os.path.join(d, "OUTCAR")

            if not os.path.exists(outcar_path):
                print(f"Skipping {d}:OUTCAR not found.")
                continue
        
            #lattices, energies, atom_lists = read_outcar()
            final_index = 0

            # Find final optimised structure    
            for i, (lattice, energy, atoms) in enumerate(zip(read_outcar(outcar_path)[0], read_outcar(outcar_path)[1], read_outcar(outcar_path)[2])):       #lattices, energies, atom_list
                final_index = i

            # Write configurations in "input.data" format. 
            for i, (lattice, energy, atoms) in enumerate(zip(read_outcar(outcar_path)[0], read_outcar(outcar_path)[1], read_outcar(outcar_path)[2])):       #lattices, energies, atom_list
                if i == final_index:
                    out.write("begin\n")
                    out.write("comment source_file_name={0:s} structure_number={1:d}\n".format(outcar_path, i + 1))
                    out.write("lattice {0:s} {1:s} {2:s}\n".format(lattice[0][0], lattice[0][1], lattice[0][2]))
                    out.write("lattice {0:s} {1:s} {2:s}\n".format(lattice[1][0], lattice[1][1], lattice[1][2]))
                    out.write("lattice {0:s} {1:s} {2:s}\n".format(lattice[2][0], lattice[2][1], lattice[2][2]))
                    for a in atoms:
                        out.write("atom {0:s} {1:s} {2:s} {3:s} {4:s} {5:s} {6:s} {7:s} {8:s}\n".format(a[0], a[1], a[2], a[6], "0.0", "0.0", a[3], a[4], a[5]))
                    out.write("energy {0:s}\n".format(energy))
                    out.write("charge {0:s}\n".format("0.0"))
                    out.write("end\n")
                else:
                    continue


def main():
    '''dirs = [f"{x:.2f}_{y:.2f}_{z:.2f}" 
            for x in np.arange(1.00, 1.51, 0.10)
            for y in np.arange(1.00, 1.51, 0.10)
            for z in np.arange(1.00, 1.51, 0.10)]'''
    dirs = [f"{x[0]}" for x in os.walk(".")]

    write_input_data(dirs, "input.data")


if __name__ == "__main__":
    main()