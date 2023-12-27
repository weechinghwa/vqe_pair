#!/usr/bin/env python
# coding: utf-8

## All package and functions used are defined in utils
from utils import *
from calc_config import *
from vqe import *

## Setting to use latest framework (pauli)
import qiskit_nature
qiskit_nature.settings.use_pauli_sum_op = False

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
if esti == "esti0":
    backend_dummy = "NOPE:Exact_eval"
else:
    backend_dummy = estimator.backend
## Record config information on the abstract result and full result file.
with open(pathfilename["full_result"], "a") as f:
    print("##### ##### ##### ##### ##### Configuration info START ##### ##### ##### ##### #####", file =f)
    print("Computation for nucleus : ", nucleus_name, file=f)
    print("Computer name           : ", pcname, file=f)
    print("Estimator               : ", f"esti=={esti} ", estimator, file=f)
    print("Backend                 : ", backend_dummy, file=f)
    print("Input directory name    : ", input_dir, file=f)
    print("Start time              : ", start_time, file=f)
    print("Algorithm used          : ", quan_algo, file=f)
    for i in optimizer.__dict__:
        print("                          |",i, optimizer.__dict__[i], file=f)
    print("Size of excitations     : ", len(var_form.excitation_list), file=f)
    print("Excitations input       : ", var_form.excitation_list, file=f)
    print("Intial Point            : ", initial_point, file = f)
with open(pathfilename["abstract_result"], "a") as f:
    print("##### ##### ##### ##### ##### Configuration info START ##### ##### ##### ##### #####", file =f)
    print("Computation for nucleus : ", nucleus_name, file=f)
    print("Computer name           : ", pcname, file=f)
    print("Estimator               : ", estimator, file=f)
    print("Backend                 : ", backend_dummy, file=f)
    print("Input directory name    : ", input_dir, file=f)
    print("Start time              : ", start_time, file=f)
    print("Algorithm used          : ", quan_algo, file=f)
    print("include_onebody?        : ", include_onebody, file=f)
    print("include_twobody?        : ", include_twobody, file=f)
    print("Size of excitations     : ", len(var_form.excitation_list), file=f)
    print("Intial Point            : ", initial_point, file = f)
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
    print("Size of obs_onebody     : ", len(obs_onebody_df),file=f)
    print("Size of obs_twobody     : ", len(obs_twobody_df),file=f)
    print("Factor in twobody terms : ", two_factor, file=f)
    print("Optimizer's config      : |", optimizer, file=f)
    for i in optimizer.__dict__:
        print("                          |",i, optimizer.__dict__[i], file=f)
    print("Twobody matrix elements      :-",file=f)
    pd.set_option('display.max_rows', obs_twobody_df.shape[0]+1),
    print(obs_twobody_df, file=f)

with open(pathfilename["abstract_result"], "a") as f:
    print("num_particles           : ", num_particles, file=f)
    print("num_orbitals            : ", num_spatial_orbitals, file=f)
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

## LR and perturb initialized as None
lr, perturb = None, None
alpha = None
## Defining SPSA optimizer
from sympy import Symbol, sequence
if optmz =="SPSA":
    def loss(x):
        result = estimator.run(var_form,Hamiltonian , x).result()
        return np.real(result.values[0])
    alpha = 0.602 ; target_magnitude = 0.1 ; A = 0 ; gamma = 0.101 ; c = 0.1
    lr, perturb = optimizer.calibrate(gamma = gamma, c = c, target_magnitude = target_magnitude, alpha = alpha, stability_constant  = A, 
                                      loss = loss, initial_point=initial_point )

    optimizer.learning_rate = lr
    optimizer.perturbation = perturb

# Define Solver
from qiskit_algorithms.minimum_eigensolvers import VQE, AdaptVQE
vqe = VQE(
    estimator = estimator,
    ansatz = var_form,
    optimizer = optimizer,
    callback=store_intermediate_result,
    initial_point=initial_point)
adapt_vqe = AdaptVQE(
    vqe,
    gradient_threshold = grad_tol,
    eigenvalue_threshold = optimizer_tol,
    max_iterations = grad_maxiter)

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
    print("lr schedule (float if constant):        ", lr, file=f)
    print("perturb schedule (float if constant):   ", perturb, file=f)
    if alpha is not None:
        print(f"alpha = {alpha} ; target_magnitude = {target_magnitude} ; A = {A} ; gamma = {gamma} ; c = {c}", file=f)
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

if pass_manager == None:
    fin_cir = vqe_result.optimal_circuit.assign_parameters(vqe_result.optimal_parameters).decompose().decompose().decompose()
    fin_cir.draw("mpl", filename = pathfilename["subresult_dir"] + "-circ.png")
    fin_cir_details = f"Circuit Depth {fin_cir.depth()}; Compositions: {fin_cir.count_ops()}"
    pass
else: 
    fin_cir = pass_manager.run(vqe_result.optimal_circuit.assign_parameters(vqe_result.optimal_parameters))
    fin_cir.draw("mpl", filename = pathfilename["subresult_dir"] + "-circ.png")
    fin_cir_details = f"Circuit Depth {fin_cir.depth()}; Compositions: {fin_cir.count_ops()}"

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


