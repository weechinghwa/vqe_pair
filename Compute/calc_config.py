import ast
from utils import GlobalDataManager

data_manager = GlobalDataManager()

## Argparser
import argparse
argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--input_dir", help="The input file's directory name")
argParser.add_argument("-s", "--shots", help="Integer, number of shots of the circuit")
argParser.add_argument("-o", "--optmz", help="Define Optimizer, accepted optimizer: COBYLA or SPSA or DIRECT_L_RAND or ESCH")
argParser.add_argument("-n", "--pcname", help="3-character alphabets, the name of the PC doing the calculation")
argParser.add_argument("-esti", "--estimator", help="To define which estimator to use" )
argParser.add_argument("-tc", "--termination_checker", help="Define termination function for SPSA")
argParser.add_argument("-lrp", "--learningrate_perturbation", help="Parameters for SPSA LR_P powerseries. Takes a python list [ alpha, target_magnitude, A, gamma, c  ].")

## Other parameters
### initial_state in vqe.py (Choosing the starting point of the calculation)
### optimizer_maxiter 
### include_imaginary of UCC in vqe.py 

## esti is predefined as None
esti = None

args = argParser.parse_args()

for key, value in vars(args).items():
    print(f"{key}: {value}")

## Source File input ##
input_dir = args.input_dir; data_manager.add_data("input_dir", input_dir)
shots = args.shots; data_manager.add_data("shots", shots)
optmz = args.optmz; data_manager.add_data("optimizer", optmz)
pcname = args.pcname #or "Hlp" or Ypc"
esti = args.estimator; data_manager.add_data("estimator", esti)
tc = "TerminationChecker" if args.termination_checker == None else args.termination_checker
param_powerser_lrp =  ast.literal_eval(args.learningrate_perturbation)

# input_dir = "000_test0" #200_Be9

### The following doesnt require setting up, unless file naming is different
obs_onebody_csv = "../Data/"+input_dir+"/"+input_dir+"-1B_H_input.csv"
obs_twobody_csv = "../Data/"+input_dir+"/"+input_dir+"-2B_H_input.csv"
parameter_py = "../Data/"+input_dir+"/"+input_dir+"-parameter.txt"

## Computation config ## 
quan_algo = "VQE"; data_manager.add_data("algorithm", quan_algo)## (string)(VQE or adaptVQE)

optimizer_maxiter = 200
optimizer_tol = 0.001

## Estimator
# edit the vqe.py to change the setting of the estimator
# Choosing either the exact, fakebackend or the aer simulator(with noise model)

## import computational data (observalbles and parameters)
parameter_txt=[]
with open (parameter_py, 'rt') as myfile:    #filename
    for line in myfile:
        line = line.rstrip('\n')
        parameter_txt.append(line)
parameter = parameter_txt[1].split(",,,")
num_orbitals = ast.literal_eval(parameter[0])
num_spin_orbitals = int(parameter[1])
num_particles = ast.literal_eval(parameter[2])
num_spatial_orbitals = int(num_spin_orbitals/2)
two_factor = float(parameter[3]) ## from 1611_Be8 and onward
include_onebody = ast.literal_eval(parameter[4])
include_twobody = ast.literal_eval(parameter[5])
## False for N-P separated calculation
# Note: to run a N_P separated calculation,
# one shall fill up the alpha state with the 
# pairs, and left the final one to be in beta
# then set N_P_separate == True.
# N_P_separate = False
# preserve_spin = not N_P_separate
try: 
    preserve_spin = ast.literal_eval(parameter[6])
except:
    preserve_spin = True
# print(num_orbitals,num_spin_orbitals,num_particles,num_spatial_orbitals,preserve_spin) # to test if the data is correct (not important in production)
# print(parameter)


## Setup custom excitation list ##
from itertools import combinations
def HFground_pair_list(num_particles:"tuple",num_orbitals:"tuple")->"list":
    neut_state_init = list(range(0,num_particles[0]))
    prot_state_init = list(range(num_orbitals[0],num_orbitals[0]+num_particles[1]))
    nucl_state_init = neut_state_init + prot_state_init
    pair_list = list(combinations(nucl_state_init,2))
    return pair_list

#Custom excitation 1
def like_qiskit(num_spatial_orbitals: int,num_particles:tuple): 
    ## note: num_orbitals is crutial information, but it is not defined in qiskit, only as part of modification
    # (parameter.py takes care of this: define this in parameter.py in each calculation input_dir)
    # This function should mimic the excitation of a qiskit's UCC "d"-excitation with preserve_spin = False
    non_repeat_list = list(combinations(range(0,sum(num_orbitals)),2))
    
    neut_orbitals_list = list(range(0,num_orbitals[0]))
    prot_orbitals_list = list(range(num_orbitals[0], sum(num_orbitals)))
    neut_state_list = list(range(0,num_particles[0]))
    prot_state_list = list(range(num_orbitals[0], num_orbitals[0] + num_particles[1]))

    init_state_indeces = neut_state_list + prot_state_list
    init_pair_list = HFground_pair_list(num_particles, num_orbitals) ## same functioned used in the txt_read.ipynb

    allowed_init = list(set(non_repeat_list) & set(init_pair_list))
    allowed_fina = non_repeat_list
    my_excitation = set()

    for init in allowed_init:
        for fina in allowed_fina:
            if (fina[0] in init_state_indeces) or (fina[1] in init_state_indeces):
                pass
            elif(   (fina[0] in neut_orbitals_list + prot_orbitals_list) and
                    (fina[1] in neut_orbitals_list + prot_orbitals_list) and
                    not preserve_spin
               ):
                my_excitation.add(tuple([init,fina]))
            elif(   (init[0] in neut_orbitals_list) == (fina[0] in neut_orbitals_list) and
                    (init[1] in neut_orbitals_list) == (fina[1] in neut_orbitals_list) and
                    (init[0] in prot_orbitals_list) == (fina[0] in prot_orbitals_list) and
                    (init[1] in prot_orbitals_list) == (fina[1] in prot_orbitals_list) and
                    preserve_spin
               ):
                my_excitation.add(tuple([init,fina]))

    my_excitation_list = list(my_excitation)
    my_excitation_list.sort()
    return my_excitation_list
