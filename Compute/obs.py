## The Hamiltonian
### Use the defined obs_twobody_df to construct the Hamiltonian
from qiskit_nature.second_q.operators import FermionicOp
from calc_config import *
import pandas as pd
from vqe import qubit_mapper

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
