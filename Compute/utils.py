## Package used
import os
from pathlib import Path
import re
import pandas as pd
from fractions import Fraction
import numpy as np
from datetime import datetime
from itertools import combinations


## Functions used
def remove_line(energy_list:"list",line_pattern:'str')->"list":
    pattern_target = re.compile(line_pattern)
    for line in energy_list:
        if pattern_target.search(line) != None:
            energy_list.remove(line)
    return energy_list

def remove_character(the_string:'str', to_remove_char:'str')->'str':
    pattern_target = re.compile(to_remove_char)
    to_replace = list(to_remove_char)
    if pattern_target.search(the_string) != None:
        for char in to_replace:
            the_string = the_string.replace(char,"")
    return the_string

def identify_line(text_file:'str',pattern_start:'str', pattern_end:'str')->tuple:
    pat_start = re.compile(pattern_start)
    pat_end = re.compile(pattern_end)
    line_start_counter = []
    line_end_counter = []
    
    for counter, line in enumerate(text_file):
        if pat_start.search(line) != None:
            line_start_counter.append(counter)
        else:
            pass
        if pat_end.search(line):
            line_end_counter.append(counter)
        else:
            pass
    output_line_counter = line_start_counter + line_end_counter
    return output_line_counter

def degenerate_pair_gen(num_orbitals:"tuple")->"list":
    # num_orbitals: (num_neut_orbitals, num_prot_orbitals)
    pair = []; quad=[]
    pair_list=[]; quad_list=[]
    neut_orbitals_list = list(range(0,num_orbitals[0]))
    prot_orbitals_list = list(range(num_orbitals[0], sum(num_orbitals)))
    matching_lvl = min(len(neut_orbitals_list),len(prot_orbitals_list))
    for i in range(0,matching_lvl):
        if len(quad) < 4:
            quad.extend([neut_orbitals_list[i],prot_orbitals_list[i]])
        elif len(quad)==4:
            quad.sort(); quad_list.append((quad))
            quad = []; quad.extend([neut_orbitals_list[i],prot_orbitals_list[i]])
    if len(quad)==4:
        quad.sort(); quad_list.append(list(quad))
        quad = []; quad.extend([neut_orbitals_list[i],prot_orbitals_list[i]])
    for quad_dum in quad_list:
        pair_list = pair_list+list(combinations(quad_dum,2))
    orbital_list = neut_orbitals_list if len(neut_orbitals_list) > len(prot_orbitals_list) else prot_orbitals_list
    for index_for_list in range(matching_lvl,len(orbital_list)):
        i = orbital_list[index_for_list]
        if len(pair)==2:
            pair_list.append(tuple(pair))
            pair = []; pair.append(i)
        elif len(pair) < 2:
            pair.append(i)
    if len(pair)==2:
        pair_list.append(tuple(pair))
        pair = []; pair.append(i)
    pair_list.sort()
    return pair_list

def antipara_spin_pair_gen(obs_onebody_df:"pandas.DataFrames", num_orbitals:"tuple")->"list":
    # Function that generate list of pair combinations that has spin, S=0 
    # obs_onebody_df is the source dataframe for single particle energy levels
    # num_orbitals is tuple containing the number of neutron and proton
    spin_dict = {}
    pair_list = []
    for index, row in obs_onebody_df.iterrows():
        spin_dict[int(row['q_i'])] = int(row["spin"])
    neut_index_list = list(range(0,num_orbitals[0])); prot_index_list = list(range(num_orbitals[0],sum(num_orbitals)))
    # Upgrade this to a class to show the number of Tz=1 and Tz=0
    ## Tz=1
    for neut in neut_index_list:
        for neut2 in neut_index_list:
            S_neut = spin_dict[neut] + spin_dict[neut2]
            if S_neut == 0:
                pair_list.append((neut,neut2))
    for prot in prot_index_list:
        for prot2 in prot_index_list:
            S_prot = spin_dict[prot] + spin_dict[prot2]
            if S_prot == 0:
                pair_list.append((prot,prot2))
    ## Tz=0 only
    for neut in neut_index_list:
        for prot in prot_index_list:
            S = spin_dict[neut] + spin_dict[prot]
            if S == 0 :
                pair_list.append((neut,prot))   ## the opposite (prot,neut) is ignored (not in the real file)
    pair_list.sort() ## rearranged to make it easy to read
    pair_list
    return pair_list

def HFground_pair_list(num_particles:"tuple",num_orbitals:"tuple")->"list":
    neut_state_init = list(range(0,num_particles[0]))
    prot_state_init = list(range(num_orbitals[0],num_orbitals[0]+num_particles[1]))
    nucl_state_init = neut_state_init + prot_state_init
    pair_list = list(combinations(nucl_state_init,2))
    return pair_list

def sin_bod_if_list_gen(num_orbitals:"tuple")->"list":
    # a function that generates (init,fina) list, where init and fina are indeces of single level epsilon
    num_neut = num_orbitals[0] ; num_prot = num_orbitals[1]
    if_neut = list(combinations(range(0,num_neut),2))
    if_prot = list(combinations(range(num_neut,num_neut+num_prot),2))
    if_list = if_neut + if_prot
    return if_list

def extract_number(file:'str')->"int":
    phrase_interest = re.findall("\D\D\D_\d+",file)[0] # to ensure the phrase match XXX_NNN whr XXX is string for pcname, and NNN is the code of calculation
    s = re.findall("\d+",phrase_interest)[0]
    return (int(s) if s else -1,file)

