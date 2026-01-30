#!/usr/bin/zsh
#SBATCH --job-name=VASP
#SBATCH --mail-type=ALL
#SBATCH --mail-user=ulumuddin@imm.rwth-aachen.de
#SBATCH --cpus-per-task=1
#SBATCH --time=0-05:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --mem=128G
#SBATCH --output=output.log # Store standard output for debugging
#SBATCH --error=error.log  # Store errors for debugging
#SBATCH --account=p0020330

ulimit -c unlimited
export MPICH_COREDUMP=1


# Load required modules
module purge
module load intel-compilers/2022.1.0
module load impi/2021.6.0
module load iccifort/2019.5.281
module load imkl/2019.5.281
module load GCC/11.3.0
module load OpenMPI/4.1.4
module load Eigen
module load FFTW/3.3.10
module load GSL/2.7
module load libfabric/1.15.1

# Bypass missing libefa
export OMPI_MCA_btl="^ofi"        # For OpenMPI
export I_MPI_FABRICS="shm:tcp"   # For Intel MPI


# Update PATH and LD_LIBRARY_PATH
export PATH="/home/rz120074/github/dotfiles/scripts/binp/:/home/rz120074/github/dotfiles/dotfiles/bins:/home/rz120074/github/n2p2/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/sources/n2p2/lib:$HOME/Github/dotfiles/bins:/lib64:/usr/lib64:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH=$(dirname $(gcc -print-file-name=libstdc++.so.6)):$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/home/rz120074/miniconda3/lib:$LD_LIBRARY_PATH

# Run the job
#srun nnp-train
mpirun -np 10 nnp-train

