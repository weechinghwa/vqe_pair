#!/usr/bin/env python
# coding: utf-8

## All package and functions used are defined in utils
from utils import *
from calc_config import *

## Run the ipynb to process the result text file to retrieve/extract information for the calculation
import nbformat
from nbconvert import PythonExporter
from types import SimpleNamespace

# Convert the notebook to a Python script
notebook_filename = 'txt_read.ipynb'
exporter = PythonExporter()
source, metadata = exporter.from_filename(notebook_filename)

# Execute the Python script in a namespace
namespace = SimpleNamespace()
exec(source, namespace.__dict__)

## In the txt_read.ipynb, the following variables are defined.
num_orbitals = namespace.num_orbitals
num_particles = namespace.num_particles
num_spin_orbitals = namespace.num_spin_orbitals
obs_onebody_df = namespace.obs_onebody_df
obs_twobody_df = namespace.obs_twobody_df
abs_main = namespace.abs_main
pathfilename = namespace.pathfilename
nucleus_name = namespace.nucleus_name
num_spatial_orbitals = int(num_spin_orbitals/2)

### Define excitation list (to be used in the VQE)
# Define excitations list
def custom_excitation_list(num_spatial_orbitals: int,num_particles):
    # the function is of resemblance of the excitations selected in the Hamiltonian, but not really"
    non_repeat_list = list(combinations(range(0,sum(num_orbitals)),2))
    
    neut_orbitals_list = list(range(0,num_orbitals[0]))
    prot_orbitals_list = list(range(num_orbitals[0], sum(num_orbitals)))
    neut_state_list = list(range(0,num_particles[0]))
    prot_state_list = list(range(num_orbitals[0], num_orbitals[0] + num_particles[1]))

    init_state_indeces = neut_state_list + prot_state_list
    init_pair_list = HFground_pair_list(num_particles, num_orbitals)

    allowed_init = list(set(non_repeat_list) & set(init_pair_list))
    allowed_fina = non_repeat_list
    # allowed_fina = []
    # for fina in non_repeat_list:
    #     if not fina[0] or fina[1] in neut_state_list + prot_state_list:
    #         allowed_fina.append(fina)

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
vqe_excitations = custom_excitation_list

## Setting up path and define names, pathfilename carry all the names for input and output
## This line was ran in the ipynb so, dont need to run once more 
# # # abs_main, nucleus, pathfilename = pathfilename_gen(pcname,input_txt)
os.chdir(abs_main)

# Record the start time for computation; And computation configuration.
start_time = datetime.now()

## Record config information on the abstract result and full result file.
with open(pathfilename["full_result"], "a") as f:
    print("##### ##### ##### ##### ##### Configuration info START ##### ##### ##### ##### #####", file =f)
    print("Computation for nucleus : ", nucleus_name, file=f)
    print("Computer name           : ", pcname, file=f)
    print("Input textfile name     : ", input_txt, file=f)
    print("Start time              : ", start_time, file=f)
    print("Algorithm used          : ", quan_algo, file=f)
    print("Iter mode               : ", iter_mode, file=f)
    print("Optimizer maxiter       : ", optimizer_maxiter, file=f)
    print("Optimizer tolerance     : ", optimizer_tol, file=f)
    print("Excitations input       : ", vqe_excitations(num_spatial_orbitals, num_particles), file=f)
with open(pathfilename["abstract_result"], "a") as f:
    print("##### ##### ##### ##### ##### Configuration info START ##### ##### ##### ##### #####", file =f)
    print("Computation for nucleus : ", nucleus_name, file=f)
    print("Computer name           : ", pcname, file=f)
    print("Input textfile name     : ", input_txt, file=f)
    print("Start time              : ", start_time, file=f)
    print("Algorithm used          : ", quan_algo, file=f)
    print("Iter mode               : ", iter_mode, file=f)
    print("Optimizer maxiter       : ", optimizer_maxiter, file=f)
    print("Optimizer tolerance     : ", optimizer_tol, file=f)
    print("Excitations input       : ", vqe_excitations(num_spatial_orbitals,num_particles), file=f)
if quan_algo == "adaptVQE":
    with open(pathfilename["abstract_result"],"a") as f1, open(pathfilename["full_result"], "a") as f2:
        print("Gradient maxiter        : ", grad_maxiter, file=f1)
        print("Gradient tolerance      : ", grad_tol, file=f1)
        print("Gradient maxiter        : ", grad_maxiter, file=f2)
        print("Gradient tolerance      : ", grad_tol, file=f2)

pd.set_option('display.max_rows', obs_onebody_df.shape[0]+1)

with open(pathfilename["full_result"], "a") as f:
    print("num_particles           : ", num_particles, file=f)
    print("num_orbitals            : ", num_spatial_orbitals, file=f)
    print("num_spatial_orbitals    : ", num_spatial_orbitals, file=f)
    print("num_spin_orbitals       : ", num_spin_orbitals, file=f)
    print("Onebody matrix elements      :-",file=f)
    pd.set_option('display.max_rows', obs_onebody_df.shape[0]+1)
    print(obs_onebody_df, file = f)
    print("Twobody matrix elements      :-",file=f)
    pd.set_option('display.max_rows', obs_twobody_df.shape[0]+1),
    print(obs_twobody_df, file=f)