def pathfilename_gen(pcname_:"str", input_dir_:"str")->"str , str , dict":
    ## Setting up the path (now is directory where compute.py is ran)
    current_path = os.getcwd()                     # Current path(which is the Compute dir)
    try:
        abs_main                                   # Check if the abs_main was defined before
    except:
        abs_main = os.path.dirname(current_path)   # Main directory containing the compute dir
    os.chdir(abs_main)                             # Change dir to main dir(so called absolute main directory)

    abspath_data_dir = os.path.join(abs_main,"Data")
    abspath_result_dir = os.path.join(abs_main,"Result")
    
    #### Extract index for next dir and filename
    rel_path_result = os.path.relpath("Result",abs_main)
    rel_PATH_result = (Path(rel_path_result))
    subresult_dir_list = [str(x) for x in rel_PATH_result.iterdir() if x.is_dir()]
    if len(subresult_dir_list) == 0:
        new_index = 1
    else:
        latest_result_dir = (max(subresult_dir_list,key=extract_number))
        new_index = extract_number(latest_result_dir)[0]+1
    
    #### Create a new directory to keep new results
    ##### Extract neucleus name
    input_dir_dum = re.split('-|_|\\.', input_dir_)
    nucleus_name = input_dir_dum[1]
    output_id = pcname_ + "_" + "{:03d}".format(new_index) + "_"    ### When the index reaches 999, add A to expand.
    subresult_dir_name = os.path.join(rel_path_result,output_id+nucleus_name)
    os.mkdir(subresult_dir_name)
    subresult_dir = os.path.join(subresult_dir_name,output_id+nucleus_name)
    ### Using a dictionary to store the file names to be used
    pathfilename = {}
    #### Input filenames or path
    pathfilename["source_dir"] = os.path.join(abspath_data_dir, input_dir_)
    #### Output # only ready to be input as fermionic op is considered not source
    pathfilename["output_1B-source_csv"] =  subresult_dir + "-1B-source.csv"
    pathfilename["output_2B-source_csv"] =  subresult_dir + "-2B-source.csv"
    pathfilename["output_1B-H_input_csv"] = subresult_dir + "-1B-H_input.csv"
    pathfilename["output_2B-H_input_csv"] = subresult_dir + "-2B-H_input.csv"
    pathfilename["abstract_result"] = subresult_dir + "-vqe_abst.txt"
    pathfilename["full_result"] = subresult_dir + "-vqe_full.txt"
    pathfilename["conver_png"] = subresult_dir + "-converge.png"
    pathfilename["callback"] = subresult_dir + "-callback.csv"
    pathfilename["circuit"] = subresult_dir + "circuit.txt"
    pathfilename["output_id"] = output_id
    pathfilename["SPSA_lr_perturb"] = subresult_dir + "-lr_perturb.csv"
    pathfilename["subresult_dir"] = subresult_dir
    return abs_main, nucleus_name, pathfilename

class TerminateThreeStep:

    def __init__(self, N : int, tol :float ):
        self.N = N
        self.tol = tol
        self.values = []
        self.collected = []

    def __call__(self, nfev, parameters, value, stepsize, accepted) -> bool:
        self.values.append(value)
        self.collected.append((nfev, parameters, value, stepsize, accepted))
        if len(self.values) > self.N:
            if ((abs(self.values[-1] - self.values[-2]) < self.tol) and
                (abs(self.values[-2] - self.values[-3]) < self.tol)): # 2 steps to confirm termination
                return True
        return False

class TerminatePovSlope:
 
    def __init__(self, N : int):
        self.N = N
        self.values = []
        self.collected = []
 
    def __call__(self, nfev, parameters, value, stepsize, accepted) -> bool:
        self.values.append(value)
        self.collected.append((nfev, parameters, value, stepsize, accepted))
        if len(self.values) > self.N:
            last_values = self.values[-self.N:]
            pp = np.polyfit(range(self.N), last_values, 1)
            slope = pp[0] / self.N
 
            if slope > 0:
                return True
        return False

class TerminateThreeSMA:
 
    def __init__(self, N : int, tol :float ):
        self.N = N
        self.tol = tol
        self.values = []
        self.collected = []
 
    def __call__(self, nfev, parameters, value, stepsize, accepted) -> bool:
        self.values.append(value)
        self.collected.append((nfev, parameters, value, stepsize, accepted))
        if len(self.values) > self.N + 3:
            sma_l1 = self.sma(values=self.values, step_num=-1, period=self.N)
            sma_l2 = self.sma(values=self.values, step_num=-2, period=self.N)
            sma_l3 = self.sma(values=self.values, step_num=-3, period=self.N)
 
            if ((abs(sma_l2 - sma_l1) < self.tol) and
                (abs(sma_l3 - sma_l2) < self.tol)):
                return True
        return False
    
    def sma(self, values: list, step_num : int, period : int):
        mv_list = values[-(period - step_num - 1) : len(values) + step_num + 1 ]
        sma_val = sum(mv_list)/period
        return sma_val
## ORIginal excitations function
# def custom_excitation_list(num_spatial_orbitals: int,
#                            num_particles: tuple[int, int]):
# #### EDIT HERE
#     my_excitation_list = [((0, 1), (2, 3)), ((0, 1), (4, 5)), ((6, 7), (8, 9)), ((6, 7), (10, 11))]
#     return my_excitation_list
# excitations = custom_excitation_list