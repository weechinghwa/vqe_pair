from calc_config import *

from qiskit_aer.backends import AerSimulator
from qiskit.primitives import BackendEstimator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Define Estimator
#A# Exact Evaluation (Estimator)
from qiskit.primitives import Estimator
## Primitives from qiskit
estimator_exact = Estimator()  # options={"shots":128}


#B# IBM's Fake Backends
from qiskit.primitives import BackendEstimator
from qiskit.providers.fake_provider import FakeGuadalupeV2, FakeKolkataV2, FakeHanoiV2, FakeSherbrooke, FakeGeneva
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

##### Alternative method of using statevector simulator follow the code on https://qiskit.org/ecosystem/algorithms/tutorials/03_vqe_simulation_with_noise.html#Performance-without-noise
##### ref https://quantumcomputing.stackexchange.com/questions/32667/what-are-the-differences-between-the-two-estimator-in-the-qiskit

## Alternative estimator 1: Fake guadalupe  **No GPU**
estimator_backend_fake = BackendEstimator(backend = FakeGuadalupeV2(),options={"shots":shots})

### with IBM quantum Backend (GPU accelerated)
from qiskit_aer.backends import AerSimulator
## Alternative estimator 2 FakeGuadalupeV2
backend2 = FakeGuadalupeV2()
pass_manager2 = generate_preset_pass_manager(3, backend2)
backend_gpu2 = AerSimulator.from_backend(backend2, method="automatic", device="GPU")
estimator_gpu2 = BackendEstimator(backend=backend_gpu2, options={"shots":shots},bound_pass_manager = pass_manager2)

## Alternative estimator 3 FakeKolkataV2
backend3 = FakeKolkataV2()
pass_manager3 = generate_preset_pass_manager(3, backend3)
backend_gpu3 = AerSimulator.from_backend(backend3, method="automatic", device="GPU")
estimator_gpu3 = BackendEstimator(backend=backend_gpu3, options={"shots":shots},bound_pass_manager = pass_manager3)

## Alternative estimator 4 FakeHanoiV2
backend4 = FakeHanoiV2()
pass_manager4 = generate_preset_pass_manager(3, backend4)
backend_gpu4 = AerSimulator.from_backend(backend4, method="automatic", device="GPU")
estimator_gpu4 = BackendEstimator(backend=backend_gpu4, options={"shots":shots},bound_pass_manager = pass_manager4)

## Alternative estimator 4______ FakeHanoiV2 NO GPU
estimator_cpu4 = BackendEstimator(backend=backend4, options={"shots":shots})

## Alternative estimator 5 FakeSherbooke 
backend5 = FakeSherbrooke()
pass_manager5 = generate_preset_pass_manager(3, backend5)
backend_gpu5 = AerSimulator.from_backend(backend5, method="automatic", device="GPU")
estimator_gpu5 = BackendEstimator(backend=backend_gpu5, options={"shots":shots},bound_pass_manager = pass_manager5)

## Alternative estimator 6 FakeGeneva 
backend6 = FakeGeneva()
pass_manager6 = generate_preset_pass_manager(3, backend6)
backend_gpu6 = AerSimulator.from_backend(backend6, method="automatic", device="GPU")
estimator_gpu6 = BackendEstimator(backend=backend_gpu6, options={"shots":shots},bound_pass_manager = pass_manager6)

## Alternative estimator 6______ FakeGeneva NO GPU
estimator_cpu6 = BackendEstimator(backend=backend6, options={"shots":shots})


# Fake Johors
# Sample code
# ## Alternative estimator Custom
# from FakeBackends.fake_johor_NAME import FakeJohorV2 as NAME
# backend_name = NAME(); backend_name_gpu = AerSimulator.from_backend(backend_name, method="automatic", device="GPU")
# pass_man_name = generate_preset_pass_manager(3, backend_name)
# esti_gpu_name= BackendEstimator(backend=backend_name_gpu, options={"shots":shots}, bound_pass_manager = pass_man_name)

