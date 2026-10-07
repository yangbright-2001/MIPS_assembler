import scan_label
from scan_label import test_file

register_dict = {
        '$zero':0,
        '$at':1,
        '$v0':2,
        '$v1':3,
        '$a0':4,
        '$a1':5,
        '$a2':6,
        '$a3':7,
        '$t0':8,
        '$t1':9,
        '$t2':10,
        '$t3':11,
        '$t4':12,
        '$t5':13,
        '$t6':14,
        '$t7':15,
        '$s0':16,
        '$s1':17,
        '$s2':18,
        '$s3':19,
        '$s4':20,
        '$s5':21,
        '$s6':22,
        '$s7':23,
        '$t8':24,
        '$t9':25,
        '$k0':26,
        '$k1':27,
        '$gp':28,
        '$sp':29,
        '$fp':30,
        '$ra':31,
}

op_code = { 'addi':'001000',
            'addiu':'001001',
            'andi':'001100',
            'beq':'000100',
            'bgez':'000001',
            'bgtz':'000111',
            'blez':'000110',
            'bltz':'000001',
            'bne' :'000101',
            'lb':'100000',
            'lbu':'100100',
            'lh':'100001',
            'lhu':'100101',
            'lui':'001111',
            'lw'  :'100011',
            'ori' :'001101',
            'sb':'101000',
            'slti':'001010',
            'sltiu':'001011',
            'sh':'101001',
            'sw'  :'101011',
            'xori':'001110',
            'lwl':'100010',
            'lwr':'100110',
            'swl':'101010',
            'swr':'101110',
            'j'   :'000010',
            'jal' :'000011' 
}

r_mips = [
    'add', 'addu','and','div','divu','jalr','jr','mfhi','mflo','mthi','mtlo','mult','multu',
    'nor','or','sll','sllv','slt','sltu','sra','srav','srl','srlv','sub','subu',
    'syscall','xor'
    ]

i_mips = [
    'addi','addiu','andi','beq','bgez','bgtz','blez','bltz','bne','lb','lbu','lh','lhu',
    'lui','lw','ori','sb','slti','sltiu','sh','sw','xori','lwl','lwr','swl','swr'
    ]

j_mips = ['j', 'jal']

all_mips = r_mips + i_mips + j_mips

#r-type转的时候永远都是 op,rs,rt,rd,shamp,func
r_list_1 = ['add','addu','and','nor','or','slt','sltu','sub','subu','xor'] #指令的三个寄存器对应rd,rs,rt
r_list_2 = ['sllv','srav','srlv']   #指令的三个值对应rd,rt,rs
r_list_3 = ['sll','sra','srl']  #指令的三个值对应rd,rt,shamt
r_list_4 = ['div','divu','mult','multu']     #指令的两个值对应rs,rt
r_list_5 = ['jalr']  #指令的两个值对应rd,rs
r_list_6 = ['jr','mthi','mtlo']  #指令的一个值对应rs
r_list_7 = ['mfhi','mflo']   #指令的一个值对应rd
r_list_8 = ['syscall']   #指令后面没有值了

r_function = {'add':'100000',
            'addu':'100001',
            'and':'100100',
            'div':'011010',
            'divu':'011011',
            'jalr':'001001',
            'jr' :'001000',
            'mfhi':'010000',
            'mflo':'010010',
            'mthi':'010001',
            'mtlo':'010011',
            'mult':'011000',
            'multu':'011001',
            'nor':'100111',
            'or' :'100101',
            'sll':'000000',
            'sllv':'000100',
            'slt':'101010',
            'sltu':'101011',
            'sra':'000011',
            'srav':'000111',
            'srl':'000010',
            'srlv':'000110',
            'sub':'100010',
            'subu':'100011',
            'syscall':'001100',
            'xor':'100110',
}

