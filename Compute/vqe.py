from calc_config import *

## Define callback function: to collect convergence information
counts = []; values = []
def store_intermediate_result(eval_count, parameters, mean, std):
    counts.append(eval_count)
    values.append(mean)


## VQE Algorithm Setup ## 
# Define a converter aka mapping method
from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitConverter
qubit_converter = QubitConverter(JordanWignerMapper())

# from qiskit_nature.second_q.circuit.library.initial_states import HartreeFock
from qiskit_nature.second_q.circuit.library.ansatzes import UCC
from ucc_trott import UCC as UCC_trott

# from qiskit.algorithms.optimizers import ISRES,COBYLA,SLSQP, SPSA
from qiskit.algorithms.minimum_eigensolvers import VQE, AdaptVQE
from qiskit import Aer

## Define Estimator
from qiskit.primitives import Estimator
estimator = Estimator()

## Reference state / Initial state
from np_hartreefock import * ## Import custom init state
initial_state = HartreeFock(
    num_orbitals = num_orbitals,
    num_particles = num_particles,
    qubit_converter = qubit_converter)

## Ansatz
reps=1
var_form = UCC_trott(
    num_particles=num_particles,
    num_spatial_orbitals=num_spatial_orbitals,
    excitations=vqe_excitations,
    qubit_converter=qubit_converter,
    reps=reps,
    initial_state=initial_state,
    trott_order=1)

## Optimizer setting
from qiskit.algorithms.optimizers import ISRES,COBYLA,SLSQP, SPSA
# optimizer = ISRES(
#     max_evals = optimizer_maxiter)
# optimizer = SPSA(
#     maxiter=optimizer_maxiter)
optimizer=COBYLA(
    maxiter=optimizer_maxiter,
    disp=True, 
    tol = optimizer_tol)

# Define Solver
vqe = VQE(
    estimator = estimator,
    ansatz = var_form,
    optimizer = optimizer,
    callback=store_intermediate_result)

adapt_vqe = AdaptVQE(
    vqe,
    threshold = grad_tol,
    max_iterations = grad_maxiter)
