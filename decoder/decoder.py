

import argparse


def decoder(binary):
    opcode = binary[25:]
    if opcode == '0110011':
        type = 'R'
        rd = binary[19:24]
    if opcode == '0010011' or '0000011':
        type = 'I'
    if opcode == '0100011':
        type = 'S'
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
    print(opcode)
    print(type)

def display_format(): 
    print('------------------------------------------------------------')
    print('|   funct7   |  rs2  |  r1  | funct3 |    rd     |  opcode  |')
    print('------------------------------------------------------------')
    print('|      imm[11:0]     |  r1  | funct3 |    rd     |  opcode  |')
    print('------------------------------------------------------------')
    print('| imm[11:5]  |  rs2  |  r1  | funct3 | imm[4:0]  |  opcode  |')
    print('------------------------------------------------------------')
    print('|imm[12|10:5]|  rs2  |  r1  | funct3 |imm[4:1|11]|  opcode  |')
    print('------------------------------------------------------------')
    print('|            imm[31:12]              |    rd     |  opcode  |')
    print('------------------------------------------------------------')
    print('|         imm[20|10:1|11|19:12]      |    rd     |  opcode  |')
    print('------------------------------------------------------------')


if __name__ == "__main__": 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("encoding", type=str)
    args = parser.parse_args()
    display_format()
    decoder(args.encoding)