with open(pathfilename["abstract_result"], "a") as f:
    print("num_particles           : ", num_particles, file=f)
    print("num_spatial_orbitals    : ", num_spatial_orbitals, file=f)
    print("num_spin_orbitals       : ", num_spin_orbitals, file=f)
    print("Size of obs_onebody     : ", len(obs_onebody_df),file=f)
    print("Size of obs_twobody     : ", len(obs_twobody_df),file=f)
    print("Configuration information recorded")

## The Hamiltonian
### Use the defined obs_onebody_df and obs_twobody_df to construct the Hamiltonian
from qiskit_nature.second_q.operators import FermionicOp
import pandas as pd
tmp_ham = {}

### One body Term: Single particle energy levels
for index, row in obs_onebody_df.iterrows():
    init_ = int(row['q_i']); fina_ = int(row['q_f'])
    the_onestring = "+_" +str(fina_) + " " + "-_" +str(init_)
    tmp_ham[the_onestring] = row['delta']

### Two body Terms: Pairing interaction
for index, row in obs_twobody_df.iterrows():
    init_1 = int(row['q_i1']); init_2 = int(row['q_i2']);
    fina_1 = int(row['q_f1']); fina_2 = int(row['q_f2']);
    the_twostring = "+_" +str(fina_1) + " " + "+_" +str(fina_2) + " " + "-_" +str(init_1) + " " + "-_" +str(init_2)
    tmp_ham[the_twostring] = row['V_ffii']

## The Hamiltonian Fermionic operator are given by
Hamiltonian = FermionicOp(tmp_ham, 
                          num_spin_orbitals=num_spin_orbitals, 
                          copy=False)

# Record the operators being evaluated/computed
with open(pathfilename["full_result"], "a") as f:
    print("The fermionic op        : ", Hamiltonian, file=f)
    print("##### ##### ##### ##### ##### Configuration info END ##### ##### ##### ##### #####", file=f)
    print("/n", file=f)

#### Setting up of the VQE algorithm
# Define a converter aka mapping method
from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitConverter
qubit_converter = QubitConverter(JordanWignerMapper())

# from qiskit_nature.second_q.circuit.library.initial_states import HartreeFock
from qiskit_nature.second_q.circuit.library.ansatzes import UCC
from qiskit.algorithms.optimizers import ISRES,COBYLA,SLSQP
from qiskit.algorithms.minimum_eigensolvers import VQE, AdaptVQE
from qiskit import Aer

# Hamiltonian
Hamiltonian = qubit_converter.map(Hamiltonian)

## Define Estimator
from qiskit.primitives import Estimator
estimator = Estimator()

## Reference state / Initial state
from np_hartreefock import * ## Import custom init state
initial_state = HartreeFock(
    num_orbitals = num_orbitals,
    num_particles = num_particles,
    qubit_converter = qubit_converter)

## Ansatz
reps=1
var_form = UCC(
    num_particles=num_particles,
    num_spatial_orbitals=num_spatial_orbitals,
    excitations=vqe_excitations,
    qubit_converter=qubit_converter,
    reps=reps,
    initial_state=initial_state
)

# Define classical optimizer
optimizer=COBYLA(
    maxiter=optimizer_maxiter,
    disp=True, 
    tol = optimizer_tol)

# Define Solver
vqe = VQE(
    estimator = estimator,
    ansatz = var_form,
    optimizer = optimizer)

adapt_vqe = AdaptVQE(vqe,
                     threshold = 0.001,
                     max_iterations = 200)


# To record list of optimizer used
with open(pathfilename["full_result"], "a") as f:
    print("Optimizer used       : ", optimizer, file=f)


if iter_mode == True:
    with open(pathfilename["abstract_result"], "a") as f:
        print("Shortened result for ", str(nucleus_name), file=f)
        print("For more info, refer to output file with name := ", pathfilename["full_result"], file=f)
        print("##### ##### ##### ##### ##### Shortened results as Follows ##### ##### ##### ##### #####", file=f)
        print("Computation started")
elif iter_mode == False:
    with open(pathfilename["abstract_result"], "a") as f:
        print("Shortened result for ", nucleus_name, file=f)
        print("For more info, refer to output file with name := ", pathfilename["full_result"], file=f)
        print("##### ##### ##### ##### ##### Shortened result( there should only be one line of result) as Follows ##### ##### ##### ##### #####", file=f)
        print("Computation started")

# ### The result
## quan_algo config
if quan_algo == "VQE":
    vqe_result = vqe.compute_minimum_eigenvalue(Hamiltonian) ## compute_minimum_eigenvalue
elif quan_algo == "adaptVQE":
    vqe_result = adapt_vqe.compute_minimum_eigenvalue(Hamiltonian)
else:
    print("PLEASE PROVIDE AN ALGORITHM NAME, it can be " + "VQE" + " or " + "adaptVQE" )

