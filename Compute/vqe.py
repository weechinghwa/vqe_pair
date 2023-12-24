from calc_config import *
from utils import TerminationChecker

## Define callback function: to collect convergence information
counts = []; values = []; stdeviation = []; param_list = []
def store_intermediate_result(eval_count, parameters, mean, std):
    counts.append(eval_count)
    values.append(mean)
    param_list.append(parameters)
    stdeviation.append(std)


## Mapper (FermionicOp to SparsePauliOp transformation) ## 
from qiskit_nature.second_q.mappers import JordanWignerMapper
qubit_mapper = JordanWignerMapper()


## Reference state / Initial state ## 
# from qiskit_nature.second_q.circuit.library.initial_states import HartreeFock
from np_hartree_fock import * ## Import custom init state
initial_state = HartreeFock(
    num_orbitals = num_orbitals,
    num_particles = num_particles,
    qubit_mapper = qubit_mapper)


## Ansatz libraries ##
from qiskit_nature.second_q.circuit.library.ansatzes import UCC
# from ucc_trott import UCC as UCC_trott
## Ansatz
reps=1
var_form = UCC(
    num_particles=num_particles,
    num_spatial_orbitals=num_spatial_orbitals,
    excitations=vqe_excitations,
    qubit_mapper=qubit_mapper,
    reps=reps,
    initial_state=initial_state,
    preserve_spin= preserve_spin)
# var_form = UCC_trott(
#     num_particles=num_particles,
#     num_spatial_orbitals=num_spatial_orbitals,
#     excitations=vqe_excitations,
#     qubit_converter=qubit_mapper,
#     reps=reps,
#     initial_state=initial_state,
#     preserve_spin= preserve_spin,
#     trott_order=1)

## Initial point
initial_point = [0]*len(var_form.excitation_list)

## Classical Optimizer ##
from qiskit import Aer
from qiskit_algorithms.optimizers import ISRES,ESCH,DIRECT_L,DIRECT_L_RAND, CRS, ADAM,SLSQP, SPSA,QNSPSA,COBYLA
# optimizer = ISRES(max_evals = optimizer_maxiter)
# optimizer = ESCH(max_evals = optimizer_maxiter)
# optimizer = DIRECT_L(max_evals=optimizer_maxiter)
# optimizer = CRS(max_evals=optimizer_maxiter)
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
    optimizer = SPSA(maxiter=optimizer_maxiter,termination_checker=TerminationChecker(N = 10, tol = optimizer_tol,), callback=SPSA_callback)
    initial_point = [0.1,0,0,0]
if optmz == "COBYLA":
    optimizer=COBYLA(maxiter=optimizer_maxiter, disp=True, tol = optimizer_tol)

# optimizer = ADAM(maxiter=optimizer_maxiter, tol=optimizer_tol)
# optimizer = SLSQP(maxiter=optimizer_maxiter, tol=optimizer_tol)
# optimizer = SPSA(maxiter=optimizer_maxiter)

# ### for QNSPSA
# from qiskit.primitives import Sampler
# sampler = Sampler()
# fidelity = QNSPSA.get_fidelity(var_form, sampler)
# optimizer = QNSPSA(fidelity,maxiter=optimizer_maxiter)

from estimators import esti_dic
if esti == None: 
    print(f"Please define the esti properly with the following: {esti_dic.keys()}")
else:
    pass_manager, estimator = esti_dic[esti]