from FakeBackends.fake_johor_FJ001 import FakeJohorV2 as FJ001
backend_fj001 = FJ001(); backend_fj001_gpu = AerSimulator.from_backend(backend_fj001, method="automatic", device="GPU")
pass_man_fj001 = generate_preset_pass_manager(3, backend_fj001)
esti_gpu_fj001= BackendEstimator(backend=backend_fj001_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj001)

from FakeBackends.fake_johor_FJ002 import FakeJohorV2 as FJ002
backend_fj002 = FJ002(); backend_fj002_gpu = AerSimulator.from_backend(backend_fj002, method="automatic", device="GPU")
pass_man_fj002 = generate_preset_pass_manager(3, backend_fj002)
esti_gpu_fj002= BackendEstimator(backend=backend_fj002_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj002)

from FakeBackends.fake_johor_FJ003 import FakeJohorV2 as FJ003
backend_fj003 = FJ003(); backend_fj003_gpu = AerSimulator.from_backend(backend_fj003, method="automatic", device="GPU")
pass_man_fj003 = generate_preset_pass_manager(3, backend_fj003)
esti_gpu_fj003= BackendEstimator(backend=backend_fj003_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj003)

from FakeBackends.fake_johor_FJ004 import FakeJohorV2 as FJ004
backend_fj004 = FJ004(); backend_fj004_gpu = AerSimulator.from_backend(backend_fj004, method="automatic", device="GPU")
pass_man_fj004 = generate_preset_pass_manager(3, backend_fj004)
esti_gpu_fj004= BackendEstimator(backend=backend_fj004_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj004)

from FakeBackends.fake_johor_FJ005 import FakeJohorV2 as FJ005
backend_fj005 = FJ005(); backend_fj005_gpu = AerSimulator.from_backend(backend_fj005, method="automatic", device="GPU")
pass_man_fj005 = generate_preset_pass_manager(3, backend_fj005)
esti_gpu_fj005= BackendEstimator(backend=backend_fj005_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj005)

from FakeBackends.fake_johor_FJ006 import FakeJohorV2 as FJ006
backend_fj006 = FJ006(); backend_fj006_gpu = AerSimulator.from_backend(backend_fj006, method="automatic", device="GPU")
pass_man_fj006 = generate_preset_pass_manager(3, backend_fj006)
esti_gpu_fj006= BackendEstimator(backend=backend_fj006_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj006)

from FakeBackends.fake_johor_FJ007 import FakeJohorV2 as FJ007
backend_fj007 = FJ007(); backend_fj007_gpu = AerSimulator.from_backend(backend_fj007, method="automatic", device="GPU")
pass_man_fj007 = generate_preset_pass_manager(3, backend_fj007)
esti_gpu_fj007= BackendEstimator(backend=backend_fj007_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj007)

from FakeBackends.fake_johor_FJ008 import FakeJohorV2 as FJ008
backend_fj008 = FJ008(); backend_fj008_gpu = AerSimulator.from_backend(backend_fj008, method="automatic", device="GPU")
pass_man_fj008 = generate_preset_pass_manager(3, backend_fj008)
esti_gpu_fj008= BackendEstimator(backend=backend_fj008_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj008)

from FakeBackends.fake_johor_FJ009 import FakeJohorV2 as FJ009
backend_fj009 = FJ009(); backend_fj009_gpu = AerSimulator.from_backend(backend_fj009, method="automatic", device="GPU")
pass_man_fj009 = generate_preset_pass_manager(3, backend_fj009)
esti_gpu_fj009= BackendEstimator(backend=backend_fj009_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj009)

from FakeBackends.fake_johor_FJ010 import FakeJohorV2 as FJ010
backend_fj010 = FJ010(); backend_fj010_gpu = AerSimulator.from_backend(backend_fj010, method="automatic", device="GPU")
pass_man_fj010 = generate_preset_pass_manager(3, backend_fj010)
esti_gpu_fj010= BackendEstimator(backend=backend_fj010_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj010)

