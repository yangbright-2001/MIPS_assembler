import os

# import pandas as pd   #如果老师的电脑里面有pandas，可以运行这个


test_file=input("Please enter the test file name:")
while not os.path.exists(test_file):
    test_file=input("Your input of test file is wrong, please enter the correct name:")

data_list = []
label_dict = dict()

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

def discard_comment(line):  #去掉在代码右侧的comment
    if "#" in line:  #line是一个string
        line = line[:line.find('#')]
    return line

#生成数据结构储存.data，形如 str1: .asciiz "hello world!\n"， str1是名字，.asciiz是数据类型，"hello world!\n"是内容
#因为不知道老师的电脑里面带不带panda模块，所以.data数据就暂时以二维的list的形式记录下来
#本意是希望用pandas数据框架来存这部分数据的，但为防止运行时因缺少pandas包而报错，还是暂时先用list存一下data数据吧，这个二维列表中每一个元素（其实它也是一个list）对应一行数据
def construct_dataframe(df):
    #把.data的数据存在一个dataframe里面，如果老师的python有pandas，就可以运行下面这段语句  
    # df = pd.DataFrame(data_list,columns=['data_name','data_type','content'])
    return df

def renew_dict(label,index,dict):   #label的相对位置以字典的形式存放
    dict[label] = index
    return dict

#第一次扫描，记录label的相对位置
def main_scan(test_file):     
    data_flag = False   #是否记录data
    assemble_flag = False   #是否开始.text过程
    # compile_flag = False    #是否编译这一行
    # count_flag = False  #相对地址是否加一

    address_index = 0  #找到data在哪一行
    data_list = []  #用来记录data的那个二位列表
    label_dict = dict()

    fin = open(test_file,"r") 

    for line in fin:

        line = line.strip() #去掉两端的空格
        if (line.find("#") == 0):   #如果整行都是comment，这行就不用管了
            continue
        if (line == ''):    #如果这行是空的，也不用继续下去了
            continue    

        line = discard_comment(line)    #把comment部分删掉
        
        if '.data' in line:
            data_flag = True    #标志着出现.data列，下一次循环开始把data记录到data_list里面
            continue

        if data_flag == True:  #把data记录到data_list里面（默认一个data）
            new_row = []
            a = line.find(":")  #':‘的位置
            col_1 = line[:a]    #data的名字
            new_row.append(col_1)
            remain_data = line[(a+1):] 
            remain_data = remain_data.lstrip()
            b = remain_data.find(' ')
            col_2 = remain_data[:b]  #data的数据类型
            new_row.append(col_2)
            col_3 = remain_data[(b+1):].lstrip()   #data的内容
            new_row.append(col_3)
            data_list.append(new_row)  
            
        if '.text' in line:         #到.text了，停止记录.data部分
            data_flag = False
            assemble_flag = True    #准备下一次循环开始记地址并编译

            #把.data的数据用data_structure存起来
            data_frame = construct_dataframe(data_list)  
            # print(construct_datatable(data_list))     #如果想查看.data部分内容，可以运行这个print语句
            continue
                
        if assemble_flag == True:      

            line = line.split()   #把这一行代码分成几部分
            for i in range(len(line)):
                line[i] = line[i].rstrip(',')   #去掉逗号
                line[i] = line[i].rstrip(':')   #去掉label后面的冒号

            if line[0] not in all_mips:   #这是一个label，label不算地址
                label_dict = renew_dict(line[0],address_index,label_dict)   #label及其相对地址以字典的形式存放
                  
            if (line[0] in all_mips) or ((len(line) > 1) and (line[1] in all_mips)): #这一行有instruction，label可能跟代码在同一行
                address_index += 1   #instruction算地址

    fin.close()
    # print(label_dict)     #如果想看储存有label的相对位置的字典，可以运行此行
    return label_dict


