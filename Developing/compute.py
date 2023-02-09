#!/usr/bin/env python
# coding: utf-8

# # Calculation of Be8 pairing energy

# ### Configuration
# Whatever variable not in this script, is imported. They are tagged as init_config
from calc_config_ import *
import datetime

# Record the start time for computation; And computation configuration.
start_time = datetime.datetime.now()
with open(output_filename, "a") as f:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Calc started @",start_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
    print("Configuration of this Calculation:-",file=f)
    print("************************** Configuration info START **************************",file=f)
    print("Algorithm            : ", quan_algo,file=f)
    print("Excitation           : ", excitations,file=f)
    print("Iter mode            : ", iter_mode,file=f)
    print("Optimizer maxiter    : ", optimizer_maxiter,file=f)
    print("Optimizer tolerance  : ", optimizer_tol,file=f)
    
if quan_algo == "adaptVQE":
    with open(output_filename, "a") as f:
        print("Gradient maxiter     : ", grad_maxiter,file=f)
        print("Gradient tolerance   : ", grad_tol,file=f)

pd.set_option('display.max_rows', obs_onebody_df.shape[0]+1)

with open(output_filename, "a") as f:
    print("num_particles        : ", num_particles,file=f)
    print("num_spatial_orbitals : ", num_spatial_orbitals,file=f)
    print("num_spin_orbitals    : ", num_spin_orbitals,file=f)
    print("Onebody matrix elements      :-",file=f)
    pd.set_option('display.max_rows', obs_onebody_df.shape[0]+1)
    print(obs_onebody_df, file=f)
    print("Twobody matrix elements      :-",file=f)
    pd.set_option('display.max_rows', obs_twobody_df.shape[0]+1)
    print(obs_twobody_df, file=f)

# ### The Hamiltonian
from qiskit_nature.second_q.operators import FermionicOp
import pandas as pd
tmp_ham = {}

# One body Term: Single particle energy levels
for index, row in obs_onebody_df.iterrows():
    init_ = int(row['i']); fina_ = int(row['f'])
    the_onestring = "+_" +str(fina_) + " " + "-_" +str(init_)
    tmp_ham[the_onestring] = row['e']

# Two body Terms: Pairing interaction
for index, row in obs_twobody_df.iterrows():
    init_1 = int(row['i1']); init_2 = int(row['i2']);
    fina_1 = int(row['f1']); fina_2 = int(row['f2']);
    the_twostring = "+_" +str(fina_1) + " " + "+_" +str(fina_2) + " " + "-_" +str(init_1) + " " + "-_" +str(init_2)
    tmp_ham[the_twostring] = row['V']

Hamil_pair = FermionicOp(tmp_ham, 
                          num_spin_orbitals=num_spin_orbitals, 
                          copy=False)


# Record the operators being evaluated/computed
with open(output_filename, "a") as f:
    print("The fermionic op     : ", file=f)
    print(Hamil_pair, file=f)
    print("************************** Configuration info END **************************",file=f)
    
if iter_mode == True:
    with open(iter_mode_output_filename, "a") as f:
        print("For more info, refer to result file with name := "+output_filename,file=f)
        print("************************** Computation Results as Follows **************************",file=f)


# ## Setting up of the VQE algorithm
# Define a converter aka mapping method
from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitConverter
qubit_converter = QubitConverter(JordanWignerMapper())

from qiskit_nature.second_q.circuit.library.initial_states import HartreeFock
from qiskit_nature.second_q.circuit.library.ansatzes import UCC

from qiskit.algorithms.optimizers import ISRES,COBYLA,SLSQP
from qiskit.algorithms.minimum_eigensolvers import VQE, AdaptVQE
from qiskit import Aer

# Hamiltonian
Ham = Hamil_pair
Ham = qubit_converter.map(Ham)

## Define Estimator
from qiskit.primitives import Estimator
estimator = Estimator()

# Mapping of Second quantized fermionic operator to Pauli
# qubit_op = qubit_converter.convert(hamiltonian,num_particles=num_particles)

# Define Initial State
initial_state = HartreeFock(
        num_spatial_orbitals=num_spatial_orbitals,
        num_particles=num_particles,
        qubit_converter=qubit_converter,
    )

