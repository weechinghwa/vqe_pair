#!/usr/bin/env python
# coding: utf-8

## All package and functions used are defined in utils
from utils import *
from calc_config import *
from vqe import *



## The following are imported from the above calc_config and utils
import pandas as pd
obs_twobody_df = pd.read_csv(obs_twobody_csv) if include_twobody == True else []
obs_onebody_df = pd.read_csv(obs_onebody_csv) if include_onebody == True else []
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
    print("include_onebody?        : ", include_onebody, file=f)
    print("include_twobody?        : ", include_twobody, file=f)
    print("Size of excitations     : ", len(var_form.excitation_list), file=f)
if quan_algo == "adaptVQE":
    with open(pathfilename["abstract_result"],"a") as f1, open(pathfilename["full_result"], "a") as f2:
        print("Gradient maxiter        : ", grad_maxiter, file=f1)
        print("Gradient tolerance      : ", grad_tol, file=f1)
        print("Gradient maxiter        : ", grad_maxiter, file=f2)
        print("Gradient tolerance      : ", grad_tol, file=f2)

with open(pathfilename["full_result"], "a") as f:
    print("num_particles           : ", num_particles, file=f)
    print("num_orbitals            : ", num_spatial_orbitals, file=f)
    print("num_spatial_orbitals    : ", num_spatial_orbitals, file=f)
    print("num_spin_orbitals       : ", num_spin_orbitals, file=f)
    print("Observable data_id      : ", input_dir, file = f)    
    print("Size of obs_twobody     : ", len(obs_twobody_df),file=f)
    print("Factor in twobody terms : ", two_factor, file=f)
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
### Use the defined obs_twobody_df to construct the Hamiltonian
from qiskit_nature.second_q.operators import FermionicOp

### Two body Terms: Pairing interaction
if include_onebody == True:
    tmp_ham_one = {}
    for index, row in obs_onebody_df.iterrows():
        fina = int(row['i']); init = int(row['j'])
        the_onestring = "+_" +str(fina) + " " + "-_" +str(init) 
        tmp_ham_one[the_onestring] = row["epsilon"]
        tmp_ham = tmp_ham_one
else: 
    tmp_ham_one = {}
    
### Two body Terms: Pairing interaction
if include_twobody == True:
    tmp_ham_two = {}
    for index, row in obs_twobody_df.iterrows():
        fina_1 = int(row['i']); fina_2 = int(row['j']); 
        init_1 = int(row['k']); init_2 = int(row['l']); 
        the_twostring = "+_" +str(fina_1) + " " + "+_" +str(fina_2) + " " + "-_" +str(init_1) + " " + "-_" +str(init_2)
        tmp_ham_two[the_twostring] = two_factor*row['V_ijkl']
        tmp_ham = tmp_ham_two

if include_onebody == True and include_twobody == True:
    tmp_ham = z = {**tmp_ham_one, **tmp_ham_two}

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
Hamiltonian = qubit_mapper.map(Hamiltonian)
Hamiltonian_paulop_len = len(Hamiltonian)

# Begin Computation #
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
with open(pathfilename["full_result"], "a") as f:
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  ","iteraction: ", 1 , "@",current_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print(vqe_result, file=f)


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

optimal_excitations = []
with open(pathfilename["full_result"], "a") as f:
    print("Cluster terms used in the ansatz in the final iteraction(of adaptVQE):- ", file=f)
    print("************************** Cluster term list START *********************************", file=f)
    for i in adaptvqe_ansatz:
        print(i, adaptvqe_ansatz[i], file=f)
        optimal_excitations.append(adaptvqe_ansatz[i])
    print("************************** Cluster term list END *********************************", file=f)

end_time = datetime.now()
time_elapsed = end_time - start_time
time_elapsed_s = time_elapsed.total_seconds()
time_elapsed_mins = divmod(time_elapsed_s, 60)[0]

