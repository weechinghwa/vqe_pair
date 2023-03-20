## Source File input
input_txt = 'result_Be10.txt'

## Computation config
pcname = "Hpc" #or "Hlp" or Ypc"
quan_algo = "VQE"    ## (string)(VQE or adaptVQE)
# excitations = "dq"    ## (string)(s d t q or etc) (self defined, so if need to use q, write the functions myself)

iter_mode = True ## (Boolean)

## Optimizer setting

optimizer_maxiter = 300
optimizer_tol = 0.00001


# Define classical optimizer
from qiskit.algorithms.optimizers import ISRES,COBYLA,SLSQP, SPSA
optimizer = SPSA(
    maxiter=optimizer_maxiter
    )
# optimizer=COBYLA(
#     maxiter=optimizer_maxiter,
#     disp=True, 
#     tol = optimizer_tol)



# grad_maxiter = 200
# grad_tol = 0.001


## Optimizer information
## MAybe include configuration of cobyla in the future (classical optimizer)
## REF https://www.geeksforgeeks.org/how-to-import-variables-from-another-file-in-python/



