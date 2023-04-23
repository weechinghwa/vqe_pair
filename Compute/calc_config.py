## Source File input ##
input_dir = "203_Be8"

### The following doesnt require setting up, unless file naming is different
obs_onebody_csv = "../Data/"+input_dir+"/"+input_dir+"-1B_H_input.csv"
obs_twobody_csv = "../Data/"+input_dir+"/"+input_dir+"-2B_H_input.csv"
parameter_py = "../Data/"+input_dir+"/"+"parameter.txt"



## Computation config ## 
pcname = "Hpc" #or "Hlp" or Ypc"
quan_algo = "VQE"    ## (string)(VQE or adaptVQE)

iter_mode = False ## (Boolean) # True for iteratively repeating new VQE calulation until optimizer_tol is reached
optimizer_maxiter = 300
optimizer_tol = 0.00001
include_onebody = True
include_twobody = True
two_factor = 0.5



## import computational data (observalbles and parameters)
parameter_txt=[]
with open (parameter_py, 'rt') as myfile:    #filename
    for line in myfile:
        line = line.rstrip('\n')
        parameter_txt.append(line)
parameter = parameter_txt[1].split(",,,")
import ast
num_orbitals = ast.literal_eval(parameter[0])
num_spin_orbitals = int(parameter[1])
num_particles = ast.literal_eval(parameter[2])
num_spatial_orbitals = int(num_spin_orbitals/2)
# print(num_orbitals,num_spin_orbitals,num_particles,num_spatial_orbitals) # to test if the data is correct (not important in production)



## Setup custom excitation list ##
from itertools import combinations
def HFground_pair_list(num_particles:"tuple",num_orbitals:"tuple")->"list":
    neut_state_init = list(range(0,num_particles[0]))
    prot_state_init = list(range(num_orbitals[0],num_orbitals[0]+num_particles[1]))
    nucl_state_init = neut_state_init + prot_state_init
    pair_list = list(combinations(nucl_state_init,2))
    return pair_list
def custom_excitation_list(num_spatial_orbitals: int,num_particles:tuple): ## note: num_orbitals is crutial information, but it is not input(parameter_py takes care of this)
    # the function is of resemblance of the excitations selected in the Hamiltonian, but not really"
    non_repeat_list = list(combinations(range(0,sum(num_orbitals)),2))
    
    neut_orbitals_list = list(range(0,num_orbitals[0]))
    prot_orbitals_list = list(range(num_orbitals[0], sum(num_orbitals)))
    neut_state_list = list(range(0,num_particles[0]))
    prot_state_list = list(range(num_orbitals[0], num_orbitals[0] + num_particles[1]))

    init_state_indeces = neut_state_list + prot_state_list
    init_pair_list = HFground_pair_list(num_particles, num_orbitals) ## same functioned used in the txt_read.ipynb

    allowed_init = list(set(non_repeat_list) & set(init_pair_list))
    allowed_fina = non_repeat_list
    my_excitation_list = []

    for init in allowed_init:
        for fina in allowed_fina:
            if (fina[0] in init_state_indeces) or (fina[1] in init_state_indeces):
                pass
            elif ((init[0] in neut_orbitals_list) == (fina[0] in neut_orbitals_list) and
                (init[1] in neut_orbitals_list) == (fina[1] in neut_orbitals_list) and
                (init[0] in prot_orbitals_list) == (fina[0] in prot_orbitals_list) and
                (init[1] in prot_orbitals_list) == (fina[1] in prot_orbitals_list) 
               ):
                excitations = [init,fina];
                my_excitation_list.append(tuple(excitations) if (excitations not in my_excitation_list) else tuple())
    my_excitation_list.sort()
    return my_excitation_list

vqe_excitations = custom_excitation_list # or replace with "d" if wish to use default vqe_excitations list



## Not used if adapt_veq is not used (quan_algo != "adaptVQE") ##
# grad_maxiter = 200
# grad_tol = 0.001
## Optimizer information
## MAybe include configuration of cobyla in the future (classical optimizer)
## REF https://www.geeksforgeeks.org/how-to-import-variables-from-another-file-in-python/



