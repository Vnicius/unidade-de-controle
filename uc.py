 #!/usr/bin/python
 #-*- coding: utf-8-*-

import re

class ControlUnit():
    def __init__(self,mem_data,mem_instr):
        self.mem_data = mem_data    #Memória de dados
        self.mem_instr = mem_instr       #Memória de instruções
        self.reg = [0] * 4       #Array de registradores
        self.ir = ""     #Armazena a instrução atual
        self.pc = 0      #Armazena o endereço da próxima instrução
        self.flags = [False] * 4      #Flags condicionais

    def add_mem_instr(self,instr):
        self.mem_instr.append(instr)

    def fetch(self):
        self.ir = self.mem_instr[self.pc]
        self.pc += 1

    def decode_exec(self):
        instr = self.ir.split(" ")  #Divide a instrução
        op = instr[0].upper()       #Pega a operação da instrução

        if (op == "ADD") or (op == "SUB") or (op == "DIV") or (op == "MULT"):   #Casos seja uma operação aritmética
            self.arithmetic(op,instr[1:])
        elif op == "STORE":
            self.store(instr[1:])
        elif op == "LOAD":
            self.load(instr[1:])


    def arithmetic(self,operation,data):
        data = ''.join(data).replace(" ",'')    #Transforma o array data em string e retira os espaços
        operands = data.split(",")      #Separa os operandos
        op1 = op2 = 0       #Variaveis para guardar os dois operandos da operação

        reg_result = int(operands[0][1])    #Guarda o indíce do registrador de saída

        if "R" in operands[1].upper():      #Confere se é um registrador
            op1 = self.reg[int(operands[1][1])]     #Pega apenas o número do registrador
        elif "MD" in operands[1].upper():   #Confere se é um acesso à memória
            op1 = self.mem_data[int(re.sub(r'[^\d]','',operands[1].upper()))]   #Pega apenas o endereço da memória
        else:
            op1 = int(operands[1])      #Caso seja um número

        if "R" in operands[2].upper():
            op2 = self.reg[int(operands[2][1])]
        elif "MD" in operands[2].upper():
            op2 = self.mem_data[int(re.sub(r'[^\d]','',operands[2].upper()))]
        else:
            op2 = int(operands[2])

        if operation == "ADD":
            self.reg[reg_result] = op1 + op2
        elif operation == "SUB":
            self.reg[reg_result] = op1 - op2
        elif operation == "MULT":
            self.reg[reg_result] = op1 * op2
        elif operation == "DIV":
            self.reg[reg_result] = int(op1 / op2)

        #print (self.reg[reg_result])

    def store(self,data):
        """Recebe um endereço da memória e o dado que será armazenado nele"""
        data = ''.join(data).replace(" ",'')    #Transforma o array data em string e retira os espaços
        operands = data.split(',')
        value = 0

        mem_endr = int(re.sub(r'[^\d]','',operands[0].upper()))     #Endereço na memória

        if "R" in operands[1].upper():      #Confere se é um registrador
            value = self.reg[int(operands[1][1])]
        else:
            value = int(operands[1])

        self.mem_data[mem_endr] = value     #Armazena o dado no endereço da memória


    def load(self,data):
        '''Armazena dados da memória de dados (ou valores) no registrador indicado'''
        data = ''.join(data).replace(" ",'')    #Transforma o array data em string e retira os espaços
        operands = data.split(',')
        value = -1

        reg_result = int(operands[0][1])

        if "MD" in operands[1].upper():   #Confere se é um acesso à memória
            value = self.mem_data[int(re.sub(r'[^\d]','',operands[1].upper()))]   #Pega apenas o endereço da memória
        else:
            value = int(operands[1])      #Caso seja um número

        self.reg[reg_result] = value

    def __str__(self):
        return ("\nIR: "+self.ir+"\nMem_data: "+str(self.mem_data)+"\nReg: "+str(self.reg)+"\nPC: "+str(self.pc)+"\nFlags: "+str(self.flags))

#########################

mem_data = [0] * 10
mem_instr = []

name = "prog.txt"
#name = input("Arquivo: ")
file = open(name,"r")

uc = ControlUnit(mem_data,mem_instr)

for line in file.readlines():
    if line is not "\s":
        uc.add_mem_instr(line.replace("\n",""))
file.close()

i = 0
tam = len(uc.mem_instr)

while i < tam:
    uc.fetch()
    uc.decode_exec()
    i += 1
    print(uc)
    input()