with open(pathfilename["abstract_result"], "a") as f:
    print(f"{input_dir} Done!! ", "@", current_time, "Time elapsed : ",time_elapsed_mins, "mins ; Energy Eigenvalue: ",vqe_result.eigenvalue,file=f)
    print(f"With Backend:    {backend_dummy};     on computer:    {pcname}",file = f)
    print(f"Parameters        : Excitations of {optimal_excitations} with params {optimal_point}", file = f )
    print("Fin Cir Details    : ", fin_cir_details ,file=f)
    print(" ", file = f)
    print("H, HF              : ", round(H_HF,6), file=f)
    print("one, HF            : ", round(one_HF,6), file=f)
    print("two, HF            : ", round(two_HF,6), file=f)
    print("H, UCCDopt         : ", round(H_UCCDopt,6), file=f)
    print("one, UCCDopt       : ", round(one_UCCDopt,6), file=f)
    print("two, UCCDopt       : ", round(two_UCCDopt,6), file=f)
    

# Draw the circuit
with open(pathfilename["full_result"], "a") as f:
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    print(" ",file=f)
    print("**************************  Pauli op         **************************", file=f)
    print(Hamiltonian,file=f)


    
## Convergence information
### Saving them into csv for future reference
conver_csv = pd.DataFrame(list(zip(counts, values,param_list,stdeviation)), columns=["eval_count","eval_value","Parameters","stdeviation"])
conver_csv.to_csv(pathfilename["callback"])


## Plot them out
from matplotlib import pyplot as plt
import numpy as np

plt.figure(figsize = (20,10))
plt.rcParams.update({'font.size': 12})

plt.plot(counts, values)
## The grids
ylocs, ylabels = plt.yticks()
xlocs, xlabels = plt.xticks()
xstep = round(xlocs[-2]/25)
plt.xlim(0,xlocs[-1])
# plt.yticks(np.arange(ylocs[0],ylocs[-1], step=round(max(ylocs)-min(ylocs))/10))
plt.xticks(np.arange(xlocs[1],xlocs[-1], step=xstep))
plt.grid(visible=True)

plt.xlabel("Iterations/Eval_count")
plt.ylabel("Energy")
plt.legend()
plt.title("VQEcallback-Optimization Steps for "+str(pathfilename["output_id"])+nucleus_name)

plt.savefig(pathfilename["subresult_dir"]+"-VQE_opt_step.png")

if optmz =="SPSA":
    with open(pathfilename["subresult_dir"]+"_SPSA_TC_callback.txt", "a") as f: 
        print(f"(nfev, parameters, value, stepsize, accepted)\n",file = f)
        print(optimizer.termination_checker.collected, file = f)

    SPSA_callback = pd.DataFrame(list(zip(SPSA_callback_counts, SPSA_callback_param_list,SPSA_callback_values,SPSA_callback_stepsize,SPSA_callback_accept)), columns=["count", "param_list", "value", "stepsize", "accepted"])
    SPSA_callback.to_csv(pathfilename["subresult_dir"]+"_SPSA_callback.csv")
    SPSA_callback_counts = np.array(SPSA_callback_counts)
    ## plot it out
    plt.clf()
    plt.figure(figsize = (20,10))
    plt.rcParams.update({'font.size': 12})
    plt.plot(SPSA_callback_counts/3, SPSA_callback_values)
    ## The grids
    ylocs, ylabels = plt.yticks()
    xlocs, xlabels = plt.xticks()
    
    # plt.yticks(np.arange(ylocs[0],ylocs[-1], step=round(max(ylocs)-min(ylocs))/10))
    try:
        xstep = round(xlocs[-2]/25)
        plt.xlim(0,len(SPSA_callback_values)+xstep)
        plt.xticks(np.arange(0,xlocs[-1], step=xstep))
    except:
        plt.xlim(0,len(SPSA_callback_values)+2)
        plt.xticks(np.arange(0,len(SPSA_callback_values)+2))
    plt.grid(visible=True)

    plt.xlabel("Iterations")
    plt.ylabel("Energy")
    plt.legend()
    plt.title("SPSAcallback-Optimization Steps for "+str(pathfilename["output_id"])+nucleus_name)

    plt.savefig(pathfilename["subresult_dir"]+"-SPSA_opt_step.png")


print("Calculation Done!! ", "@", current_time, "Time elapsed : ",time_elapsed_mins, "mins ; Energy Eigenvalue: ",vqe_result.eigenvalue)
print("Calculation ID     : ", pathfilename["output_id"])
print("H, HF              : ", round(H_HF,6), )
print("one, HF            : ", round(one_HF,6), )
print("two, HF            : ", round(two_HF,6), )
print("H, UCCDopt         : ", round(H_UCCDopt,6), )
print("one, UCCDopt       : ", round(one_UCCDopt,6), )
print("two, UCCDopt       : ", round(two_UCCDopt,6), )
print("Fin Cir Details    : ", fin_cir_details)
print("Optimal Params     : ", vqe_result.optimal_parameters)



# Record final essential result to a single csv file
## The following are the codes that ease the process of compiling the computed result
with open("Result/computed_result@Hpc.txt", "a") as f:
    print(
        pathfilename["full_result"],"|",
        start_time,"|",
        end_time,"|",
        time_elapsed_mins,"|",
        " ","|",
        f"Final_circuit Details: {fin_cir_details} ","|",
        input_dir,"|",
        two_factor,"|",
        hermitian_info,"|",
        "H:"+str(Hamiltonian_fermop_len)+";1B:"+str(len(obs_onebody_df))+";2B:"+str(len(obs_twobody_df))+"|",
        type(estimator), backend_dummy ,shots,"shots","|",
        quan_algo+";",type(optimizer),"|",
        "none|",
        len(var_form.excitation_list),";",vqe_excitations, "|",
        optimizer_maxiter, "|",
        optimizer_tol, "|",
        " ", "|",
        " ","|",
        vqe_result.eigenvalue,"|",
        "none","|",
        " ", file = f)
