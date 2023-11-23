# Information for 2121_He6
Nucleus     :   He6
Onebody     :   SPE
Twobody     :   strictly ijkl where i<j, k>l, j>=k
Description :   With Helium Core
                Twobody = (4,2) in (6,6)
                two_factor is 0.5; (antisymmetrized TBME)
                Seniority force -Gq/(11+Nq); Nq neutron = 4, Nq proton = 2, Gq = 1
                source file = He6_2100(only onebody uses that): results from SLy4 HF-para
                
                Section of the calculation, not all available orbitals are included, only 0123 and 6789 from 2121_He6_herm_1 are included. 

                231123 - num_spatial_orbitals must be larger than the number of particles in of any kind. 
                So only still include all the qubits, only removes the matrix elements, and the excitation operator.

                Aim is to decrease the circuit depth.