current_time = datetime.now()
counter = 1
with open(pathfilename["full_result"], "a") as f:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ","iteraction: ", str(1), "@",current_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print(vqe_result, file=f)
with open(pathfilename["abstract_result"], "a") as f:
    print("iter : ", counter, "@", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)
    print("iter : ", counter, "@", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue)
## Future to add, convergence message by the classical optimizer

## Note
# vqe_current refers to current vqe or vqe_iter(n)
# vqe refers to vqe_iter(n-1)
if iter_mode == True:
    vqe_energy = vqe_result.eigenvalue
    optimal_point = vqe_result.optimal_point
    vqe_current_energy = 0
    counter = 1

    while abs(vqe_energy - vqe_current_energy) > optimizer_tol: #condition for iter(n+1) #if current condition is not satisfied, the loop stop
        # Set Iter(n-1) info;
        counter += 1
        vqe_energy = vqe_current_energy
        
        # Generate Iter(n) info; Current VQE, use the previous optimal points as current initial points
        vqe_current = VQE(estimator = estimator, ansatz = var_form, optimizer = optimizer,initial_point=optimal_point)
        vqe_current_result = vqe_current.compute_minimum_eigenvalue(Hamiltonian) ## compute current minimum eigenvalue
        vqe_current_energy = vqe_current_result.eigenvalue
        
        # Set initial_point for Iter(n+1); Prepare for next iteration
        optimal_point = vqe_current_result.optimal_point
        
        # Record current time
        current_time = datetime.now()

        # Record vqe_current_result
        with open(pathfilename["full_result"], "a") as f:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ","iteration: ", counter, "@",current_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
            print(vqe_current_result,file=f)
        # Record only iteration number and energy of current iteration 
        with open(pathfilename["abstract_result"], "a") as f:
            print("iter : ", counter, "@", current_time, "; Energy Eigenvalue: ",vqe_current_energy,file=f)
            print("iter : ", counter, "@", current_time, "; Energy Eigenvalue: ",vqe_current_energy)
    # After while loop, reset the result to final iteration of vqe evaluation
    vqe_result = vqe_current_result
else:
    pass

# Append information into the iter file
if iter_mode == True:
    with open(pathfilename["abstract_result"], "a") as f:
        print("Optimizer maxiter    : ", optimizer_maxiter,file=f)
        print("Excitation           : ", vqe_excitations,file=f)
        print("Optimizer tolerance  : ",optimizer_tol,file=f)
        print("The fermionic op     : ", file=f)
        print(Hamiltonian,file=f)
        ### last iter information into the last block
        print("iter : ",  counter, "@", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)




with open(pathfilename["full_result"], "a") as f:
    print("########################################################################################", file=f)
    print(file=f)
    print("**************************   VQE final iteration START   *********************************", file=f)
    print(vqe_result, file=f)
    print("**************************   VQE final iteration END     *********************************", file=f)
    print(file=f)
    print("########################################################################################", file=f)
# Draw the circuit
with open(pathfilename["full_result"], "a") as f:
    print("**************************  Optimal Circuit  **************************",file=f)
    print(vqe_result.optimal_circuit.decompose().decompose().draw(),file=f)

# ## To find out what excitations had been used
adaptvqe_ansatz = {}
for cluster in vqe_result.optimal_circuit.operators:
     for i , cluster_term in enumerate(var_form.operators):
        if cluster.equals(cluster_term):
            adaptvqe_ansatz[var_form.excitation_list[i]] = cluster_term


with open(pathfilename["full_result"], "a") as f:
    print("Cluster terms used in the ansatz in the final iteraction(of adaptVQE):- ", file=f)
    print("************************** Cluster term list START *********************************", file=f)
    for i in adaptvqe_ansatz:
        print(i, file=f)
    print("************************** Cluster term list END *********************************", file=f)

end_time = datetime.now()
time_elapsed = end_time - start_time
time_elapsed_s = time_elapsed.total_seconds()
time_elapsed_mins = divmod(time_elapsed_s, 60)[0]

with open(pathfilename["full_result"], "a") as f:
    print("iter : ",  counter, "@", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Computation Ended @",end_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Total time elapsed(mins): ",+time_elapsed_mins,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
    print("**************************************** E ****************************************", file=f)
    print("**************************************** N ****************************************", file=f)
    print("**************************************** D ****************************************", file=f)

with open(pathfilename["abstract_result"], "a") as f:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Computation Ended @",end_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Total time elapsed(mins): ",+time_elapsed_mins,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
    print("**************************************** E ****************************************", file=f)
    print("**************************************** N ****************************************", file=f)
    print("**************************************** D ****************************************", file=f)

# Record final essential result to a single csv file
## The following are the codes that ease the process of compiling the computed result
with open("Result/computed_result@Hpc.txt", "a") as f:
    print(pathfilename["full_result"],",",
        start_time,",",
        end_time,",",
        time_elapsed_mins,",",
        " ",",",
        " ",",",
        quan_algo,",",
        iter_mode,",",
        len(vqe_excitations(num_spatial_orbitals, num_particles)),",",
        optimizer_maxiter,",",
        optimizer_tol,",",
        " ",",",
        " ",",",
        vqe_result.eigenvalue,",",
        str(counter),",",
        " ", file = f)



