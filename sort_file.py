import pandas as pd
from fuzzywuzzy import process
import Levenshtein as lev
import numpy as np
import openpyxl

# -----------------------code for first csv file-------------------------------------------
buyer_df = pd.read_csv("./results/CD_21_05/final2.csv", usecols=['PRODUCTS','UNITS', 'BATCHES', 'EXPIRY'])
# aggregation_functions
return_list = []
for i, row in buyer_df.iterrows():
    return_list.append(' - '.join((row['PRODUCTS'], row['UNITS'], row['BATCHES'], row['EXPIRY'])))

# ---------------------------code for second csv file -----------------------------------------
jk_df = pd.read_csv("./results/JK_21_05/final.csv", usecols=['PRODUCTS','UNITS', 'BATCHES', 'EXPIRY'])
# aggregation_functions
purchase_list = []
for i, row in jk_df.iterrows():
    purchase_list.append(' - '.join((row['PRODUCTS'], row['UNITS'], row['BATCHES'], row['EXPIRY'])))


def max5_similarities(list_of_tup):
    lst = len(list_of_tup)
    for i in range(0, lst):
        for j in range(0, lst - i - 1):
            if list_of_tup[j][1] > list_of_tup[j + 1][1]:
                list_of_tup[j], list_of_tup[j + 1] = list_of_tup[j + 1], list_of_tup[j]
        # print(list_of_tup)
    return list_of_tup[lst-5:][::-1]


rows_to_color = []
for i in range(len(return_list)):
    ratios = [(x, round(lev.ratio(return_list[i], x), 3)) for x in purchase_list]
    ratios = max5_similarities(ratios)
    # print(return_list[i], '--', ratios)
    if ratios[0][1] < 0.7:
        rows_to_color.append(i)


def color_cells(x):
    global rows_to_color
    color = 'background-color: red'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    for i in rows_to_color:
        df1.iloc[i, :] = 'background-color: red'
    return df1


buyer_df.style.apply(color_cells, axis=None).to_excel('Final_Result.xlsx', engine='openpyxl', index=False)

#     for pdt in  max5_similarities(Ratios):
#         if pdt[1]<0.7:
#             c1 = 'background-color: red'
#             c2 = ''
#             # df1 = pd.DataFrame(c2, index=pdt.index, columns=pdt.columns)
#             # print(df1)
#             # df1.loc[pdt, :] = c1
#             (df1.style.apply(pdt, axis=None).to_excel('styled.xlsx', engine='openpyxl', index=False))
#     # if max5_similarities(Ratios) < 0.7:
#     #     print(max5_similarities(Ratios))
#
#     # Ratios = sorted(Ratios, key=lambda x: x[1], reverse=True)
#     # print(prod, "--->", max5_similarities(Ratios))
#
#     # a = np.array(Ratios)
#
#     # print(a[0:5, a])

