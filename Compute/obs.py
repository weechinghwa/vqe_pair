## The Hamiltonian
### Use the defined obs_twobody_df to construct the Hamiltonian
from qiskit_nature.second_q.operators import FermionicOp
from calc_config import *
import pandas as pd
from vqe import qubit_mapper
import numpy as np
from qiskit.quantum_info.operators import SparsePauliOp

## Data Loading
obs_twobody_df = pd.read_csv(obs_twobody_csv) if include_twobody == True else []
obs_onebody_df = pd.read_csv(obs_onebody_csv) if include_onebody == True else []

### One body Terms: Single particle energy levels
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

## Prepping Hamiltonian to be computed. Mapping. ## 
Hamiltonian_fermop_len = len(Hamiltonian)
Hamiltonian = qubit_mapper.map(Hamiltonian)

# Define observable to minimize (obs_to_minimize)
## Add a constant term to the Hamiltonian
sp_energies = obs_onebody_df["epsilon"].to_list()
E_sum_sp = sum(sp_energies[0:num_particles[0]] + sp_energies[num_orbitals[0]:num_orbitals[0]+num_particles[1]])
Identity_string = "I"*num_spin_orbitals
constant_term = SparsePauliOp(Identity_string, coeffs=np.array([-round(E_sum_sp,6)]))
obs_to_minimize = SparsePauliOp.sum([Hamiltonian, constant_term])

obs_to_minimize = Hamiltonian