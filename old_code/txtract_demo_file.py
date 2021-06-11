import cv2
import textract
# text = textract.process("E:/Documents/Ongoing Projects/office_work/Bill Verification/test bill/qcdnb00214.pdf")
img = cv2.imread("../results/JK2_21_05/page_1.jpg")
# cv2.imwrite('test.jpg', img[473:1650, 1026:1100])

text = textract.process('test.jpg')
var1 = text.decode('utf-8')
print(var1)
# file1 = open('page0.txt', 'w')
# file1.write(var1)
# file1.close()
