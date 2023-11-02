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
    print("Estimator               : ", estimator, file=f)
    print("Backend                 : ", estimator.backend, file=f)
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
    print("Estimator               : ", estimator, file=f)
    print("Backend                 : ", estimator.backend, file=f)
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
    # alpha = 1.2 ; a = 0.5 ; A = 0 ; gamma = 1; c = 0.5
    # lr, perturb = optimizer.calibrate(gamma = gamma, c = c, target_magnitude = a, alpha = alpha, stability_constant  = A, 
    #                                   loss = loss, initial_point=[1]+[0]*(len(var_form.excitation_list) -1 ) )
    lr = 0.01 # np.array([0.20000, 0.12746, 0.09793, 0.08123, 0.07026, 0.06241, 0.05646, 0.05176, 0.04795, 0.04477, 0.04208, 0.03977, 0.03775, 0.03598, 0.03440, 0.03299, 0.03171, 0.03056, 0.02950, 0.02853, 0.02764, 0.02682, 0.02606, 0.02535, 0.02468, 0.02406, 0.02348, 0.02293, 0.02241, 0.02192, 0.02146, 0.02102, 0.02061, 0.02021, 0.01983, 0.01947, 0.01913, 0.01880, 0.01849, 0.01818, 0.01789, 0.01762, 0.01735, 0.01709, 0.01684, 0.01660, 0.01637, 0.01615, 0.01594, 0.01573, 0.01553, 0.01533, 0.01514, 0.01496, 0.01478, 0.01461, 0.01444, 0.01428, 0.01412, 0.01397, 0.01382, 0.01368, 0.01354, 0.01340, 0.01326, 0.01313, 0.01300, 0.01288, 0.01276, 0.01264, 0.01252, 0.01241, 0.01230, 0.01219, 0.01208, 0.01198, 0.01188, 0.01178, 0.01168, 0.01159, 0.01150, 0.01140, 0.01131, 0.01123, 0.01114, 0.01106, 0.01097, 0.01089, 0.01081, 0.01073, 0.01066, 0.01058, 0.01051, 0.01044, 0.01036, 0.01029, 0.01022, 0.01016, 0.01009, 0.01002, 0.00996, 0.00990, 0.00983, 0.00977, 0.00971, 0.00965, 0.00959, 0.00953, 0.00948, 0.00942, 0.00937, 0.00931, 0.00926, 0.00921, 0.00915, 0.00910, 0.00905, 0.00900, 0.00895, 0.00890, 0.00886, 0.00881, 0.00876, 0.00872, 0.00867, 0.00863, 0.00858, 0.00854, 0.00849, 0.00845, 0.00841, 0.00837, 0.00833, 0.00829, 0.00825, 0.00821, 0.00817, 0.00813, 0.00809, 0.00805, 0.00802, 0.00798, 0.00794, 0.00791, 0.00787, 0.00784, 0.00780, 0.00777, 0.00773, 0.00770, 0.00767, 0.00764, 0.00760, 0.00757, 0.00754, 0.00751, 0.00748, 0.00745, 0.00742, 0.00739, 0.00736, 0.00733, 0.00730, 0.00727, 0.00724, 0.00721, 0.00718, 0.00715, 0.00713, 0.00710, 0.00707, 0.00705, 0.00702, 0.00699, 0.00697, 0.00694, 0.00692, 0.00689, 0.00687, 0.00684, 0.00682, 0.00679, 0.00677, 0.00674, 0.00672, 0.00670, 0.00667, 0.00665, 0.00663, 0.00660, 0.00658, 0.00656, 0.00654, 0.00652, 0.00649, 0.00647, 0.00645, 0.00643, 0.00641, 0.00639, 0.00637, 0.00635, 0.00633, 0.00631, 0.00629, 0.00627, 0.00625, 0.00623, 0.00621, 0.00619, 0.00617, 0.00615, 0.00613, 0.00611, 0.00609, 0.00608, 0.00606, 0.00604, 0.00602, 0.00600, 0.00599, 0.00597, 0.00595, 0.00593, 0.00592, 0.00590, 0.00588, 0.00587, 0.00585, 0.00583, 0.00582, 0.00580, 0.00578, 0.00577, 0.00575, 0.00574, 0.00572, 0.00570, 0.00569, 0.00567, 0.00566, 0.00564, 0.00563, 0.00561, 0.00560, 0.00558, 0.00557, 0.00555, 0.00554, 0.00553, 0.00551, 0.00550, 0.00548, 0.00547, 0.00545, 0.00544, 0.00543, 0.00541, 0.00540, 0.00539, 0.00537, 0.00536, 0.00535, 0.00533, 0.00532, 0.00531, 0.00529, 0.00528, 0.00527, 0.00526, 0.00524, 0.00523, 0.00522, 0.00521, 0.00519, 0.00518, 0.00517, 0.00516, 0.00515, 0.00513, 0.00512, 0.00511, 0.00510, 0.00509, 0.00507, 0.00506, 0.00505, 0.00504, 0.00503, 0.00502, 0.00501, 0.00499, 0.00498, 0.00497, 0.00496, 0.00495, 0.00494, 0.00493, 0.00492, 0.00491, 0.00490, 0.00489, 0.00488, 0.00487, 0.00486, 0.00485, 0.00483, 0.00482, 0.00481, 0.00480, 0.00479, 0.00478, 0.00477, 0.00476, 0.00475, 0.00474, 0.00474, 0.00473, 0.00472, 0.00471, 0.00470, 0.00469, 0.00468, 0.00467, 0.00466, 0.00465, 0.00464, 0.00463, 0.00462, 0.00461, 0.00460, 0.00460, 0.00459, 0.00458, 0.00457, 0.00456, 0.00455, 0.00454, 0.00453, 0.00452, 0.00452, 0.00451, 0.00450, 0.00449, 0.00448, 0.00447, 0.00446, 0.00446, 0.00445, 0.00444, 0.00443, 0.00442, 0.00442, 0.00441, 0.00440, 0.00439, 0.00438, 0.00438, 0.00437, 0.00436, 0.00435, 0.00434, 0.00434, 0.00433, 0.00432, 0.00431, 0.00431, 0.00430, 0.00429, 0.00428, 0.00428, 0.00427, 0.00426, 0.00425, 0.00425, 0.00424, 0.00423, 0.00422, 0.00422, 0.00421, 0.00420, 0.00419, 0.00419, 0.00418, 0.00417, 0.00417, 0.00416, 0.00415, 0.00415, 0.00414, 0.00413, 0.00412, 0.00412, 0.00411, 0.00410, 0.00410, 0.00409, 0.00408, 0.00408, 0.00407, 0.00406, 0.00406, 0.00405, 0.00404, 0.00404, 0.00403, 0.00403, 0.00402, 0.00401, 0.00401, 0.00400, 0.00399, 0.00399, 0.00398, 0.00397, 0.00397, 0.00396, 0.00396, 0.00395, 0.00394, 0.00394, 0.00393, 0.00393, 0.00392, 0.00391, 0.00391, 0.00390, 0.00390, 0.00389, 0.00388, 0.00388, 0.00387, 0.00387, 0.00386, 0.00385, 0.00385, 0.00384, 0.00384, 0.00383, 0.00383, 0.00382, 0.00382, 0.00381, 0.00380, 0.00380, 0.00379, 0.00379, 0.00378, 0.00378, 0.00377, 0.00377, 0.00376, 0.00375, 0.00375, 0.00374, 0.00374, 0.00373, 0.00373, 0.00372, 0.00372, 0.00371, 0.00371, 0.00370, 0.00370, 0.00369, 0.00369, 0.00368, 0.00368, 0.00367, 0.00367, 0.00366, 0.00366, 0.00365, 0.00365, 0.00364, 0.00364, 0.00363, 0.00363, 0.00362, 0.00362, 0.00361, 0.00361, 0.00360, 0.00360, 0.00359, 0.00359, 0.00358, 0.00358, 0.00357, 0.00357, 0.00356, 0.00356, 0.00355, 0.00355, 0.00354, 0.00354, 0.00354, 0.00353, 0.00353, 0.00352, 0.00352, 0.00351, 0.00351, 0.00350, 0.00350, 0.00349, 0.00349, 0.00349, 0.00348, 0.00348, 0.00347, 0.00347, 0.00346, 0.00346, 0.00345, 0.00345, 0.00345, 0.00344, 0.00344, 0.00343, 0.00343, 0.00342, 0.00342, 0.00342, 0.00341, 0.00341, 0.00340, 0.00340, 0.00339, 0.00339, 0.00339, 0.00338, 0.00338, 0.00337, 0.00337, 0.00337, 0.00336, 0.00336, 0.00335, 0.00335, 0.00335, 0.00334, 0.00334, 0.00333, 0.00333, 0.00333, 0.00332, 0.00332, 0.00331, 0.00331, 0.00331, 0.00330, 0.00330, 0.00329, 0.00329, 0.00329, 0.00328, 0.00328, 0.00328, 0.00327, 0.00327, 0.00326, 0.00326, 0.00326, 0.00325, 0.00325, 0.00324, 0.00324, 0.00324, 0.00323, 0.00323, 0.00323, 0.00322, 0.00322, 0.00322, 0.00321, 0.00321, 0.00320, 0.00320, 0.00320, 0.00319, 0.00319, 0.00319, 0.00318, 0.00318, 0.00318, 0.00317, 0.00317, 0.00317, 0.00316, 0.00316, 0.00316, 0.00315, 0.00315, 0.00314, 0.00314, 0.00314, 0.00313, 0.00313, 0.00313, 0.00312, 0.00312, 0.00312, 0.00311, 0.00311, 0.00311, 0.00310, 0.00310, 0.00310, 0.00309, 0.00309, 0.00309, 0.00308, 0.00308, 0.00308, 0.00307, 0.00307, 0.00307, 0.00307, 0.00306, 0.00306, 0.00306, 0.00305, 0.00305, 0.00305, 0.00304, 0.00304, 0.00304, 0.00303, 0.00303, 0.00303, 0.00302, 0.00302, 0.00302, 0.00301, 0.00301, 0.00301, 0.00301, 0.00300, 0.00300, 0.00300, 0.00299, 0.00299, 0.00299, 0.00298, 0.00298, 0.00298, 0.00298, 0.00297, 0.00297, 0.00297, 0.00296, 0.00296, 0.00296, 0.00295, 0.00295, 0.00295, 0.00295, 0.00294, 0.00294, 0.00294, 0.00293, 0.00293, 0.00293, 0.00293, 0.00292, 0.00292, 0.00292, 0.00291, 0.00291, 0.00291, 0.00291, 0.00290, 0.00290, 0.00290, 0.00289, 0.00289, 0.00289, 0.00289, 0.00288, 0.00288, 0.00288, 0.00288, 0.00287, 0.00287, 0.00287, 0.00286, 0.00286, 0.00286, 0.00286, 0.00285, 0.00285, 0.00285, 0.00285, 0.00284, 0.00284, 0.00284, 0.00283, 0.00283, 0.00283, 0.00283, 0.00282, 0.00282, 0.00282, 0.00282, 0.00281, 0.00281, 0.00281, 0.00281, 0.00280, 0.00280, 0.00280, 0.00280, 0.00279, 0.00279, 0.00279, 0.00279, 0.00278, 0.00278, 0.00278, 0.00278, 0.00277, 0.00277, 0.00277, 0.00277, 0.00276, 0.00276, 0.00276, 0.00276, 0.00275, 0.00275, 0.00275, 0.00275, 0.00274, 0.00274, 0.00274, 0.00274, 0.00273, 0.00273, 0.00273, 0.00273, 0.00272, 0.00272, 0.00272, 0.00272, 0.00271, 0.00271, 0.00271, 0.00271, 0.00271, 0.00270, 0.00270, 0.00270, 0.00270, 0.00269, 0.00269, 0.00269, 0.00269, 0.00268, 0.00268, 0.00268, 0.00268, 0.00268, 0.00267, 0.00267, 0.00267, 0.00267, 0.00266, 0.00266, 0.00266, 0.00266, 0.00266, 0.00265, 0.00265, 0.00265, 0.00265, 0.00264, 0.00264, 0.00264, 0.00264, 0.00264, 0.00263, 0.00263, 0.00263, 0.00263, 0.00262, 0.00262, 0.00262, 0.00262, 0.00262, 0.00261, 0.00261, 0.00261, 0.00261, 0.00260, 0.00260, 0.00260, 0.00260, 0.00260, 0.00259, 0.00259, 0.00259, 0.00259, 0.00259, 0.00258, 0.00258, 0.00258, 0.00258, 0.00258, 0.00257, 0.00257, 0.00257, 0.00257, 0.00257, 0.00256, 0.00256, 0.00256, 0.00256, 0.00256, 0.00255, 0.00255, 0.00255, 0.00255, 0.00254, 0.00254, 0.00254, 0.00254, 0.00254, 0.00253, 0.00253, 0.00253, 0.00253, 0.00253, 0.00253, 0.00252, 0.00252, 0.00252, 0.00252, 0.00252, 0.00251, 0.00251, 0.00251, 0.00251, 0.00251, 0.00250, 0.00250, 0.00250, 0.00250, 0.00250, 0.00249, 0.00249, 0.00249, 0.00249, 0.00249, 0.00248, 0.00248, 0.00248, 0.00248, 0.00248, 0.00248, 0.00247, 0.00247, 0.00247, 0.00247, 0.00247, 0.00246, 0.00246, 0.00246, 0.00246, 0.00246, 0.00245, 0.00245, 0.00245, 0.00245, 0.00245, 0.00245, 0.00244, 0.00244, 0.00244, 0.00244, 0.00244, 0.00243, 0.00243, 0.00243, 0.00243, 0.00243, 0.00243, 0.00242, 0.00242, 0.00242, 0.00242, 0.00242, 0.00242, 0.00241, 0.00241, 0.00241, 0.00241, 0.00241, 0.00240, 0.00240, 0.00240, 0.00240, 0.00240, 0.00240, 0.00239, 0.00239, 0.00239, 0.00239, 0.00239, 0.00239, 0.00238, 0.00238, 0.00238, 0.00238, 0.00238, 0.00238, 0.00237, 0.00237, 0.00237, 0.00237, 0.00237, 0.00237, 0.00236, 0.00236, 0.00236, 0.00236, 0.00236, 0.00236, 0.00235, 0.00235, 0.00235, 0.00235, 0.00235, 0.00235, 0.00234, 0.00234, 0.00234, 0.00234, 0.00234, 0.00234, 0.00233, 0.00233, 0.00233, 0.00233, 0.00233, 0.00233, 0.00232, 0.00232, 0.00232, 0.00232, 0.00232, 0.00232, 0.00232, 0.00231, 0.00231, 0.00231, 0.00231, 0.00231, 0.00231, 0.00230, 0.00230, 0.00230, 0.00230, 0.00230, 0.00230, 0.00230, 0.00229, 0.00229, 0.00229, 0.00229, 0.00229, 0.00229, 0.00228, 0.00228, 0.00228, 0.00228, 0.00228, 0.00228, 0.00228, 0.00227, 0.00227, 0.00227, 0.00227, 0.00227, 0.00227, 0.00226, 0.00226, 0.00226, 0.00226, 0.00226, 0.00226, 0.00226, 0.00225, 0.00225, 0.00225, 0.00225, 0.00225, 0.00225, 0.00225, 0.00224, 0.00224])
    perturb = 0.01 # np.array([0.01]*1000)
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
    print("lr schedule (float if constant):        ", lr, file=f)
    print("perturb schedule (float if constant):   ", perturb, file=f)
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

