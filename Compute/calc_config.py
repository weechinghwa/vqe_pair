## Source File input
input_txt = 'result_Be9.txt'

## Computation config
pcname = "Hpc" #or "Hlp" or Ypc"
quan_algo = "VQE"    ## (string)(VQE or adaptVQE)
# excitations = "dq"    ## (string)(s d t q or etc) (self defined, so if need to use q, write the functions myself)

iter_mode = True ## (Boolean)
optimizer_maxiter = 100
optimizer_tol = 0.00001

# grad_maxiter = 200
# grad_tol = 0.001





## Optimizer information
## MAybe include configuration of cobyla in the future (classical optimizer)
## REF https://www.geeksforgeeks.org/how-to-import-variables-from-another-file-in-python/



