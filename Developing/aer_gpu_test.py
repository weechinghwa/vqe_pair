from qiskit import *
from qiskit.circuit.library import *
from qiskit.providers.aer import *
import sys

sim = AerSimulator(method='statevector')
sim_gpu = AerSimulator(method='statevector', device='GPU')

shots = 10
depth= 10
qubits = 25
block_bits = 25

circuit = transpile(QuantumVolume(qubits, depth, seed=0),
                    backend=sim,
                    optimization_level=0)
circuit.measure_all()

result_base = execute(circuit,sim,shots=shots,seed_simulator=12345).result()

#print(result_base)
#if result_base.to_dict()['metadata']['mpi_rank'] == 0:
print(result_base.to_dict()['backend_name'])
print(result_base.to_dict()['results'][0]['time_taken'])
print(sorted(result_base.to_dict()['results'][0]['data']['counts'].items(),key=lambda x:x[0]))

result_gpu = execute(circuit,sim_gpu,shots=shots,seed_simulator=12345,blocking_qubits=block_bits, cuStateVec_enable=True).result()

#print(result_gpu)
#if result_gpu.to_dict()['metadata']['mpi_rank'] == 0:
print(result_gpu.to_dict()['backend_name'])
print(result_gpu.to_dict()['results'][0]['time_taken'])
print(sorted(result_gpu.to_dict()['results'][0]['data']['counts'].items(),key=lambda x:x[0]))