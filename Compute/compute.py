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
    print("Intial Point            : ", initial_point, file = f)
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


## Defining SPSA optimizer
if optmz =="SPSA":
    def loss(x):
        result = estimator.run(var_form,Hamiltonian , x).result()
        return np.real(result.values[0])
    lr, perturb = optimizer.calibrate(loss = loss, initial_point=[1]+[0]*(len(var_form.excitation_list) -1 ) )
    # lr = np.array([0.10000, 0.05000, 0.03333, 0.02500, 0.02000, 0.01667, 0.01429, 0.01250, 0.01111, 0.01000, 0.00909, 0.00833, 0.00769, 0.00714, 0.00667, 0.00625, 0.00588, 0.00556, 0.00526, 0.00500, 0.00476, 0.00455, 0.00435, 0.00417, 0.00400, 0.00385, 0.00370, 0.00357, 0.00345, 0.00333, 0.00323, 0.00312, 0.00303, 0.00294, 0.00286, 0.00278, 0.00270, 0.00263, 0.00256, 0.00250, 0.00244, 0.00238, 0.00233, 0.00227, 0.00222, 0.00217, 0.00213, 0.00208, 0.00204, 0.00200, 0.00196, 0.00192, 0.00189, 0.00185, 0.00182, 0.00179, 0.00175, 0.00172, 0.00169, 0.00167, 0.00164, 0.00161, 0.00159, 0.00156, 0.00154, 0.00152, 0.00149, 0.00147, 0.00145, 0.00143, 0.00141, 0.00139, 0.00137, 0.00135, 0.00133, 0.00132, 0.00130, 0.00128, 0.00127, 0.00125, 0.00123, 0.00122, 0.00120, 0.00119, 0.00118, 0.00116, 0.00115, 0.00114, 0.00112, 0.00111, 0.00110, 0.00109, 0.00108, 0.00106, 0.00105, 0.00104, 0.00103, 0.00102, 0.00101, 0.00100, 0.00099])
    # perturb = np.array([0.10000, 0.08706, 0.08027, 0.07579, 0.07248, 0.06988, 0.06776, 0.06598, 0.06444, 0.06310, 0.06190, 0.06084, 0.05987, 0.05899, 0.05818, 0.05743, 0.05674, 0.05610, 0.05549, 0.05493, 0.05439, 0.05389, 0.05341, 0.05296, 0.05253, 0.05212, 0.05173, 0.05135, 0.05099, 0.05065, 0.05032, 0.05000, 0.04969, 0.04940, 0.04911, 0.04884, 0.04857, 0.04831, 0.04806, 0.04782, 0.04758, 0.04735, 0.04713, 0.04691, 0.04670, 0.04650, 0.04630, 0.04611, 0.04592, 0.04573, 0.04555, 0.04537, 0.04520, 0.04503, 0.04487, 0.04471, 0.04455, 0.04439, 0.04424, 0.04409, 0.04395, 0.04380, 0.04366, 0.04353, 0.04339, 0.04326, 0.04313, 0.04300, 0.04288, 0.04275, 0.04263, 0.04251, 0.04240, 0.04228, 0.04217, 0.04206, 0.04195, 0.04184, 0.04173, 0.04163, 0.04152, 0.04142, 0.04132, 0.04122, 0.04113, 0.04103, 0.04094, 0.04084, 0.04075, 0.04066, 0.04057, 0.04048, 0.04039, 0.04031, 0.04022, 0.04014, 0.04005, 0.03997, 0.03989, 0.03981, 0.03973])
    optimizer.learning_rate = lr
    optimizer.perturbation = perturb
    print(optimizer.learning_rate)


# Define Solver
from qiskit.algorithms.minimum_eigensolvers import VQE, AdaptVQE
vqe = VQE(
    estimator = estimator,
    ansatz = var_form,
    optimizer = optimizer,
    callback=store_intermediate_result,
    initial_point=initial_point)
adapt_vqe = AdaptVQE(
    vqe,
    threshold = grad_tol,
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
### Saving them into csv for future reference
conver_csv = pd.DataFrame(list(zip(counts, values,param_list,stdeviation)), columns=["eval_count","eval_values","Parameters","stdeviation"])
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

plt.yticks(np.arange(ylocs[0],ylocs[-1], step=0.2))
plt.xticks(np.arange(xlocs[1],xlocs[-1], step=xlocs[-2]/25), rotation=70)
plt.grid(visible=True)

plt.xlabel("Iterations/Eval_count")
plt.ylabel("Energy")
plt.legend()
plt.title("Convergence plot for "+str(pathfilename["output_id"])+nucleus_name)

plt.savefig(pathfilename["conver_png"])


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