#Custom excitation 2
def pair_clusters(num_spatial_orbitals: int,num_particles:tuple): 
    ## note: num_orbitals is crutial information, but it is not defined in qiskit, only as part of modification
    # (parameter.py takes care of this: define this in parameter.py in each calculation input_dir)
    # This function constrain the like_qiskit function to only pairs    
    neut_orbitals_list = list(range(0,num_orbitals[0]))
    prot_orbitals_list = list(range(num_orbitals[0], sum(num_orbitals)))
    neut_state_list = list(range(0,num_particles[0]))
    prot_state_list = list(range(num_orbitals[0], num_orbitals[0] + num_particles[1]))

    init_state_indeces = neut_state_list + prot_state_list
    init_pair_list = HFground_pair_list(num_particles, num_orbitals) ## same functioned used in the txt_read.ipynb
    number_pairs = [(i, i+1) for i in range(0, 50, 2)]

    allowed_init = list(set(init_pair_list) & set(number_pairs))
    allowed_fina = number_pairs
    my_excitation = set()

    for init in allowed_init:
        for fina in allowed_fina:
            if (fina[0] in init_state_indeces) or (fina[1] in init_state_indeces):
                pass
            elif(   (fina[0] in neut_orbitals_list + prot_orbitals_list) and
                    (fina[1] in neut_orbitals_list + prot_orbitals_list) and
                    not preserve_spin
                ):
                my_excitation.add(tuple([init,fina]))
            elif(   (init[0] in neut_orbitals_list) == (fina[0] in neut_orbitals_list) and
                    (init[1] in neut_orbitals_list) == (fina[1] in neut_orbitals_list) and
                    (init[0] in prot_orbitals_list) == (fina[0] in prot_orbitals_list) and
                    (init[1] in prot_orbitals_list) == (fina[1] in prot_orbitals_list) and
                    preserve_spin
                ):
                my_excitation.add(tuple([init,fina]))
    my_excitation_list = list(my_excitation)
    my_excitation_list.sort()
    return my_excitation_list
#Custom excitation 3
def UpCCGSD(num_spatial_orbitals: int,num_particles:tuple): 
    ## note: num_orbitals is crutial information, but it is not defined in qiskit, only as part of modification
    # (parameter.py takes care of this: define this in parameter.py in each calculation input_dir)
    # This function constrain the like_qiskit function to only pairs    
    neut_orbitals_list = list(range(0,num_orbitals[0]))
    prot_orbitals_list = list(range(num_orbitals[0], sum(num_orbitals)))
    neut_state_list = list(range(0,num_particles[0]))
    prot_state_list = list(range(num_orbitals[0], num_orbitals[0] + num_particles[1]))

    init_state_indeces = neut_state_list + prot_state_list
    init_pair_list = HFground_pair_list(num_particles, num_orbitals) ## same functioned used in the txt_read.ipynb
    number_pairs = [(i, i+1) for i in range(0, 50, 2)]

    allowed_init = list(set(init_pair_list) & set(number_pairs))
    allowed_fina = number_pairs
    my_excitation = set()

    for init in allowed_init:
        for fina in allowed_fina:
            if (fina[0] in init_state_indeces) or (fina[1] in init_state_indeces):
                pass
            elif(   (fina[0] in neut_orbitals_list + prot_orbitals_list) and
                    (fina[1] in neut_orbitals_list + prot_orbitals_list) and
                    not preserve_spin
                ):
                my_excitation.add(tuple([init,fina]))
            elif(   (init[0] in neut_orbitals_list) == (fina[0] in neut_orbitals_list) and
                    (init[1] in neut_orbitals_list) == (fina[1] in neut_orbitals_list) and
                    (init[0] in prot_orbitals_list) == (fina[0] in prot_orbitals_list) and
                    (init[1] in prot_orbitals_list) == (fina[1] in prot_orbitals_list) and
                    preserve_spin
                ):
                my_excitation.add(tuple([init,fina]))
    my_excitation_list = list(my_excitation)

    for i in neut_orbitals_list:
        for j in neut_orbitals_list:
            if j > i:
                my_excitation_list.append(((i,),(j,)))
            else: 
                pass
    for i in prot_orbitals_list:
        for j in prot_orbitals_list:
            if j > i:
                my_excitation_list.append(((i,),(j,)))
            else: 
                pass

    my_excitation_list.sort()
    return my_excitation_list

#Custom excitation Custom of the custom
def custom_excite(num_spatial_orbitals: int,num_particles:tuple):
    return([((2,3),(4,5))])

vqe_excitations = pair_clusters # or replace with "d" if wish to use default vqe_excitations list

## Not used if adapt_veq is not used (quan_algo != "adaptVQE") ##
grad_maxiter = 200
grad_tol = 0.00001
