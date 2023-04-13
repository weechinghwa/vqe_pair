from calc_config import *

## VQE Algorithm Setup ## 
# Define a converter aka mapping method
from qiskit_nature.second_q.mappers import JordanWignerMapper, QubitConverter
qubit_converter = QubitConverter(JordanWignerMapper())

# from qiskit_nature.second_q.circuit.library.initial_states import HartreeFock
from qiskit_nature.second_q.circuit.library.ansatzes import UCC
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
var_form = UCC(
    num_particles=num_particles,
    num_spatial_orbitals=num_spatial_orbitals,
    excitations=vqe_excitations,
    qubit_converter=qubit_converter,
    reps=reps,
    initial_state=initial_state)

## Optimizer setting
from qiskit.algorithms.optimizers import ISRES,COBYLA,SLSQP, SPSA
optimizer = SPSA(
    maxiter=optimizer_maxiter)
# optimizer=COBYLA(
#     maxiter=optimizer_maxiter,
#     disp=True, 
#     tol = optimizer_tol)

# Define Solver
vqe = VQE(
    estimator = estimator,
    ansatz = var_form,
    optimizer = optimizer)

adapt_vqe = AdaptVQE(
    vqe,
    threshold = 0.001,
    max_iterations = 200)
