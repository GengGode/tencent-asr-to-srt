import re
import os
import sys

from sqlalchemy import false, true

def int_str_2(i:int,is_cut:bool=false):
	s=str(i)
	len_s=len(s)
	if len_s==1:
		s='0'+s
	elif len_s >2 and is_cut==true:
		s=s[0]+s[1]
	return s

def read_tencent_asr_file(file_path:str):
	with open(file_path,'r',encoding='utf8') as f:
		content=f.read()
	lines=content.splitlines()
	return lines

def find_all_file_name(f_dir:str):
    for root, dirs, files in os.walk(f_dir):
        for file_name in files:
            yield file_name

def lrc_file_write(file_handle,cmd:int,value):
	if cmd==0:
		file_handle = open(value,'w',encoding='utf-8')
	if cmd==1:
		file_handle.close()
	if cmd==2:
		file_handle.write("[%s:%s.%s]%s\n"%(int_str_2(value[0]),int_str_2(value[1]),int_str_2(value[2],true),value[6]))
	return file_handle

def parse_asr_file(lines):
	# 0 read file name and open file
	# 1 close file
	# 2 read file parse data to file
	cmd = 0 #
	write_file_handle=''
	line_id=0
	while line_id<len(lines)-1:
		line=lines[line_id]

		if cmd==0:
			file_name_match=re.findall(R"file: (.*?)$",line)
			file_name=file_name_match[0]
			file_name_noextension=os.path.splitext(file_name)[0]
			# print(file_name_noextension)
			write_file_handle=lrc_file_write(write_file_handle,cmd,file_name_noextension)
			cmd=2
			line_id+=1
		elif cmd==1:
			write_file_handle=lrc_file_write(write_file_handle,cmd,None)
			cmd=0
		elif cmd==2:
			# match_end_symbol=re.findall(R"*end*",line)
			line_data_match=re.findall('\[(\d*?):(\d*?)\.(\d*?),(\d*?):(\d*?)\.(\d*?).*?\]  (.*?)$',line)
			if len(line_data_match)==1:
				line_data=line_data_match[0]
				write_file_handle=lrc_file_write(write_file_handle,cmd,line_data)
			else:
				cmd=1
				line_id+=1
		line_id+=1

def main():
	file_dir="C:\\Users\\WDAGUtilityAccount\\Desktop\\text\\"
	for file_name in find_all_file_name(file_dir):
		file_path=file_dir+file_name
		file_lines=read_tencent_asr_file(file_path)
		parse_asr_file(file_lines)
		print(file_path,file_lines[0])

if __name__ == '__main__':
    main()
else:
	file_dir=sys.argv[0]
	for file_name in find_all_file_name(file_dir):
		file_path=file_dir+file_name
		file_lines=read_tencent_asr_file(file_path)
		parse_asr_file(file_lines)
		print(file_path,file_lines[0])