from FakeBackends.fake_johor_FJ011 import FakeJohorV2 as FJ011
backend_fj011 = FJ011(); backend_fj011_gpu = AerSimulator.from_backend(backend_fj011, method="automatic", device="GPU")
pass_man_fj011 = generate_preset_pass_manager(3, backend_fj011)
esti_gpu_fj011= BackendEstimator(backend=backend_fj011_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj011)

from FakeBackends.fake_johor_FJ012 import FakeJohorV2 as FJ012
backend_fj012 = FJ012(); backend_fj012_gpu = AerSimulator.from_backend(backend_fj012, method="automatic", device="GPU")
pass_man_fj012 = generate_preset_pass_manager(3, backend_fj012)
esti_gpu_fj012= BackendEstimator(backend=backend_fj012_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj012)

from FakeBackends.fake_johor_FJ013 import FakeJohorV2 as FJ013
backend_fj013 = FJ013(); backend_fj013_gpu = AerSimulator.from_backend(backend_fj013, method="automatic", device="GPU")
pass_man_fj013 = generate_preset_pass_manager(3, backend_fj013)
esti_gpu_fj013= BackendEstimator(backend=backend_fj013_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj013)

from FakeBackends.fake_johor_FJ014 import FakeJohorV2 as FJ014
backend_fj014 = FJ014(); backend_fj014_gpu = AerSimulator.from_backend(backend_fj014, method="automatic", device="GPU")
pass_man_fj014 = generate_preset_pass_manager(3, backend_fj014)
esti_gpu_fj014= BackendEstimator(backend=backend_fj014_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj014)

from FakeBackends.fake_johor_FJ015 import FakeJohorV2 as FJ015
backend_fj015 = FJ015(); backend_fj015_gpu = AerSimulator.from_backend(backend_fj015, method="automatic", device="GPU")
pass_man_fj015 = generate_preset_pass_manager(3, backend_fj015)
esti_gpu_fj015= BackendEstimator(backend=backend_fj015_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj015)

from FakeBackends.fake_johor_FJ016 import FakeJohorV2 as FJ016
backend_fj016 = FJ016(); backend_fj016_gpu = AerSimulator.from_backend(backend_fj016, method="automatic", device="GPU")
pass_man_fj016 = generate_preset_pass_manager(3, backend_fj016)
esti_gpu_fj016= BackendEstimator(backend=backend_fj016_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj016)

from FakeBackends.fake_johor_FJ017 import FakeJohorV2 as FJ017
backend_fj017 = FJ017(); backend_fj017_gpu = AerSimulator.from_backend(backend_fj017, method="automatic", device="GPU")
pass_man_fj017 = generate_preset_pass_manager(3, backend_fj017)
esti_gpu_fj017= BackendEstimator(backend=backend_fj017_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj017)

from FakeBackends.fake_johor_FJ018 import FakeJohorV2 as FJ018
backend_fj018 = FJ018(); backend_fj018_gpu = AerSimulator.from_backend(backend_fj018, method="automatic", device="GPU")
pass_man_fj018 = generate_preset_pass_manager(3, backend_fj018)
esti_gpu_fj018= BackendEstimator(backend=backend_fj018_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj018)

from FakeBackends.fake_johor_FJ019 import FakeJohorV2 as FJ019
backend_fj019 = FJ019(); backend_fj019_gpu = AerSimulator.from_backend(backend_fj019, method="automatic", device="GPU")
pass_man_fj019 = generate_preset_pass_manager(3, backend_fj019)
esti_gpu_fj019= BackendEstimator(backend=backend_fj019_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj019)

from FakeBackends.fake_johor_FJ020 import FakeJohorV2 as FJ020
backend_fj020 = FJ020(); backend_fj020_gpu = AerSimulator.from_backend(backend_fj020, method="automatic", device="GPU")
pass_man_fj020 = generate_preset_pass_manager(3, backend_fj020)
esti_gpu_fj020= BackendEstimator(backend=backend_fj020_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj020)

