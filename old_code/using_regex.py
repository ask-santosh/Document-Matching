import textract
import re

# text = textract.process("E:/Documents/Ongoing Projects/office_work/Bill Verification/test bill/qcdnb00214.pdf")
# text = textract.process("EXP-2144.pdf")
text = textract.process("CD_21_05.pdf")
test_string = text.decode('utf-8')
print(test_string)
file1 = open('cd_21_05.txt', 'w')
file1.write(test_string)
file1.close()
test_string = test_string[test_string.find('SL\n') + 3:]
pattern = '^[0-9]'
num_of_products = 0
for line in test_string.split('\n'):
    if re.search(pattern, line):
        num_of_products = int(line)
    else:
        break

print(f"Number of products: {num_of_products}")

# ----------
test_string = test_string[test_string.find('UNIT\n\n')+6:]
# print(test_string)
products = test_string.split('\n')[:num_of_products]
print(products)

# ----------------
test_string = test_string[test_string.find('CREDIT NOTE\n')+12:]
unit = test_string.split('\n')[:num_of_products]
print(unit)

# -------------------------
test_string = test_string[test_string.find('EXPIR\n\n')+7:]
batch = test_string.split('\n')[:num_of_products]
print(batch)

# ----------------------------
from datetime import datetime
test_string = test_string[test_string.find('\n\n')+2:]
# expir = [datetime.strptime(data, '%m-%y') for data in test_string.split('\n')[:num_of_products]]
expir = test_string.split('\n')[:num_of_products]
print(expir)

# ----------------------------------
test_string = test_string[test_string.find('QNTY FREE\n')+10:]
qts = test_string.split('\n')[:num_of_products]
print(qts)

import pandas as pd
save_csv = pd.DataFrame({'PRODUCT': products, 'UNIT': unit, 'BATCH': batch, 'EXPIRY': expir, 'QNTY': qts})

# save_csv.to_csv('exctrated-exp-2144.csv', index=False)
# csv_file = pd.read_csv('exctrated-exp-2144.csv')
sorted_csv = save_csv.sort_values(by=['PRODUCT'])
print(sorted_csv)
# sortedlist = sorted(csv_file, key=lambda row: row[1], reverse=True)
# sorted_csv.to_csv('CD_21_05.csv', index=False)

# pattern = '^UNIT\n'
# result = re.match(pattern, test_string)
# result1 = re.search(pattern, test_string)
# result2 = re.findall("UNIT", test_string)
# result3 = re.split("PRODUCT", test_string)
# print(f"result1 value {result1}")
# print(result)
# print(result2)
# print(f"result3 value{result3}")
# print(result1.start())
