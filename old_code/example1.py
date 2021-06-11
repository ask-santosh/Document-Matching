# import textract
# extract_data = textract.process(
#     './qcdnb00286-1.jpg', encoding='ascii')
# print(extract_data.decode('utf-8'))


# ----------------------------------------------------------------------------------------

import easyocr
# import gc

reader = easyocr.Reader(['en'])
result = reader.readtext('J1534-1.jpg')
print(result)

# del variable
# gc.collect()
