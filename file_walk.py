import os
import re
from mybs import parser
index = {'\\by':11, '\\jrcs':14, '\\jrzl':13, '\\jrzz':12, '\\pzby':18, '\\pzcs':19, '\\pzzz':16, '\\tsjs':3, '\\xwdt':2}
file_dict=[]
for v,k,j in os.walk('.'):
    for name in j:
        if re.match(r'\d*.html',name):
            file_id = int(name.split('.')[0])
            if file_id >452:
#                 if v.split('.')[1] not in file_dict:
#                     file_dict.append(str(v.split('.')[1]))
# print(file_dict)

                column_id=index[v.split('.')[1]]
                path = v + '\\' + name
                cell=(file_id,column_id,path)
                file_dict.append(cell)
with open('recovery.sql','w+',encoding='utf-8') as f:    
    for f_id,c_id,path in file_dict:
        pas = parser(f_id,c_id,path)
        pas.to_sql()
        f.write(pas.sql_1+';\n')
        f.write(pas.sql_2+';\n')
        f.write(pas.sql_3+';\n')
    
'''pa = parser(file_dict[578]) '''               
            