from FakeBackends.fake_johor_FJ021 import FakeJohorV2 as FJ021
backend_fj021 = FJ021(); backend_fj021_gpu = AerSimulator.from_backend(backend_fj021, method="automatic", device="GPU")
pass_man_fj021 = generate_preset_pass_manager(3, backend_fj021)
esti_gpu_fj021= BackendEstimator(backend=backend_fj021_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj021)

from FakeBackends.fake_johor_FJ022 import FakeJohorV2 as FJ022
backend_fj022 = FJ022(); backend_fj022_gpu = AerSimulator.from_backend(backend_fj022, method="automatic", device="GPU")
pass_man_fj022 = generate_preset_pass_manager(3, backend_fj022)
esti_gpu_fj022= BackendEstimator(backend=backend_fj022_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj022)

from FakeBackends.fake_johor_FJ023 import FakeJohorV2 as FJ023
backend_fj023 = FJ023(); backend_fj023_gpu = AerSimulator.from_backend(backend_fj023, method="automatic", device="GPU")
pass_man_fj023 = generate_preset_pass_manager(3, backend_fj023)
esti_gpu_fj023= BackendEstimator(backend=backend_fj023_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj023)

from FakeBackends.fake_johor_FJ024 import FakeJohorV2 as FJ024
backend_fj024 = FJ024(); backend_fj024_gpu = AerSimulator.from_backend(backend_fj024, method="automatic", device="GPU")
pass_man_fj024 = generate_preset_pass_manager(3, backend_fj024)
esti_gpu_fj024= BackendEstimator(backend=backend_fj024_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj024)

from FakeBackends.fake_johor_FJ025 import FakeJohorV2 as FJ025
backend_fj025 = FJ025(); backend_fj025_gpu = AerSimulator.from_backend(backend_fj025, method="automatic", device="GPU")
pass_man_fj025 = generate_preset_pass_manager(3, backend_fj025)
esti_gpu_fj025= BackendEstimator(backend=backend_fj025_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj025)

from FakeBackends.fake_johor_FJ026 import FakeJohorV2 as FJ026
backend_fj026 = FJ026(); backend_fj026_gpu = AerSimulator.from_backend(backend_fj026, method="automatic", device="GPU")
pass_man_fj026 = generate_preset_pass_manager(3, backend_fj026)
esti_gpu_fj026= BackendEstimator(backend=backend_fj026_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj026)

from FakeBackends.fake_johor_FJ027 import FakeJohorV2 as FJ027
backend_fj027 = FJ027(); backend_fj027_gpu = AerSimulator.from_backend(backend_fj027, method="automatic", device="GPU")
pass_man_fj027 = generate_preset_pass_manager(3, backend_fj027)
esti_gpu_fj027= BackendEstimator(backend=backend_fj027_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj027)

from FakeBackends.fake_johor_FJ028 import FakeJohorV2 as FJ028
backend_fj028 = FJ028(); backend_fj028_gpu = AerSimulator.from_backend(backend_fj028, method="automatic", device="GPU")
pass_man_fj028 = generate_preset_pass_manager(3, backend_fj028)
esti_gpu_fj028= BackendEstimator(backend=backend_fj028_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj028)

from FakeBackends.fake_johor_FJ029 import FakeJohorV2 as FJ029
backend_fj029 = FJ029(); backend_fj029_gpu = AerSimulator.from_backend(backend_fj029, method="automatic", device="GPU")
pass_man_fj029 = generate_preset_pass_manager(3, backend_fj029)
esti_gpu_fj029= BackendEstimator(backend=backend_fj029_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj029)

