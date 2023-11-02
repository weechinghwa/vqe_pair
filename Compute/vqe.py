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
from qiskit.algorithms.optimizers import ISRES,ESCH,DIRECT_L,DIRECT_L_RAND, CRS, ADAM,SLSQP, SPSA,QNSPSA,COBYLA
# optimizer = ISRES(max_evals = optimizer_maxiter)
# optimizer = ESCH(max_evals = optimizer_maxiter)
# optimizer = DIRECT_L(max_evals=optimizer_maxiter)
# optimizer = CRS(max_evals=optimizer_maxiter)
if optmz == "DIRECT_L_RAND":
    optimizer = DIRECT_L_RAND(max_evals=optimizer_maxiter)
if optmz =="SPSA":
    optimizer = SPSA(maxiter=optimizer_maxiter,termination_checker=TerminationChecker(N = 10, tol = optimizer_tol,))
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

# Define Estimator
#A# Exact Evaluation (Estimator)
from qiskit.primitives import Estimator
estimator_exact = Estimator()  # options={"shots":128}

#B# IBM's Fake Backends
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeGuadalupeV2, FakeKolkataV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

## Alternative estimator 1 **No GPU**
estimator_backend_fake = BackendEstimator(backend = FakeGuadalupeV2(),options={"shots":shots})

### with IBM quantum Backend (GPU accelerated)
from qiskit_aer.backends import AerSimulator
## Alternative estimator 2 FakeGuadalupeV2
backend2 = FakeGuadalupeV2()
pass_manager2 = generate_preset_pass_manager(3, backend2)
backend_gpu2 = AerSimulator.from_backend(backend2, method="automatic", device="GPU")

estimator_gpu2 = BackendEstimator(backend=backend_gpu2, options={"shots":shots},bound_pass_manager = pass_manager2)

## Alternative estimator 3 FakeKolkataV2
backend3 = FakeKolkataV2()
pass_manager3 = generate_preset_pass_manager(3, backend3)
backend_gpu3 = AerSimulator.from_backend(backend3, method="automatic", device="GPU")

estimator_gpu3 = BackendEstimator(backend=backend_gpu3, options={"shots":shots},bound_pass_manager = pass_manager3)


## Alternative estimator 4 


### Estimator selection
if esti == "esti0":
    estimator = estimator_exact #backend_fake #estimator_exact
elif esti == "esti1":
    estimator = estimator_backend_fake #backend_fake #estimator_exact
elif esti == "esti2":
    estimator = estimator_gpu2
elif esti == "esti3":
    estimator = estimator_gpu3
elif esti == None: 
    print("Please define the esti properly")

