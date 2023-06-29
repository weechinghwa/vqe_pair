#!/usr/bin/env python
# coding: utf-8

## All package and functions used are defined in utils
from utils import *
from calc_config import *
from vqe import *



## The following are imported from the above calc_config and utils
import pandas as pd
obs_onebody_df = pd.read_csv(obs_onebody_csv)
obs_twobody_df = pd.read_csv(obs_twobody_csv)

# vqe_excitations = custom_excitation_list or 'd' ; check calc_config
# nucleus_name ; check pathfilename_gen



## Setting up path and define names, pathfilename carry all the names for input and output
## This line was ran in the ipynb so, dont need to run once more 
abs_main, nucleus_name, pathfilename = pathfilename_gen(pcname,input_dir)
os.chdir(abs_main)



# Record the start time for computation; And computation configuration.
start_time = datetime.now()

## Record config information on the abstract result and full result file.
with open(pathfilename["full_result"], "a") as f:
    print("##### ##### ##### ##### ##### Configuration info START ##### ##### ##### ##### #####", file =f)
    print("Computation for nucleus : ", nucleus_name, file=f)
    print("Computer name           : ", pcname, file=f)
    print("Input directory name    : ", input_dir, file=f)
    print("Start time              : ", start_time, file=f)
    print("Algorithm used          : ", quan_algo, file=f)
    print("Iter mode               : ", iter_mode, file=f)
    print("Optimizer's config      : |", optimizer, file=f)
    for i in optimizer.__dict__:
        print("                          |",i, optimizer.__dict__[i], file=f)
    print("Size of excitations     : ", len(var_form.excitation_list), file=f)
    print("Excitations input       : ", var_form.excitation_list, file=f)
with open(pathfilename["abstract_result"], "a") as f:
    print("##### ##### ##### ##### ##### Configuration info START ##### ##### ##### ##### #####", file =f)
    print("Computation for nucleus : ", nucleus_name, file=f)
    print("Computer name           : ", pcname, file=f)
    print("Input directory name    : ", input_dir, file=f)
    print("Start time              : ", start_time, file=f)
    print("Algorithm used          : ", quan_algo, file=f)
    print("Iter mode               : ", iter_mode, file=f)
    print("include_onebody?        : ", include_onebody, file=f)
    print("include_twobody?        : ", include_twobody, file=f)
    print("Size of excitations     : ", len(var_form.excitation_list), file=f)
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
    print("Observable data_id      : ", input_dir, file = f)    
    print("Size of obs_onebody     : ", len(obs_onebody_df),file=f)
    print("Size of obs_twobody     : ", len(obs_twobody_df),file=f)
    print("Factor in twobody terms : ", two_factor, file=f)
    print("Onebody matrix elements      :-",file=f)
    pd.set_option('display.max_rows', obs_onebody_df.shape[0]+1)
    print(obs_onebody_df, file = f)
    print("Factor in twobody terms : ", two_factor, file=f)
    print("Twobody matrix elements      :-",file=f)
    pd.set_option('display.max_rows', obs_twobody_df.shape[0]+1),
    print(obs_twobody_df, file=f)

with open(pathfilename["abstract_result"], "a") as f:
    print("num_particles           : ", num_particles, file=f)
    print("num_spatial_orbitals    : ", num_spatial_orbitals, file=f)
    print("num_spin_orbitals       : ", num_spin_orbitals, file=f)
    print("Observable data_id      : ", input_dir, file = f)
    print("Size of obs_onebody     : ", len(obs_onebody_df),file=f)
    print("Size of obs_twobody     : ", len(obs_twobody_df),file=f)
    print("Factor in twobody terms : ", two_factor, file=f)
    print("Optimizer's config      : |", optimizer, file=f)
    for i in optimizer.__dict__:
        print("                          |",i, optimizer.__dict__[i], file=f)
    print("Configuration information recorded")

## The Hamiltonian
### Use the defined obs_onebody_df and obs_twobody_df to construct the Hamiltonian
from qiskit_nature.second_q.operators import FermionicOp
tmp_ham_one = {}
tmp_ham_two = {}