from FakeBackends.fake_johor_FJ030 import FakeJohorV2 as FJ030
backend_fj030 = FJ030(); backend_fj030_gpu = AerSimulator.from_backend(backend_fj030, method="automatic", device="GPU")
pass_man_fj030 = generate_preset_pass_manager(3, backend_fj030)
esti_gpu_fj030= BackendEstimator(backend=backend_fj030_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj030)

from FakeBackends.fake_johor_FJ031 import FakeJohorV2 as FJ031
backend_fj031 = FJ031(); backend_fj031_gpu = AerSimulator.from_backend(backend_fj031, method="automatic", device="GPU")
pass_man_fj031 = generate_preset_pass_manager(3, backend_fj031)
esti_gpu_fj031 = BackendEstimator(backend=backend_fj031_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj031)

from FakeBackends.fake_johor_FJ032 import FakeJohorV2 as FJ032
backend_fj032 = FJ032(); backend_fj032_gpu = AerSimulator.from_backend(backend_fj032, method="automatic", device="GPU")
pass_man_fj032 = generate_preset_pass_manager(3, backend_fj032)
esti_gpu_fj032 = BackendEstimator(backend=backend_fj032_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj032)

from FakeBackends.fake_johor_FJ033 import FakeJohorV2 as FJ033
backend_fj033 = FJ033(); backend_fj033_gpu = AerSimulator.from_backend(backend_fj033, method="automatic", device="GPU")
pass_man_fj033 = generate_preset_pass_manager(3, backend_fj033)
esti_gpu_fj033 = BackendEstimator(backend=backend_fj033_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj033)

from FakeBackends.fake_johor_FJ034 import FakeJohorV2 as FJ034
backend_fj034 = FJ034(); backend_fj034_gpu = AerSimulator.from_backend(backend_fj034, method="automatic", device="GPU")
pass_man_fj034 = generate_preset_pass_manager(3, backend_fj034)
esti_gpu_fj034 = BackendEstimator(backend=backend_fj034_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj034)

from FakeBackends.fake_johor_FJ035 import FakeJohorV2 as FJ035
backend_fj035 = FJ035(); backend_fj035_gpu = AerSimulator.from_backend(backend_fj035, method="automatic", device="GPU")
pass_man_fj035 = generate_preset_pass_manager(3, backend_fj035)
esti_gpu_fj035 = BackendEstimator(backend=backend_fj035_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj035)

from FakeBackends.fake_johor_FJ036 import FakeJohorV2 as FJ036
backend_fj036 = FJ036(); backend_fj036_gpu = AerSimulator.from_backend(backend_fj036, method="automatic", device="GPU")
pass_man_fj036 = generate_preset_pass_manager(3, backend_fj036)
esti_gpu_fj036 = BackendEstimator(backend=backend_fj036_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj036)

from FakeBackends.fake_johor_FJ037 import FakeJohorV2 as FJ037
backend_fj037 = FJ037(); backend_fj037_gpu = AerSimulator.from_backend(backend_fj037, method="automatic", device="GPU")
pass_man_fj037 = generate_preset_pass_manager(3, backend_fj037)
esti_gpu_fj037 = BackendEstimator(backend=backend_fj037_gpu, options={"shots":shots}, bound_pass_manager = pass_man_fj037)

