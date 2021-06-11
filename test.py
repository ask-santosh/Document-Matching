import cv2
import matplotlib.pyplot as plt
import easyocr
reader = easyocr.Reader(['en'], gpu=False)
image = cv2.imread('results/JK_21_05/page_1.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
dilated = cv2.dilate(image, None, iterations=1)
eroded = cv2.erode(image, None, iterations=1)

res = reader.readtext(eroded)
cv2.imshow('s', eroded)
cv2.waitKey(0)
cv2.destroyAllWindows()
# for response in res:
#     print(res)
for (bbox, text, prob) in res:
  # unpack the bounding box
    (tl, tr, br, bl) = bbox
    tl = (int(tl[0]), int(tl[1]))
    tr = (int(tr[0]), int(tr[1]))
    br = (int(br[0]), int(br[1]))
    bl = (int(bl[0]), int(bl[1]))
    cv2.rectangle(eroded, tl, br, (0, 255, 0), 2)
    cv2.putText(eroded, text, (tl[0], tl[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
cv2.imshow("Image", eroded)
cv2.waitKey(0)