### One body Term: Single particle energy levels
if include_onebody == True:
    for index, row in obs_onebody_df.iterrows():
        init_ = int(row['q_i']); fina_ = int(row['q_f'])
        the_onestring = "+_" +str(fina_) + " " + "-_" +str(init_)
        tmp_ham_one[the_onestring] = row['epsilon']

### Two body Terms: Pairing interaction
if include_twobody == True:
    for index, row in obs_twobody_df.iterrows():
        init_1 = int(row['l']); init_2 = int(row['k']);   # init1 == l ; init2 == k
        fina_1 = int(row['i']); fina_2 = int(row['j']);   # fina1 == i ; fina2 == j ; so that these 4 make up the term
                                                                # V_{ijkl} +_i +_j -_l -_k ； so that the matrix elements in the df (or the data file) remains Vijkl
        the_twostring = "+_" +str(fina_1) + " " + "+_" +str(fina_2) + " " + "-_" +str(init_1) + " " + "-_" +str(init_2)
        tmp_ham_two[the_twostring] = two_factor*row['V_ijkl']

tmp_ham = tmp_ham_one + tmp_ham_two
## The Hamiltonian Fermionic operator are given by
Hamiltonian = FermionicOp(tmp_ham, 
                          num_spin_orbitals=num_spin_orbitals, 
                          copy=False)
hermitian_info = Hamiltonian.is_hermitian()

# Record the operators being evaluated/computed
with open(pathfilename["full_result"], "a") as f:
    print("The fermionic op        : ", Hamiltonian, file=f)
    print("##### ##### ##### ##### ##### Configuration info END ##### ##### ##### ##### #####", file=f)
    print("", file=f)

    
## Prepping Hamiltonian to be computed. Mapping. ## 
Hamiltonian_fermop_len = len(Hamiltonian)
Hamiltonian = qubit_converter.map(Hamiltonian)
Hamiltonian_paulop_len = len(Hamiltonian)

# Begin Computation #

# VQE is important in the first few lines
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
        print("VQE running ... ... ...")


## The result ##
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
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ","iteraction: ", 1 , "@",current_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print(vqe_result, file=f)
with open(pathfilename["abstract_result"], "a") as f:
    if iter_mode == True: 
        print("iter : ", counter, "@", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)
        print("iter : ", counter, "@", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue)
    elif iter_mode == False:
        print("No iter, shortened Result computed ", "@", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)
## Future to add, convergence message by the classical optimizer

## Note
# vqe_current refers to current vqe or vqe_iter(n)
# vqe refers to vqe_iter(n-1)
if iter_mode == True:
    vqe_energy = vqe_result.eigenvalue
    optimal_point = vqe_result.optimal_point
    vqe_current_energy = 0

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


with open(pathfilename["full_result"], "a") as f:
    print("########################################################################################", file=f)
    print(file=f)
    print("**************************   VQE final iteration START   *********************************", file=f)
    print(vqe_result, file=f)
    print("**************************   VQE final iteration END     *********************************", file=f)
    print(file=f)
    print("########################################################################################", file=f)

# ## To find out what excitations had been used
adaptvqe_ansatz = {}
for counter_1 , cluster in enumerate(vqe_result.optimal_circuit.operators):
     for counter_2 , cluster_term in enumerate(var_form.operators):
        if cluster == cluster_term:
            adaptvqe_ansatz[(counter_1,counter_2)] = var_form.excitation_list[counter_2]

        # if cluster.equals(cluster_term):
        #     adaptvqe_ansatz[var_form.excitation_list[i]] = cluster_term

with open(pathfilename["full_result"], "a") as f:
    print("Cluster terms used in the ansatz in the final iteraction(of adaptVQE):- ", file=f)
    print("************************** Cluster term list START *********************************", file=f)
    for i in adaptvqe_ansatz:
        print(i, adaptvqe_ansatz[i], file=f)
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


# Generating the breakdown of the energy
optimal_point = vqe_result.optimal_point
uccd = vqe_result.optimal_circuit

## to generate breakdown
## The Hamiltonian Fermionic operator are given by
Hamiltonian = FermionicOp(tmp_ham, 
                          num_spin_orbitals=num_spin_orbitals, 
                          copy=False)