#i-type转的时候永远都是 rs,rt,immediate
i_list_1 = ['addi','addiu','andi','ori','slti','sltiu','xori']  #指令的三个值对应rt,rs,immediate
i_list_2 = ['beq','bne']    #指令的三个值对应rt,rs,immediate
i_list_3 = ['lb','lbu','lh','lhu','lw','sb','sh','sw','lwl','lwr','swl','swr']  #指令的两个值对应rt,immediate(rs)
i_list_4 = ['bgez','bgtz','blez','bltz']    #指令的两个值对应rs,label
i_list_5 = ['lui']  #指令的两个值对应rt,immediate

label_dict = scan_label.main_scan(test_file)  #完成第一次扫描记录label相对地址

def extend_bit(binary_num, width):    #延长数字使之达到规定长度,每个数字都延长一下吧
    if len(binary_num) < width:        #num是一个字符串型的二进制数
        complement_zero = '0' * (width - len(binary_num))
        binary_num = complement_zero + binary_num
    return binary_num

def process_register(line,sequence_list): #转二进制并延长至5位,参数是int
    register_code = ''                                  #sequence_list:为了打印出rs,rt,rd顺序应该怎么取line[i]
    for i in sequence_list:
        reg = register_dict[line[i]]
        reg = format(reg,'b')
        reg = extend_bit(reg,5)
        register_code = register_code + reg
    return register_code

def process_num(num,width): #输入是一个字符串型的十进制数字，把它转为对应长度的数
    if (int(num) < 0):
        num = format(abs(int(num)),'b')
        num = extend_bit(num,width)   #先延长再转为补码
        num_code = convert_2s_complement(num)
    else:
        num = format(int(num),'b')
        num_code = extend_bit(num,width)
    return num_code

def convert_2s_complement(num): #对象是二进制数字符串，这个数是对应的正数的二进制数，把整个二进制数转为补数
    num_list = list(num)
    for i in range((len(num_list) - 1),-1,-1):
        if (num_list[i] == '1'):
            break
    for j in range((i - 1), -1, -1):
        if (num_list[j] == '1'):
            num_list[j] = '0'
            continue
        elif (num_list[j] == '0'):
            num_list[j] = '1'
            continue            
    new_num = ''
    for i in range(len(num_list)):
        new_num = new_num + num_list[i]
    return new_num

#r-type转的时候永远都是 op,rs,rt,rd,shamp,func
def r_convert_12(line,sequence_list):  #处理r_list_1，r_list_2,line是一个list
    opcode = '000000'
    register_code = process_register(line,sequence_list)
    shamp = '00000'
    function_code = r_function[line[0]]
    machine_code = opcode + register_code + shamp + function_code
    return machine_code

def r_convert_3(line):
    opcode = '000000'
    rs = '00000'
    rt_rd = process_register(line,[2,1])
    register_code = rs + rt_rd
    shamp = process_num(line[3],5)
    function_code = r_function[line[0]]
    machine_code = opcode + register_code + shamp + function_code
    return machine_code

def r_convert_4(line):  #处理r_list_4,line是一个list
    opcode = '000000'
    rs_rt = process_register(line,[1,2])
    rd = '00000'
    register_code = rs_rt + rd
    shamp = '00000'
    function_code = r_function[line[0]]
    machine_code = opcode + register_code + shamp + function_code
    return machine_code

def r_convert_5(line):  #处理r_list_5,line是一个list
    opcode = '000000'
    rs = process_register(line,[2])
    rt = '00000'
    rd = process_register(line,[1])
    register_code = rs + rt + rd
    shamp = '00000'
    function_code = r_function[line[0]]
    machine_code = opcode + register_code + shamp + function_code
    return machine_code
    
def r_convert_6(line):  #处理r_list_6,line是一个list
    opcode = '000000'
    rs = process_register(line,[1])
    rt_rd = '0000000000'
    register_code = rs + rt_rd
    shamp = '00000'
    function_code = r_function[line[0]]
    machine_code = opcode + register_code + shamp + function_code
    return machine_code