esti_dic = {"esti0": (None, estimator_exact),
            "esti1": (None, estimator_backend_fake),
            "esti2": (pass_manager2, estimator_gpu2),
            "esti3": (pass_manager3, estimator_gpu3),
            "esti4": (pass_manager4, estimator_gpu4),
            "esti4_cpu": (pass_manager4, estimator_cpu4),
            "esti5": (pass_manager5, estimator_gpu5),
            "esti6": (pass_manager6, estimator_gpu6),
            "esti6_cpu": (pass_manager6, estimator_cpu6),
            "esti_fj001" : (pass_man_fj001, esti_gpu_fj001), #  5.00E+05	1.00E-09
            "esti_fj002" : (pass_man_fj002, esti_gpu_fj002), #  5.00E+05	1.00E-08
            "esti_fj003" : (pass_man_fj003, esti_gpu_fj003), #  5.00E+05	1.00E-07
            "esti_fj004" : (pass_man_fj004, esti_gpu_fj004), #  5.00E+05	1.00E-06
            "esti_fj005" : (pass_man_fj005, esti_gpu_fj005), #  5.00E+05	1.00E-05
            "esti_fj006" : (pass_man_fj006, esti_gpu_fj006), #  5.00E+04	1.00E-06
            "esti_fj007" : (pass_man_fj007, esti_gpu_fj007), #  5.00E+03	1.00E-06
            "esti_fj008" : (pass_man_fj008, esti_gpu_fj008), #  2.50E+03	1.00E-06
            "esti_fj009" : (pass_man_fj009, esti_gpu_fj009), #  1.00E+03	1.00E-06
            "esti_fj010" : (pass_man_fj010, esti_gpu_fj010), #  5.00E+02	1.00E-06
            "esti_fj011" : (pass_man_fj011, esti_gpu_fj011), #  5.00E+01	1.00E-06
            "esti_fj012" : (pass_man_fj012, esti_gpu_fj012), #  5.00E+00	1.00E-06
            "esti_fj013" : (pass_man_fj013, esti_gpu_fj013), # 50	        1.00E-08
            "esti_fj014" : (pass_man_fj014, esti_gpu_fj014), # 50	        1.00E-07
            "esti_fj015" : (pass_man_fj015, esti_gpu_fj015), # 50	        1.00E-05
            "esti_fj016" : (pass_man_fj016, esti_gpu_fj016), # 5	        1.00E-08
            "esti_fj017" : (pass_man_fj017, esti_gpu_fj017), # 5	        1.00E-07
            "esti_fj018" : (pass_man_fj018, esti_gpu_fj018), # 5	        1.00E-05
            "esti_fj019" : (pass_man_fj019, esti_gpu_fj019), # 1	        1.00E-08
            "esti_fj020" : (pass_man_fj020, esti_gpu_fj020), # 1	        1.00E-07
            "esti_fj021" : (pass_man_fj021, esti_gpu_fj021), # 1	        1.00E-05
            "esti_fj022" : (pass_man_fj022, esti_gpu_fj022), # 0.5	        1.00E-08
            "esti_fj023" : (pass_man_fj023, esti_gpu_fj023), # 0.5	        1.00E-07
            "esti_fj024" : (pass_man_fj024, esti_gpu_fj024), # 0.5	        1.00E-05
            "esti_fj025" : (pass_man_fj025, esti_gpu_fj025), # 0.05	        1.00E-08
            "esti_fj026" : (pass_man_fj026, esti_gpu_fj026), # 0.05	        1.00E-07
            "esti_fj027" : (pass_man_fj027, esti_gpu_fj027), # 0.05	        1.00E-05
            "esti_fj028" : (pass_man_fj028, esti_gpu_fj028), # 0.005        1.00E-08
            "esti_fj029" : (pass_man_fj029, esti_gpu_fj029), # 0.005        1.00E-07
            "esti_fj030" : (pass_man_fj030, esti_gpu_fj030), # 0.005        1.00E-05
            "esti_fj031" : (pass_man_fj031, esti_gpu_fj031), # 500          1.00E-05
            "esti_fj032" : (pass_man_fj032, esti_gpu_fj032), # 50           1.00E-05
            "esti_fj033" : (pass_man_fj033, esti_gpu_fj033), # 5            1.00E-05
            "esti_fj034" : (pass_man_fj034, esti_gpu_fj034), # 1            1.00E-05
            "esti_fj035" : (pass_man_fj035, esti_gpu_fj035), # 0.5          1.00E-05
            "esti_fj036" : (pass_man_fj036, esti_gpu_fj036), # 0.05         1.00E-05
            "esti_fj037" : (pass_man_fj037, esti_gpu_fj037), # 0.005        1.00E-05
            }