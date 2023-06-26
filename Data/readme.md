Change of data code (230522)

501_Be8

"5" - Batch number.
"0" - Nucleus code; 0 is Be8; 1 is Be9; 2 is Be10
"1" - Represents different type of hamiltonian.

The index 500 is reserved for the source. 
Batch number can be traced back from the email Koh sent;

The following is renamed as: (as of 230522)
Be8_SIII_new   -> 	Be8_400
Be9_SIII_0508  -> 	Be9_410
Be10_SII_0418  -> 	Be10_420

|last index	|  Description					|
| -		| -						|
| 0		| Source file located in source file		|
| 1		| 1B:SPE; 2B:Taken as it is; and ij ji only	|
| 2		| 1B:Quasiparticle E; 2B:Taken as it is		|
| 3		| 1B:\Delta{if}; 2B:Taken as it is		|
| 4		| 1B:SPE; 2B:Hermitian				|
| 5		| 1B:SPE-E_fermi 2B: Taken as it is ijji. (qp)	|
| 6		| 1B:Valence only; 2B:Specify in data folder.	|
| 7		| 1B: None; 2B: pair,up transit; only neg; ijji	|
| 8		| 1B: None; 2B: pair,up transit; all		|

Log of the source:
230522 - Data previous than batch 4 is kept in source/Keep

~Batch6~
- 3 sets of Be8 data. will be labeled as 60a1 60b1 60c1
For the two body terms, the three files correspond to different selections of data:
a. include_all_2b file is explicit. This will give you the matrix elements including those non pair states.
b. limited_to_pair_states_all_values includes all the negative and positive values.
c. limited_to_pair_states_negative_values is the one you want to use first. It is only limited to states with negative vpair matrix elements.