plt.yticks(np.arange(ylocs[0],ylocs[-1], step=round(max(ylocs)-min(ylocs))/10))
plt.xticks(np.arange(xlocs[1],xlocs[-1], step=xlocs[-2]/25), rotation=70)
plt.grid(visible=True)

plt.xlabel("Iterations/Eval_count")
plt.ylabel("Energy")
plt.legend()
plt.title("Convergence plot for "+str(pathfilename["output_id"])+nucleus_name)

plt.savefig(pathfilename["conver_png"])

if optmz =="SPSA":
    values_dum = []
    print(len(values))
    for i in range(0,int((len(values)-1)/2)):
        index_dum = 2*i; index_next = index_dum + 1
        print(index_dum,index_next)
        value_dum = values[index_dum] if values[index_dum] < values[index_next] else values[index_next]
        values_dum.append(value_dum)
    values_dum.append(values[-1])

    # ## Save the info
    # lr_perturb = pd.DataFrame(list(zip(lr,perturb)), columns=["LearningRate","Perturbation"])
    # lr_perturb.to_csv(pathfilename["SPSA_lr_perturb"])

    SPSA_convergence = pd.DataFrame(list(zip(list(range(0,len(values_dum))), values_dum)), columns=["iter_count", "Energy"])
    SPSA_convergence.to_csv(pathfilename["subresult_dir"]+"-SPSA_converg.csv")

    ## plot it out
    plt.clf()
    plt.figure(figsize = (20,10))
    plt.rcParams.update({'font.size': 12})

    plt.plot(list(range(0,len(values_dum))), values_dum)
    ## The grids
    ylocs, ylabels = plt.yticks()
    xlocs, xlabels = plt.xticks()

    plt.yticks(np.arange(ylocs[0],ylocs[-1], step=round(max(ylocs)-min(ylocs))/10))
    plt.xticks(np.arange(xlocs[1],xlocs[-1], step=xlocs[-2]/25), rotation=70)
    plt.grid(visible=True)

    plt.xlabel("Iterations")
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
        type(estimator), estimator.backend ,shots,"shots",",",
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
