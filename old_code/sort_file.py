import pandas as pd
from fuzzywuzzy import process
import Levenshtein as lev
import numpy as np
# -----------------------code for first csv file-------------------------------------------
df = pd.read_csv("extracted_qcdnb00214_sorted.csv", usecols=['PRODUCT', 'BATCH', 'QNTY', 'UNIT', 'EXPIRY'])
aggregation_functions = {'PRODUCT': 'first', 'QNTY': 'sum', 'UNIT': 'first', 'EXPIRY': 'first'}
df_old = df.groupby(df['BATCH']).aggregate(aggregation_functions)
sorted_value_old = df_old.sort_values(by=['PRODUCT'])
product1 = list(sorted_value_old.PRODUCT)
# print(product1)
# ---------------------------code for second csv file -----------------------------------------
df1 = pd.read_csv("exctrated-exp-2144_sorted.csv", usecols=['PRODUCT', 'BATCH', 'QNTY', 'UNIT', 'EXPIRY'])
aggregation_functions = {'PRODUCT': 'first', 'QNTY': 'sum', 'UNIT': 'first', 'EXPIRY': 'first'}
df_new = df1.groupby(df1['BATCH']).aggregate(aggregation_functions)
sorted_value = df_new.sort_values(by=['PRODUCT'])
product2 = list(sorted_value.PRODUCT)

# print(product2)


def max5_similarities(list_of_tup):
    lst = len(list_of_tup)
    for i in range(0, lst):
        for j in range(0, lst - i - 1):
            if list_of_tup[j][1] > list_of_tup[j + 1][1]:
                list_of_tup[j], list_of_tup[j + 1] = list_of_tup[j + 1], list_of_tup[j]
        # print(list_of_tup)
    return list_of_tup[lst-5:][::-1]



for prod in product2:
    Ratios = [(x, round(lev.ratio(prod, x), 3)) for x in product1]
    # Ratios = sorted(Ratios, key=lambda x: x[1], reverse=True)
    print(prod, "--->", max5_similarities(Ratios))

    # a = np.array(Ratios)

    # print(a[0:5, a])

