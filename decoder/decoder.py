

import argparse


def decoder(binary):
    opcode = binary[25:]
    if opcode == '0110011':
        type = 'R'
        rd = binary[19:24]
        funct3 = binary[15:18]
        rs1 = binary[9:14]
        rs2 = binary[3:8]
        funct7 = binary[:3]
        rddec = int(rd,2)
        rs1dec = int(rs1, 2)
        rs2dec = int(rs2, 2)
        if funct3 == '000': 
            if funct7 == '000':
                instr = 'add'
            if funct7 == '010': 
                instr = 'sub'
        if funct3 == '100':
            instr = 'xor'
        if funct3 == '110':
            instr = 'or'
        if funct3 == '111':
            instr = 'and'
        print(f'{instr} x{rddec}, x{rs1dec}, x{rs2dec}')
    if opcode == '0010011' or opcode == '0000011':
        type = 'I'
        rd = binary[19:24]
        funct3 = binary[15:18]
        rs1 = binary[9:14]
        imm = binary[:8]
        funct7 = binary[:3]
        rddec = int(rd,2)
        rs1dec = int(rs1, 2)
        immdec = int(imm, 2)
        if funct3 == '000': 
            instr = 'addi'
        if funct3 == '100':
            instr = 'xori'
        if funct3 == '110':
            instr = 'ori'
        if funct3 == '111':
            instr = 'andi'
        if funct3 == '001':
            instr = 'slli'
        if funct3 == '101':
            instr = 'srli'
        print(f'{instr} x{rddec}, x{rs1dec}, x{rs2dec}')
    if opcode == '0100011':
        type = 'S'
        rd = binary[19:24]
        funct3 = binary[15:18]
        rs1 = binary[9:14]
        rs2 = binary[3:8]
        imm = binary[:3]
        rddec = int(rd,2)
        rs1dec = int(rs1, 2)
        immdec = int(rs2, 2)
        if funct3 == '000': 
            instr = 'lb'
        if funct3 == '100':
            instr = 'lbu'
        if funct3 == '110':
            instr = 'ori'
        if funct3 == '111':
            instr = 'andi'
        if funct3 == '001':
            instr = 'slli'
        if funct3 == '101':
            instr = 'srli'
        print(f'{instr} x{rddec}, x{rs1dec}, x{rs2dec}')
    if opcode == '1100011':
        type = 'B'
    if opcode == '1101111':
        type = 'J'
    if opcode == '1100111':
        type = 'I'
    if opcode == '0110111' or opcode == '0010111':
        type = 'U'
    if opcode == '1110011':
        type = 'I'
   


def display_format(): 
    print('-------------------------------------------------------------')
    print('|   funct7   |  rs2  |  r1  | funct3 |    rd     |  opcode  |')
    print('-------------------------------------------------------------')
    print('|      imm[11:0]     |  r1  | funct3 |    rd     |  opcode  |')
    print('-------------------------------------------------------------')
    print('| imm[11:5]  |  rs2  |  r1  | funct3 | imm[4:0]  |  opcode  |')
    print('-------------------------------------------------------------')
    print('|imm[12|10:5]|  rs2  |  r1  | funct3 |imm[4:1|11]|  opcode  |')
    print('-------------------------------------------------------------')
    print('|            imm[31:12]              |    rd     |  opcode  |')
    print('-------------------------------------------------------------')
    print('|         imm[20|10:1|11|19:12]      |    rd     |  opcode  |')
    print('-------------------------------------------------------------')


if __name__ == "__main__": 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("encoding", type=str)
    args = parser.parse_args()
    display_format()
    decoder(args.encoding)


