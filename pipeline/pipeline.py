#This program simulates an out-of-order pipeline
import argparse
import time
import os

def read_instr(filename):
    instr = {}
    count = 0
    lines = []
    for line in open(filename).readlines(): 
        lines.append(line.rstrip())
        if line.split()[0] != 'L:':
            ins, dest, oper1, oper2 = line.split()
            instr[count] = [ins, dest, oper1, oper2]
        elif line.split()[0] == 'L:':
            label = line.split()
            instr[count] = label
        count += 1
    return instr, lines
        
def read_reg(filename): 
    reg_map = {}
    for line in open(filename).readlines(): 
        reg, t = line.split()
        reg_map[reg] = t
    return reg_map

def read_free(filename):
    free_list = []
    for line in open(filename).readlines():
        t = line.split()[0]
        free_list.append(t)
    return free_list

def reorder_buffer(data, in_order):
    print('----------------------')
    print('|   Reorder Buffer    |')
    print('----------------------')
    for i in range(len(in_order)):
        print(f'|    {in_order[i]}          |')
        print('----------------------')

def register_map(reg_map):
    print('-----------------------')
    print('|    Register Map     |')
    print('-----------------------')
    for reg, t in reg_map.items():
        print(f'|   {reg}   |    {t}    |')
        print('-----------------------')

def free_list(free_list):
    print(f' Free List: {[free_list[i] for i in range(len(free_list))]}')

def pipe_trace(data, freelist, regmap, in_order, lines): 
    
    print('-------------------------------------------------------------------------------------------')
    print('|                                       Pipe Trace                                        |')
    print('-------------------------------------------------------------------------------------------')
    print('|    Instruction    | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |')
    print('-------------------------------------------------------------------------------------------')

    for i in range(len(data)):
        if rename_trace(data, freelist, reg_map, in_order, lines, i) is not None:
            instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i)
        if instr == 'branch':
            pass
        else: 
            if instr == 'sw' or instr == 'lw':
                print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
            elif oper2 == 'L':
                print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
            else: 
                print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
        
            print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    fetch = 'F'
    decode = 'D'
    issue = 'I'
    reservation = 'IR'
    execute = 'E'
    writeback = 'W'
    commit = 'C'
    register_map(reg_map)
    print_header()

    i = 0
    #CC 0
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} |   |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} |   |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 1
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   | {fetch} |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} |   |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')

    #CC 2
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} | {issue} |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} | {issue} |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   | {fetch} | {decode} |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   | {fetch} |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   | {fetch} |   |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 3
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}  | {fetch} | {decode} | {issue} | {execute} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} | {issue} | {execute} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   | {fetch} | {decode} | {issue} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   | {fetch} | {decode} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   | {fetch} | {decode} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   | {fetch} |   |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 4
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}  | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   | {fetch} | {decode} | {issue} | {execute} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   | {fetch} | {decode} | {issue} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   | {fetch} | {decode} | {issue} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   | {fetch} | {decode} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   |   | {fetch} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   |   | {fetch} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 5
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}  | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |   |   |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   | {fetch} | {decode} | {issue} | {execute} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   | {fetch} | {decode} | {issue} | {execute} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} | {issue} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   | {fetch} | {decode} | {issue} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   |   | {fetch} | {decode} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   |   | {fetch} | {decode} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+11)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   |   | {fetch} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+12)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   |   | {fetch} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 6
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}  | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}   | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   |   | {fetch} | {decode} | {issue} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}  |   |   |   |   | {fetch} | {decode} | {issue} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+11)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   |   | {fetch} | {decode} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+12)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   |   | {fetch} | {decode} |   |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    #CC 7
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}     |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+11)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   |   | {fetch} | {decode} | {issue} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+12)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   |   | {fetch} | {decode} | {issue} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
   #CC 8
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}     |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+11)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+12)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 9
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}     |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+11)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+12)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 10
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}     |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |    |    |    |    |    |    |')
    freelist.append(dest)
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+11)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+12)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    os.system('clear')
    #CC 11
    register_map(reg_map)
    print_header()
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {commit} |  |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+1)
    print(f'|  {instr} {dest} {oper1} {oper2}    | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i+2)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+3)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+4)
    print(f'|  {instr} {dest} {oper1} {oper2}     |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+5)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+6)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   | {fetch} | {decode} | {issue} | {execute} | {commit} |   |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+7)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |   |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+9)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |    |    |    |    |    |    |')
    print('-------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+10)
    print(f'|  {instr} {dest} {oper1} {oper2}   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit} |    |    |    |    |    |    |')
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+11)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {writeback} | {commit}  |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, regmap, in_order, lines, i+12)
    print(f'|  {instr} {dest} {oper1} {oper2}    |   |   |   |   |   | {fetch} | {decode} | {issue} | {execute} | {commit} |    |    |    |    |    |    |')
    freelist.append(dest)
    print('--------------------------------------------------------------------------------------------')
    print('Updated Free List: ', freelist)
    time.sleep(2)
    

def print_header():
    print('--------------------------------------------------------------------------------------------')
    print('|                                       Pipe Trace                                         |')
    print('--------------------------------------------------------------------------------------------')
    print('|    Instruction     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |')
    print('--------------------------------------------------------------------------------------------')
    

def rename_trace(data, freelist, regmap, in_order, lines, i):
    if i > 12:
        return 'end', 'end','end','end', 'end'
    if data[i][0] == 'L:': 
        branch_index = i
        dest = 'branch'
        instr = 'branch'
        oper1 = 'branch'
        oper2 = 'branch'
    
    else: 
        instr = data[i][0]
        dest = data[i][1]
        oper1 = data[i][2]
        oper2 = data[i][3]
    #rename registers
    dest = freelist[0]
    try: 
        if instr == 'L':
            pass
            instr = 'branch'
    except: ValueError
    try: 
        if instr == 'sw' or instr == 'lw':
            oper2 = regmap[oper2]
        else: 
            oper1 = regmap[oper1]
            oper2 = regmap[oper2]
    except: KeyError
    freelist.remove(freelist[0])
    branch_index = 0
    return instr, dest, oper1, oper2, branch_index

        
        


if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("instructions", type=str)
    parser.add_argument("registermap", type=str)
    parser.add_argument("freelist", type=str)
    args = parser.parse_args()

    data, lines = read_instr(args.instructions)
    in_order = []
    reg_map = read_reg(args.registermap)
    print(reg_map)
    freelist = read_free(args.freelist)
    reorder_buffer(data, in_order)
    register_map(reg_map)
    free_list(freelist)
    pipe_trace(data,freelist,reg_map,in_order, lines)
    try: 
        for i in range(len(data)):
            instr, dest, oper1, oper2, branch_index = rename_trace(data, freelist, reg_map, in_order, lines, i)
    except: TypeError