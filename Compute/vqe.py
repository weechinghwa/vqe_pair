from calc_config import *

## Define callback function: to collect convergence information
counts = []; values = []
def store_intermediate_result(eval_count, parameters, mean, std):
    counts.append(eval_count)
    values.append(mean)


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


## Classical Optimizer ##
from qiskit import Aer
from qiskit.algorithms.optimizers import ISRES,COBYLA,SLSQP, SPSA
# optimizer = ISRES(
#     max_evals = optimizer_maxiter)
# optimizer = SPSA(
#     maxiter=optimizer_maxiter)
optimizer=COBYLA(
    maxiter=optimizer_maxiter,
    disp=True, 
    tol = optimizer_tol)


## Define Estimator
from qiskit.primitives import Estimator
estimator_exact = Estimator()  # options={"shots":128}

## Alternative estimator 1
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeGuadalupe
estimator_backend_fake = BackendEstimator(backend = FakeGuadalupe())

## Alternative estimator 2
from qiskit_aer.noise import NoiseModel


### Estimator selection
estimator = estimator_exact

# Define Solver
from qiskit.algorithms.minimum_eigensolvers import VQE, AdaptVQE
vqe = VQE(
    estimator = estimator,
    ansatz = var_form,
    optimizer = optimizer,
    callback=store_intermediate_result)

adapt_vqe = AdaptVQE(
    vqe,
    threshold = grad_tol,
    max_iterations = grad_maxiter)