with open(pathfilename["full_result"], "a") as f:
    print("Computation done @", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Computation Ended @",end_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Total time elapsed(mins): ",+time_elapsed_mins,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
    print("**************************************** E ****************************************", file=f)
    print("**************************************** N ****************************************", file=f)
    print("**************************************** D ****************************************", file=f)

with open(pathfilename["abstract_result"], "a") as f:
    print("Computation done @", current_time, "; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Computation Ended @",end_time,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", file=f)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Total time elapsed(mins): ",+time_elapsed_mins,"  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",file=f)
    print("**************************************** E ****************************************", file=f)
    print("**************************************** N ****************************************", file=f)
    print("**************************************** D ****************************************", file=f)


# Generating the breakdown of the energy
optimal_point = []
for i in vqe_result.optimal_point:
    optimal_point.append(round(i,8))
def uccd_opt(num_spatial_orbitals: int,num_particles:tuple):
    the_list = optimal_excitations
    return the_list
uccd_opt = UCC(num_particles=num_particles,
                num_spatial_orbitals=num_spatial_orbitals,
                excitations=uccd_opt,
                qubit_mapper=qubit_mapper,
                reps=reps,
                initial_state=initial_state)

## to generate breakdown
## The Hamiltonian Fermionic operator are given by
Hamiltonian = FermionicOp(tmp_ham, num_spin_orbitals=num_spin_orbitals, copy=False)
Hamil_one = FermionicOp(tmp_ham_one, num_spin_orbitals=num_spin_orbitals, copy=False)
Hamil_two = FermionicOp(tmp_ham_two, num_spin_orbitals=num_spin_orbitals, copy=False)

Hamiltonian = qubit_mapper.map(Hamiltonian)
Hamil_one = qubit_mapper.map(Hamil_one)
Hamil_two = qubit_mapper.map(Hamil_two)

H_HF = estimator.run(initial_state, Hamiltonian).result().values[0]
one_HF = estimator.run(initial_state, Hamil_one).result().values[0]
two_HF = estimator.run(initial_state, Hamil_two).result().values[0]
H_UCCDopt = estimator.run(uccd_opt, Hamiltonian, optimal_point).result().values[0]
one_UCCDopt = estimator.run(uccd_opt, Hamil_one, optimal_point).result().values[0]
two_UCCDopt = estimator.run(uccd_opt, Hamil_two, optimal_point).result().values[0]
optimal_circuit_depth = vqe_result.optimal_circuit.decompose().decompose().decompose().depth()

with open(pathfilename["abstract_result"], "a") as f:
    print("H, HF              : ", round(H_HF,6), file=f)
    print("one, HF            : ", round(one_HF,6), file=f)
    print("two, HF            : ", round(two_HF,6), file=f)
    print("H, UCCDopt         : ", round(H_UCCDopt,6), file=f)
    print("one, UCCDopt       : ", round(one_UCCDopt,6), file=f)
    print("two, UCCDopt       : ", round(two_UCCDopt,6), file=f)
    print(" ", file=f)
    print("Circuit Depth      : ", optimal_circuit_depth,file=f)
    

# Draw the circuit
with open(pathfilename["full_result"], "a") as f:
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    print("**************************  Pauli op         **************************", file=f)
    print(Hamiltonian,file=f)

    
## Convergence information
import pylab

pylab.rcParams["figure.figsize"] = (12, 4)
pylab.plot(counts, values)
pylab.xlabel("Iterations/Eval_count")
pylab.ylabel("Energy")
pylab.title("Convergence for "+str(pathfilename["output_id"]))
pylab.savefig(pathfilename["conver_png"])

print("Calculation Done!! ", "@", current_time, "Time elapsed : ",time_elapsed_mins, "mins ; Energy Eigenvalue: ",vqe_result.eigenvalue)
print("H, HF              : ", round(H_HF,6), )
print("one, HF            : ", round(one_HF,6), )
print("two, HF            : ", round(two_HF,6), )
print("H, UCCDopt         : ", round(H_UCCDopt,6), )
print("one, UCCDopt       : ", round(one_UCCDopt,6), )
print("two, UCCDopt       : ", round(two_UCCDopt,6), )
print("Circuit Depth      : ", optimal_circuit_depth)

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
        type(estimator), shots,"shots",",",
        quan_algo+";",type(optimizer),",",
        "none,",
        len(var_form.excitation_list),";",vqe_excitations, ",",
        optimizer_maxiter,",",
        optimizer_tol,",",
        " ",",",
        " ",",",
        vqe_result.eigenvalue,",",
        "none",",",
        " ", file = f)
