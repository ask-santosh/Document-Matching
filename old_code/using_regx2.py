import textract
import re

# text = textract.process("E:/Documents/Ongoing Projects/office_work/Bill Verification/test bill/qcdnb00214.pdf")
# text = textract.process("qcdnb00214.pdf")
# text = textract.process("JK_21_05.pdf")
text = textract.process("JK2_21_050_result.jpg")
test_string = text.decode('utf-8')
# print(test_string)
file1 = open('jk050_result.txt', 'w')
file1.write(test_string)
file1.close()

# ----------
test_string = test_string[test_string.find('Exp.\n\n')+6:]
last_idx = test_string.find('\n\n')
batch = test_string[:last_idx].split('\n')
test_string = test_string[last_idx+1:]
num_of_products = len(batch)
print("Number of products: ", num_of_products)
print(batch)

# ----------------------------------------------
test_string = test_string[1:]
expire = test_string.split('\n')[:num_of_products]
print(expire)
test_string = test_string[len("\n".join(expire))+1:]
# print(test_string)

#----------------------------------------
test_string = test_string[1:]
mfr = test_string.split('\n')[:num_of_products-1]
test_string = test_string[len("\n".join(mfr))+1:]
# print(test_string)

start_index = test_string.find('Mfr.\n')+5
mfr1 = test_string[start_index:test_string.find('\n', start_index)]
mfr.insert(0, mfr1)
print(mfr)

#---------------------------------------------
test_string = test_string[test_string.find('Qty.\n')+5:]
qty = test_string.split('\n')[:num_of_products]
print(qty)
test_string = test_string[len("\n".join(qty))+1:]

#----------------------------------------------
test_string = test_string[test_string.find('C\n\n')+3:]
product = test_string.split('\n')[:num_of_products]
print(product)
test_string = test_string[len("\n".join(product))+1:]

#------------------------------------------------

test_string = test_string[test_string.find('Packing\n')+8:]
packing = test_string.split('\n')[:num_of_products]
print(packing)
test_string = test_string[len("\n".join(packing))+1:]

print(test_string)
import pandas as pd
save_csv = pd.DataFrame({'PRODUCT': product, 'UNIT': packing, 'BATCH': batch, 'EXPIRY': expire, 'QNTY': qty})

# save_csv.to_csv('extracted_qcdnb00214.csv', index=False)
# csv_file = pd.read_csv('extracted_qcdnb00214.csv')
sorted_csv = save_csv.sort_values(by=['PRODUCT'])
print(sorted_csv)
# sortedlist = sorted(csv_file, key=lambda row: row[1], reverse=True)
# sorted_csv.to_csv('JK2_21_05.csv', index=False)

