from calc_config import *

from qiskit_aer.backends import AerSimulator
from qiskit.primitives import BackendEstimator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

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

esti_fj_dic = {"esti_fj001" : (pass_man_fj001, esti_gpu_fj001),
               "esti_fj002" : (pass_man_fj002, esti_gpu_fj002),
               "esti_fj003" : (pass_man_fj003, esti_gpu_fj003),
               "esti_fj004" : (pass_man_fj004, esti_gpu_fj004),
               "esti_fj005" : (pass_man_fj005, esti_gpu_fj005),
               "esti_fj006" : (pass_man_fj005, esti_gpu_fj006),
               "esti_fj007" : (pass_man_fj005, esti_gpu_fj007),
               "esti_fj008" : (pass_man_fj005, esti_gpu_fj008),
               "esti_fj009" : (pass_man_fj005, esti_gpu_fj009),
               "esti_fj010" : (pass_man_fj005, esti_gpu_fj010),
               }