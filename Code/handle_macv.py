# MARK:- libs
import numpy as np
import pandas as pd
from support_function import *

import re
import time
import pprint

# MARK: read input data
macv = []

f = open("macv.txt", "r", encoding='utf-8')
for line in f:
    macv.append(line)
f.close()

# MARK:- String Normalization
patterns = {}

for i in range(macv.__len__()):
    line = macv[i].rstrip()
    line = re.sub('(\s{2,})', ' ', line)
    line = line.lower()
    words = re.split(r" ", line, flags=re.UNICODE)
    if words.__len__() >= 2:
        if (words[0]) not in patterns:
            try:
                key = str(words[0][0]) + str(words[1][0])
                if key not in patterns:
                    value = words[0] + " " + words[1]
                    patterns[key] = value
            except Exception:
                print("ERROR:" + str(i))
                pprint.pprint(words)
        else:
            key = words[0]
            
            value = patterns[key]
        current_pattern = re.compile(rf"({key}.*)|"
                                    rf"({value}.+)", flags=re.IGNORECASE)
        if current_pattern.match(line):
            print(str(i) + "\t" + line + "-> " + patterns[key])
            time.sleep(1)
    


# for i in patterns:
#     print(patterns[i])
#     time.sleep(2)
    # nhanvien_pattern = re.compile(
    #     r"(nhân viên.+)|"
    #     r"(nv.*)", flags=re.IGNORECASE)
    # if nhanvien_pattern.match(word):
    #     print(str(i) + "\t" + word + "-> nhân viên")
    #     time.sleep(1)
