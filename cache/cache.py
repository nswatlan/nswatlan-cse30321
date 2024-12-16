
import argparse
import csv
import time

def read_csv(filename): 
    data = []
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['valid'] = int(row['valid'])
            row['LRU'] = int(row['LRU'])
            data.append(row)
    return data

def print_cache(data): 
    #title
    print("--------------------------------------------------------------")
    print("| Index |  Tag  |    Word 0    |    Word 1    | Valid |  LRU  |")
    print("--------------------------------------------------------------")
    
    for entry in data:
        print(f'|   {entry['index']}  |  {entry['tag']} |     {entry['word1']}    |    {entry['word2']}   |   {entry['valid']}   |   {entry['LRU']}   |')
        print("--------------------------------------------------------------")


def sim_cache(data): 
    inputs = {}
    while(1): 
        print_rf(registers)
        print_cache(data)
        print("Enter an instruction: ")
        command = input()
        if command == 'done': 
            break
        commands = command.split()
        inputs['instr'] = commands[0]
        inputs['dest'] = commands[1]
        inputs['offset'] = commands[2]
        inputs['oper'] = commands[3]
        address = check_addr(inputs, registers)
        if inputs['instr'] == 'lw':
            lw(data, address)
        if inputs['instr'] == 'sw':
            sw(data, address, registers, inputs)

def lw(data, addr):
    index = addr[0][4:6]
    tag = addr[0][:4]
    offset = addr[0][6]
    slot = 0
    for entry in data: 
        if entry['index'] == index and entry['tag'] == tag: 
            if entry['valid'] == 1:
                print('Cache Hit!')
                if offset == '1':
                    print(f'Word retrieved: {entry['word2']}')
                    time.sleep(2)
                    update_LRU(data,slot)
                    #update register file
                if offset == '0':
                    print(f'Word retrieved: {entry['word1']}')
                    time.sleep(2)
                    #update register filed
                    update_LRU(data,slot)
        slot += 1

def sw(data, addr, registers,inputs): 
    index = addr[0][4:6]
    tag = addr[0][:4]
    offset = addr[0][6]
    slot = 0
    for entry in data: 
        if entry['index'] == index and entry['tag'] == tag: 
            if offset == '0':
                if entry['valid'] == 1 and entry['word1'] == addr[1]:
                    print('Cache Hit!')
                    print('No change in cache data.')
                    time.sleep(2)
                elif entry['valid'] == 1 and entry['word1'] != addr[1]:
                    print('Updating Cache...')
                    time.sleep(2)
                    entry['word1'] = registers[inputs['dest']][1]
                    entry['word2'] = registers[inputs['dest']][2]
            if offset == '1':
                if entry['valid'] == 1 and entry['word2'] == addr[2]:
                    print('Cache Hit!')
                    print('No change in cache data.')
                    update_LRU(data, slot)
                    entry['LRU'] = 3
                elif entry['valid'] == 1 and entry['word2'] != addr[2]:
                    print('Updating Cache...')
                    time.sleep(2)
                    entry['word1'] = registers[inputs['dest']][1]
                    entry['word2'] = registers[inputs['dest']][2]
                    update_LRU(data, slot)
                    entry['LRU'] = 3
                    
        '''elif entry['index'] != index and entry['tag'] != tag: 
            print('Cache Miss!')
            print('Checking LRU and Updating Cache...')
            time.sleep(2)'''
        slot += 1
    print_cache(data)


def update_LRU(data, slot): 
    for entry in data:  
        if entry['LRU'] != 0:
            entry['LRU'] = entry['LRU'] - 1
    data[slot]['LRU'] = 3


def check_addr(inputs, registers): 
    dest = inputs['dest']
    offset = inputs['offset']
    oper = inputs['oper']
    addr = registers[dest]
    return addr


def read_rf(filename): 
    registers = {}
    for line in open(filename).readlines():
        reg, val, w0, w1 = line.split()
        registers[reg] = [val, w0, w1]
    return registers

def print_rf(registers): 
    print('-----------------------------------------')
    print('|             Register File              |')
    print('-----------------------------------------')
    print('|  reg   |  addr   |   word 0  | word 1  |')
    print('-----------------------------------------')

    for reg, val in registers.items():
        print(f'|  {reg}   | {val[0]}  |  {val[1]}  |  {val[2]}  |')
        print('------------------------------------------')
    

if __name__ == "__main__": 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("cache", type=str)
    parser.add_argument("registers", type=str)
    args = parser.parse_args()

    data = read_csv(args.cache)
    registers = read_rf(args.registers)
    inputs = sim_cache(data)



    
    
