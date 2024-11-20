from calc_config import *
from utils import TerminateThreeStep, TerminatePovSlope, TerminateThreeSMA, TerminateMinSlope, TerminateLnFit, TerminateLnFit10step, TerminateLnFit10stepRel, TerminationChecker, TerminateLnFit10stepRel_A, random_floats
from qiskit_nature.second_q.mappers import JordanWignerMapper
# from qiskit_nature.second_q.circuit.library.initial_states import HartreeFock
from np_hartree_fock import * ## Import custom init state
from qiskit_nature.second_q.circuit.library.ansatzes import UCC
from qiskit import Aer
from qiskit_algorithms.optimizers import ISRES,ESCH,DIRECT_L,DIRECT_L_RAND, CRS, ADAM,SLSQP, SPSA,QNSPSA,COBYLA

## Define callback function: to collect convergence information
counts = []; values = []; stdeviation = []; param_list = []
def store_intermediate_result(eval_count, parameters, mean, std):
    counts.append(eval_count)
    values.append(mean)
    param_list.append(parameters)
    stdeviation.append(std)

## Mapper (FermionicOp to SparsePauliOp transformation) ## 
qubit_mapper = JordanWignerMapper()

## Reference state / Initial state ## 
initial_state = HartreeFock(
    num_orbitals = num_orbitals,
    num_particles = num_particles,
    qubit_mapper = qubit_mapper)

## Ansatz
reps=1
var_form = UCC(
    num_particles=num_particles,
    num_spatial_orbitals=num_spatial_orbitals,
    excitations=vqe_excitations,
    qubit_mapper=qubit_mapper,
    reps=reps,
    initial_state=initial_state,
    include_imaginary=False,
    preserve_spin= preserve_spin)
ansatz_info = {"num_particles"           : num_particles        ,
               "num_spatial_orbitals"    : num_spatial_orbitals ,
               "excitations"             : str(vqe_excitations) ,
               "qubit_mapper"            : str(qubit_mapper)    ,
               "reps"                    : reps                 ,
               "include_imaginary"       : False                ,
               "preserve_spin"           : preserve_spin
               }
data_manager.add_data("ansatz", ansatz_info)

## Initial point
initial_point = [0]*len(var_form.excitation_list)

## Classical Optimizer ##
if optmz == "DIRECT_L_RAND":
    optimizer = DIRECT_L_RAND(max_evals=optimizer_maxiter)
SPSA_callback_counts = []; SPSA_callback_param_list = []; SPSA_callback_values = []; SPSA_callback_stepsize = []; SPSA_callback_accept = []
def SPSA_callback(spsa_count,spsa_param,spsa_value,spsa_stepsiz,spsa_accept):
    SPSA_callback_counts.append(spsa_count)
    SPSA_callback_param_list.append(spsa_param)
    SPSA_callback_values.append(spsa_value)
    SPSA_callback_stepsize.append(spsa_stepsiz)
    SPSA_callback_accept.append(spsa_accept)
if optmz =="SPSA":
    tc_dict = {"TerminationChecker": TerminationChecker(N=optimizer_maxiter), 
               "TerminateThreeStep": TerminateThreeStep(N = 10, tol = optimizer_tol),
               "TerminatePovSlope": TerminatePovSlope(N = 10),
               "TerminateThreeSMA": TerminateThreeSMA(N = 10, tol = optimizer_tol),
               "TerminateMinSlope": TerminateMinSlope(N = 10),
               "TerminateLnFit_neg_0.112" : TerminateLnFit(N = 10, coeff=-0.112),
               "TerminateLnFit_neg_0.1" : TerminateLnFit(N = 10, coeff=-0.1),
               "TerminateLnFit10step_neg_0.1" : TerminateLnFit10step(N=10, coeff=-0.1),
               "TerminateLnFit10stepRel" : TerminateLnFit10stepRel(N=10),
               "TerminateLnFit10stepRel_A08": TerminateLnFit10stepRel_A(N=10, m_diff=0.08),
               "TerminateLnFit10stepRel_A05": TerminateLnFit10stepRel_A(N=10, m_diff=0.05),
               "TerminateLnFit10stepRel_A01": TerminateLnFit10stepRel_A(N=10, m_diff=0.01),
               }
    termination_checker = tc_dict[tc]
    optimizer = SPSA(maxiter=optimizer_maxiter,termination_checker=termination_checker, callback=SPSA_callback)
    initial_point = [1] + [0]*(len(var_form.excitation_list) - 1)
    # initial_point = [0]*(len(var_form.excitation_list) - 1) + random_floats(-np.pi/2, np.pi/2, 1)
    # initial_point = [0.5] * len(var_form.excitation_list)
    # initial_point = random_floats(-np.pi/2, np.pi/2, len(var_form.excitation_list))

    spsa_info = {
        "optimizer": optmz,
        "termination_checker": tc,
        "maxiter": optimizer_maxiter,
        "initial_point": initial_point,
    }
    data_manager.add_data("optimizer", spsa_info)

if optmz == "COBYLA":
    optimizer=COBYLA(maxiter=optimizer_maxiter, disp=True, tol = optimizer_tol, rhobeg = 0.1)

if optmz == "ESCH":
    optimizer = ESCH(max_evals = optimizer_maxiter)
    
# Define estimator
from estimators import esti_dic
if esti == None: 
    print(f"Please define the esti properly with the following: {esti_dic.keys()}")
else:
    pass_manager, estimator = esti_dic[esti]