def r_convert_7(line):  #处理r_list_7,line是一个list
    opcode = '000000'
    rd = process_register(line,[1])
    rs_rt = '0000000000'
    register_code = rs_rt + rd
    shamp = '00000'
    function_code = r_function[line[0]]
    machine_code = opcode + register_code + shamp + function_code
    return machine_code

def r_convert_8(line):  #处理r_list_8,line是一个list
    opcode = '000000'
    register_code = '000000000000000'
    shamp = '00000'
    function_code = r_function[line[0]]
    machine_code = opcode + register_code + shamp + function_code
    return machine_code

def convert_r(line):
    if (line[0] in r_list_1):
        machine_code = r_convert_12(line,[2,3,1])
    if (line[0] in r_list_2):
        machine_code = r_convert_12(line,[3,2,1])
    if (line[0]) in r_list_3:
        machine_code = r_convert_3(line)
    if (line[0]) in r_list_4:
        machine_code = r_convert_4(line)
    if (line[0]) in r_list_5:
        machine_code = r_convert_5(line)
    if (line[0]) in r_list_6:
        machine_code = r_convert_6(line)
    if (line[0]) in r_list_7:
        machine_code = r_convert_7(line)
    if (line[0]) in r_list_8:
        machine_code = r_convert_8(line)
    return machine_code

#i-type转的时候永远都是 op,rs,rt,immediate
def i_convert_1(line): #处理i_list_1
    opcode = op_code[line[0]]
    register_code = process_register(line,[2,1])
    immediate = process_num(line[3],16)
    machine_code = opcode + register_code + immediate
    return machine_code

def i_convert_2(line,address_index):    #处理i_list_2
    opcode = op_code[line[0]]
    register_code = process_register(line,[1,2])
    immediate_num = label_dict[line[3]] - address_index - 1
    immediate = process_num(str(immediate_num),16)
    machine_code = opcode + register_code + immediate
    return machine_code

def i_convert_3(line):  #处理i_list_3
    opcode = op_code[line[0]]
    left_index = line[2].find('(')
    right_index = line[2].find(')')
    immediate_num = line[2][:left_index]  #默认immediate和（rs）之间没有空格了
    rs_num = line[2][(left_index + 1) : right_index]
    opcode = op_code[line[0]]

    rs = register_dict[rs_num]
    rs = format(rs,'b')
    rs = extend_bit(rs,5)
    rt = process_register(line,[1])

    immediate = process_num(immediate_num,16)
    machine_code = opcode + rs + rt + immediate
    return machine_code

def i_convert_4(line,address_index):    #处理i_list_2
    opcode = op_code[line[0]]
    rs = process_register(line,[1])
    if line[0] == 'bgez':
        rt = '00001'
    else:
        rt = '00000'
    register_code = rs + rt
    immediate_num = label_dict[line[2]] - address_index - 1
    immediate = process_num(str(immediate_num),16)
    machine_code = opcode + register_code + immediate
    return machine_code

def i_convert_5(line):  #处理i_list_5
    opcode = op_code[line[0]]
    rs = '00000'
    rt = process_register(line,[1])
    immediate = process_num(line[2],16)
    machine_code = opcode + rs + rt + immediate
    return machine_code

def j_convert(line):
    opcode = op_code[line[0]]
    target_index = label_dict[line[1]]
    # target_num = format((int('100000',16) + address_index),"x")
    # target_num = int(target_num,16)
    target_num = int('100000',16) + target_index
    target = process_num(str(target_num),26)
    machine_code = opcode + target
    return machine_code

def convert_ij(line,address_index):
    if (line[0] in i_list_1):
        machine_code = i_convert_1(line)
    if (line[0] in i_list_2):
        machine_code = i_convert_2(line,address_index)
    if (line[0] in i_list_3):
        machine_code = i_convert_3(line)
    if (line[0] in i_list_4):
        machine_code = i_convert_4(line,address_index)
    if (line[0]) in i_list_5:
        machine_code = i_convert_5(line)
    if (line[0]) in j_mips:
        machine_code = j_convert(line)
    return machine_code

