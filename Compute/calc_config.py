## Source File input
input_txt = 'result_Be8-copy.txt'

## Computation config
pcname = "Hpc" #or "Hpc" or Ypc"
quan_algo = "VQE"    ## (string)(VQE or adaptVQE)
excitations = "dq"    ## (string)(s d t q or etc)

iter_mode = True
optimizer_maxiter = 200
optimizer_tol = 0.00001

# grad_maxiter = 200
# grad_tol = 0.001






## Optimizer information
## MAybe include configuration of cobyla in the future (classical optimizer)

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