import pandas as pd
# -----------------------code for first csv file-------------------------------------------
df = pd.read_csv("exctrated-exp-2144_sorted.csv", usecols=['PRODUCT', 'BATCH', 'QNTY', 'UNIT', 'EXPIRY'])
aggregation_functions = { 'QNTY': 'sum', 'UNIT': 'first', 'EXPIRY': 'first'}
df_old = df.groupby(['BATCH','PRODUCT']).aggregate(aggregation_functions)
# print(df_old)
sorted_value_old = df_old.sort_values(by=['PRODUCT'])
# print(sorted_value_old)
f1 = sorted_value_old.sort_values("PRODUCT", inplace=False)
print(f1)
prod_name = f1.PRODUCT
# for row in sorted_value_old.iterrows():
#     print(type(row))

# s = list(sorted_value_old)
# print(s)
# print(s['BATCH'])
# prod_name = sorted_value_old.PRODUCT
# product1 = list(sorted_value_old.PRODUCT)