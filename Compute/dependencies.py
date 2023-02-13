## Package used
import os
from pathlib import Path
import re
import pandas as pd
from fractions import Fraction
import numpy as np

### Functions used
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
    
    for counter, line in enumerate(text_whole):
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

def degenerate_pair_gen(num_nucleon_orbitals:"tuple")->"list":
    # num_nucleon_orbitals: (num_neut_orbitals, num_prot_orbitals)
    pair = []; quad=[]
    pair_list=[]; quad_list=[]
    neut_orbitals_list = list(range(0,num_nucleon_orbitals[0]))
    prot_orbitals_list = list(range(num_nucleon_orbitals[0], sum(num_nucleon_orbitals)))
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

def antipara_spin_pair_gen(obs_onebody_df:"pandas.DataFrames", num_nucleon_orbitals:"tuple")->"list":
    # Function that generate list of pair combinations that has spin, S=0 
    # obs_onebody_df is the source dataframe for single particle energy levels
    # num_nucleon_orbitals is tuple containing the number of neutron and proton
    spin_dict = {}
    pair_list = []
    for index, row in obs_onebody_df.iterrows():
        spin_dict[int(row['q_i'])] = int(row["spin"])
    neut_index_list = list(range(0,num_nucleon_orbitals[0])); prot_index_list = list(range(num_nucleon_orbitals[0],sum(num_nucleon_orbitals)))
    # Upgrade this to a class to show the number of Tz=1 and Tz=0
    ## Tz=1
    for (neut,prot) in zip(neut_index_list,prot_index_list):
        for (neut2,prot2) in zip(neut_index_list,prot_index_list):
            S_prot = spin_dict[prot] + spin_dict[prot2]
            S_neut = spin_dict[neut] + spin_dict[neut2]
            if S_prot == 0:
                pair_list.append((prot,prot2))
            if S_neut == 0:
                pair_list.append((neut,neut2))
    ## Tz=0 only
    for neut in neut_index_list:
        for prot in prot_index_list:
            S = spin_dict[neut] + spin_dict[prot]
            if S == 0 :
                pair_list.append((neut,prot))   ## the opposite (prot,neut) is ignored (not in the real file)
    pair_list.sort() ## rearranged to make it easy to read
    return pair_list

def HFground_pair_list(num_particles:"tuple",num_nucleon_orbitals:"tuple")->"list":
    neut_state_init = list(range(0,num_particles[0]))
    prot_state_init = list(range(num_nucleon_orbitals[0],num_nucleon_orbitals[0]+num_particles[1]))
    nucl_state_init = neut_state_init + prot_state_init
    pair_list = list(combinations(nucl_state_init,2))
    return pair_list

def sin_bod_if_list_gen(num_nucleon_orbitals_:"tuple")->"list":
    # a function that generates (init,fina) list, where init and fina are indeces of single level epsilon
    num_neut = num_nucleon_orbitals_[0] ; num_prot = num_nucleon_orbitals_[1]
    if_neut = list(combinations(range(0,num_neut),2))
    if_prot = list(combinations(range(num_neut,num_neut+num_prot),2))
    if_list = if_neut + if_prot
    return if_list