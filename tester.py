import process_mips
import scan_label
import os

from scan_label import test_file
from process_mips import r_mips
from process_mips import i_mips
from process_mips import j_mips
from process_mips import all_mips

#test file的写入放在scan_label.py了，防止circular import
# test_file=input("Please enter the test file name:")
# while not os.path.exists(test_file):
#     test_file=input("Your input is wrong, please enter the correct name:")

output_file=input("Please enter the output file name:") #如果目录里面不存在这个文件，系统就会新建一个
expectedoutput_file=input("Please enter the expected output file name:")
while not os.path.exists(expectedoutput_file):
    expectedoutput_file=input("Your input of expected output file is wrong, please enter the correct name:")

fin = open(test_file,"r") 
fout = open(output_file,'w')
assemble_flag = False
address_index = 0

#mips转换成machine code
for line in fin:
    line = line.strip() #去掉两端的空格
    if (line.find("#") == 0):   #如果整行都是comment，这行就不用打印了
        continue
    if (line == ''):    #如果这行是空的，也不用打印了
        continue    

    line = scan_label.discard_comment(line)   #把“#”后面的删了
    line = line.split() #把这一行代码分成几部分

    for i in range(len(line)):
        line[i] = line[i].rstrip(',')   #去掉逗号
        line[i] = line[i].rstrip(':')   #去掉label后面的冒

    if line[0] == '.text':  #到.text了，停止统计.data
        assemble_flag = True    #下一个循环准备开始记地址并编译
        continue

    if assemble_flag == True:          
        if (line[0] in all_mips) or (  (len(line) > 1) and (line[1] in all_mips)  ): #因为指令的位置可能跟label同一行，也可能在另一行
            
            #label跟指令在同一行的情况，可把label从line中截去
            if line[0] != "syscall":  #syscall比较特殊，他的mips指令只有一个单词，因此就没有line[1]，所以要先排除这个可能
                if line[1] in all_mips: 
                    del(line[0])

            if line[0] in r_mips:
                fout.write(process_mips.convert_r(line))
                fout.write('\r\n')
            if (line[0] in i_mips) or (line[0] in j_mips):
                fout.write(process_mips.convert_ij(line,address_index))
                fout.write('\r\n')
            address_index += 1   #有instruction才把address_index加1

fin.close()
fout.close()

congratulations_flag = True

fout2 = open(output_file,'r')
fcheck = open(expectedoutput_file,'r')

#处理output和expected output的输出数据
output_lines = fout2.readlines()
for i in range(len(output_lines)):
    line = output_lines[i]
    line = line.replace("\n","") #delete "\n"
    line = line.rstrip()
    output_lines[i]=line
check_lines = fcheck.readlines()
for i in range(len(check_lines)):
    line = check_lines[i]
    line = line.replace("\n","") #delete "\n"
    line = line.rstrip()
    check_lines[i]=line

#对比output和expected output是否一致
for i in range(len(output_lines)):
    if check_lines[i] != output_lines[i]:
        print('You did something wrong in line',(i+1))
        print('The expected output should be:',check_lines[i])
        print('But your output is:',output_lines[i])
        congratulations_flag = False
if congratulations_flag == True:
    print("All Passed! Congratulations!")

fout2.close()
fcheck.close()



 