# Build Ansatz
reps=1
var_form = UCC(
    num_particles=num_particles,
    num_spatial_orbitals=num_spatial_orbitals,
    excitations=excitations,
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

# To record list of excitations
with open(output_filename, "a") as f:
    print("Optimizer used:    ",optimizer,file = f)
    print("**************************   THe input list of excitations START   **************************",file = f)
    print(var_form.excitation_list, file = f)
    print("**************************   THe input list of excitations END   ****************************",file = f)


# ### The result
## quan_algo config
if quan_algo == "VQE":
    vqe_result = vqe.compute_minimum_eigenvalue(Ham) ## compute_minimum_eigenvalue
elif quan_algo == "adaptVQE":
    vqe_result = adapt_vqe.compute_minimum_eigenvalue(Ham)
else:
    print("PLEASE PROVIDE AN ALGORITHM NAME, it can be " + str(VQE)+ " or " + str(adaptVQE))

now = datetime.datetime.now()
with open(output_filename, "a") as f:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ","iteraction: ", str(1), "@",now,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
    print(vqe_result,file=f)
        
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
        vqe_current_result = vqe_current.compute_minimum_eigenvalue(Ham) ## compute current minimum eigenvalue
        vqe_current_energy = vqe_current_result.eigenvalue
        
        # Set initial_point for Iter(n+1); Prepare for next iteration
        optimal_point = vqe_current_result.optimal_point
        
        # Record current time
        now = datetime.datetime.now()

        # Record vqe_current_result
        with open(output_filename, "a") as f:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ ","iteration: ", counter, "@",now,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
            print(vqe_current_result,file=f)
        # Record only iteration number and energy of current iteration 
        with open(iter_mode_output_filename, "a") as f:
            print("iter : ", counter, "@", now, "; Energy Eigenvalue: ",vqe_current_energy,file=f)
            print("iter : ", counter, vqe_current_result,file=f)
    
    # After while loop, reset the result to final iteration of vqe evaluation
    vqe_result = vqe_current_result
else:
    pass

# Append information into the iter file
if iter_mode == True:
    with open(iter_mode_output_filename, "a") as f:
        print("Optimizer maxiter    : ", optimizer_maxiter,file=f)
        print("Excitation           : ", excitations,file=f)
        print("Optimizer tolerance  : ",optimizer_tol,file=f)
        print("The fermionic op     : ", file=f)
        print(Hamil_pair,file=f)
        ### last iter information into the last block
        print("iter : ",  counter, "@", now, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)

# Draw the circuit
with open(circuitfilename, "a") as f:
    print("**************************  Optimal Circuit  **************************",file=f)
    print(vqe_result.optimal_circuit.decompose().decompose().draw(),file=f)


with open(output_filename, "a") as f:
    print("########################################################################################", file=f)
    print(file=f)
    print("**************************   VQE final iteration START   *********************************", file=f)
    print(vqe_result, file=f)
    print("**************************   VQE final iteration END     *********************************", file=f)
    print(file=f)
    print("########################################################################################", file=f)


# ## To find out what excitations had been used
adaptvqe_ansatz = {}
for cluster in vqe_result.optimal_circuit.operators:
     for i , cluster_term in enumerate(var_form.operators):
        if cluster.equals(cluster_term):
            adaptvqe_ansatz[var_form.excitation_list[i]] = cluster_term


with open(output_filename, "a") as f:
    print("Cluster terms used in the ansatz in the final iteraction:- ", file=f)
    print("************************** Cluster term list START *********************************", file=f)
    for i in adaptvqe_ansatz:
        print(i, file=f)
    print("************************** Cluster term list END *********************************", file=f)

end_time = datetime.datetime.now()
time_elapsed = end_time - start_time
time_elapsed_s = time_elapsed.total_seconds()
time_elapsed_mins = divmod(time_elapsed_s, 60)[0]

with open(output_filename, "a") as f:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Computation Ended @",end_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Total time elapsed(mins): ",+time_elapsed_mins,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
    print("**************************************** E ****************************************", file=f)
    print("**************************************** N ****************************************", file=f)
    print("**************************************** D ****************************************", file=f)

# Record final essential result to a single csv file
## The following are the codes that ease the process of compiling the computed result
with open("computed_result@Hpc.txt", "a") as f:
    print(output_filename,",",
        start_time,",",
        end_time,",",
        time_elapsed_mins,",",
        " ",",",
        " ",",",
        quan_algo,",",
        iter_mode,",",
        excitations,",",
        optimizer_maxiter,",",
        optimizer_tol,",",
        " ",",",
        " ",",",
        vqe_result.eigenvalue,",",
        str(counter),",",
        " ", file = f)



