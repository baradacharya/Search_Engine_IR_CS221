import numpy as np
import pandas as pd

data = pd.read_csv("NDCG.txt",delim_whitespace=True).values
data = np.array(data)
print data
result = []
line = []
for row in data:
    i = 1
    sum  = 0.0
    line = []
    for col in row:

        if(i == 1):
            sum  += col
        else :
            x = float(col)/np.log(i)
            sum += x
        i= i + 1
        line.append(sum)
    result.append(line)
google  = result[0]
final_result = []
for ln in result:
    temp_list =[]
    for i in range(0,len(ln)):
        temp_list.append(ln[i]/google[i])
    final_result.append(temp_list)
    print temp_list

