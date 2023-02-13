# Computation config
quan_algo = "VQE"    ## (string)(VQE or adaptVQE)
excitations = "dq"    ## (string)(s d t q or etc)

iter_mode = True
optimizer_maxiter = 200
optimizer_tol = 0.00001

# grad_maxiter = 200
# grad_tol = 0.001

input_file_txt = 'result_Be8_HTDA_V0_800_FuLL.txt'

pcname = "Hpc_" #or "Hpc" or Ypc"


## Optimizer information
## MAybe include configuration of cobyla in the future (classical optimizer)

## Physical system config
num_particles = (2,2)
num_spatial_orbitals = 6
num_spin_orbitals = 12

########################## File names
# nucleus_name = "Be8" # must be a string type 
calc_destination = "/Result" #forward or backward slash also fine
corename = "Be8_"



import os
path_to_dir = os.getcwd()+calc_destination
os.chdir(path_to_dir)

i = 0
while os.path.exists(pcname+corename+"{:03d}.txt".format(i)):
    i += 1

output_filename = pcname+corename+"{:03d}.txt".format(i)
iter_mode_output_filename = pcname+corename+"{:03d}".format(i)  + "_" + "per_" + str(optimizer_maxiter)+"iter.txt"
circuitfilename = pcname+corename+"{:03d}".format(i)  + "_" + "opt_circuit.txt"













# # # Config only above # # #
#################################################################################################################
#################################################################################################################
#################################################################################################################


##### To use custom excitations list, use this function for excitations
# # Custom excitations
# # Mode of excitation (or terms of CCT)
# def custom_excitation_list(num_spatial_orbitals: int,num_particles):
# #### EDIT HERE
#     my_excitation_list = [((0, 1), (2, 3)), ((0, 1), (4, 5)), ((6, 7), (8, 9)), ((6, 7), (10, 11))]
#     return my_excitation_list
# excitations = custom_excitation_list

#REF https://www.geeksforgeeks.org/how-to-import-variables-from-another-file-in-python/



## ORIginal excitations function
# def custom_excitation_list(num_spatial_orbitals: int,
#                            num_particles: tuple[int, int]):
# #### EDIT HERE
#     my_excitation_list = [((0, 1), (2, 3)), ((0, 1), (4, 5)), ((6, 7), (8, 9)), ((6, 7), (10, 11))]
#     return my_excitation_list