Hamil_one = FermionicOp(tmp_ham_one, num_spin_orbitals=num_spin_orbitals, copy=False)
Hamil_two = FermionicOp(tmp_ham_two, num_spin_orbitals=num_spin_orbitals, copy=False)

Hamiltonian = qubit_converter.map(Hamiltonian)
Hamil_one = qubit_converter.map(Hamil_one)
Hamil_two = qubit_converter.map(Hamil_two)

H_HF = estimator.run(initial_state, Hamiltonian).result().values[0]
one_HF = estimator.run(initial_state, Hamil_one).result().values[0]
two_HF = estimator.run(initial_state, Hamil_two).result().values[0]
H_UCCDopt = estimator.run(uccd, Hamiltonian, optimal_point).result().values[0]
one_UCCDopt = estimator.run(uccd, Hamil_one, optimal_point).result().values[0]
two_UCCDopt = estimator.run(uccd, Hamil_two, optimal_point).result().values[0]
with open(pathfilename["abstract_result"], "a") as f:
    print("H, HF              : ", round(H_HF,6), file=f)
    print("one, HF            : ", round(one_HF,6), file=f)
    print("two, HF            : ", round(two_HF,6), file=f)
    print("H, UCCDopt         : ", round(H_UCCDopt,6), file=f)
    print("one, UCCDopt       : ", round(one_UCCDopt,6), file=f)
    print("two, UCCDopt       : ", round(two_UCCDopt,6), file=f)
    print("State occupancy breakdown:-")
    
    append_occupy = []
    for i in tmp_ham_one:
        one_ham = FermionicOp({i:tmp_ham_one[i]},num_spin_orbitals=num_spin_orbitals, copy = False)
        one_occupy = FermionicOp({i:1},num_spin_orbitals=num_spin_orbitals, copy = False)
        one_occupy = qubit_converter.map(one_occupy)
        one_ham = qubit_converter.map(one_ham)
        one_occupy_ham = estimator.run(initial_state,  one_occupy).result().values[0]
        one_occupy = estimator.run(var_form,  one_occupy, optimal_point).result().values[0]
        one_UCCDopt = estimator.run(var_form, one_ham, optimal_point).result().values[0]
        append_occupy.append(one_occupy)
        
        print('{0:<10}'.format(i),": ",'{0:<8}'.format(str(round(one_UCCDopt,3))),one_occupy_ham,"-->",round(one_occupy,3),file=f)
    print("after  : ", sum(append_occupy),file=f)


# Draw the circuit
with open(pathfilename["full_result"], "a") as f:
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    # print("**************************  Optimal Circuit  **************************",file=f)
    # print(vqe_result.optimal_circuit.decompose().decompose().draw(),file=f)
    print("**************************  Pauli op         **************************", file=f)
    print(Hamiltonian,file=f)

    
## Convergence infroamtion
import pylab

pylab.rcParams["figure.figsize"] = (12, 4)
pylab.plot(counts, values)
pylab.xlabel("Iterations/Eval_count")
pylab.ylabel("Energy")
pylab.title("Convergence for "+str(pathfilename["output_id"]))
pylab.savefig(pathfilename["conver_png"])

print("Calculation Done!! ", "@", current_time, "Time elapsed : ",time_elapsed_mins, "mins ; Energy Eigenvalue: ",vqe_result.eigenvalue)

# Record final essential result to a single csv file
## The following are the codes that ease the process of compiling the computed result
with open("Result/computed_result@Hpc.txt", "a") as f:
    print(
        pathfilename["full_result"],",",
        start_time,",",
        end_time,",",
        time_elapsed_mins,",",
        " ",",",
        " ",",",
        input_dir,",",
        two_factor,",",
        hermitian_info,",",
        "H:"+str(Hamiltonian_fermop_len)+";1B:"+str(len(obs_onebody_df))+";2B:"+str(len(obs_twobody_df))+",",
        type(estimator),",",
        quan_algo+";",type(optimizer),",",
        iter_mode,",",
        len(var_form.excitation_list),";",vqe_excitations ",",
        optimizer_maxiter,",",
        optimizer_tol,",",
        " ",",",
        " ",",",
        vqe_result.eigenvalue,",",
        str(counter),",",
        " ", file = f)
