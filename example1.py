import pandas as pd
from pdf2image import convert_from_path
import os
import cv2
import easyocr
import gc
import pandas
import sys
test_template_data = [{'id': 1, 'name': 'JK agency', 'height': 2338, 'width': 1653,
                       'product_region': ((167, 473), (503, 1650)),
                       'unit_region': ((511, 473), (623, 1650)),
                       'batch_region': ((610, 473), (770, 1650)),
                       'exp_region': ((770, 473), (850, 1650)),
                       'qty_region': ((1026, 473), (1100, 1650))
                       }]

text_reader = easyocr.Reader(['en'], gpu=False)


def convert2images(filepath):
    filename = filepath.split('/')[-1].split('.')[0]
    images = convert_from_path(filepath)

    res_dir = f'results/{filename}'
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)
    for i in range(len(images)):
        # Save pages as images from pdf
        images[i].save(f'results/{filename}/page_{i + 1}' + '.jpg', 'JPEG')
    gc.collect()
    return res_dir


def get_template(image, templates=[]):
    # get ID of template
    for template in test_template_data:
        if template['id'] == 1:
            gc.collect()
            return template


def line_removal(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Horizontal lines removal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
    cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 5)

    # Vertical lines removal
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
    remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
    cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 5)
    gc.collect()
    return image


def getlines_from_extract(data):
    lines = []
    last_y = 0
    line = ''
    ctr = 1
    for d in data:
        if d[0][-1][1] - last_y > 20:
            lines.append(line)
            line = d[1]
            if ctr == len(data):
                lines.append(line)
            last_y = d[0][-1][1]
        else:
            line += ' '+d[1]
        ctr += 1
    return lines


def extract_text(image):
    template = get_template(image)

    # img_not = cv2.bitwise_not(image)
    # cv2.imshow("inverted image", img_not)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # image = cv2.dilate(img_not, None, iterations=1)
    # cv2.imshow("Dilated {} times".format(2), image)
    # cv2.waitKey(0)

    # scale height & width
    scale_x = 1.0   # original_image_width / current_image_width
    scale_y = 1.0   # original_image_height / current_image_height

    # Get products
    product_x1, product_y1 = template['product_region'][0][0] * scale_x, template['product_region'][0][1] * scale_y
    product_x2, product_y2 = template['product_region'][1][0] * scale_x, template['product_region'][1][1] * scale_y
    product_region = image[int(product_y1): int(product_y2), int(product_x1): int(product_x2)]
    result = text_reader.readtext(product_region)
    products = getlines_from_extract(result)

    # Get units
    unit_x1, unit_y1 = template['unit_region'][0][0] * scale_x, template['unit_region'][0][1] * scale_y
    unit_x2, unit_y2 = template['unit_region'][1][0] * scale_x, template['unit_region'][1][1] * scale_y
    unit_region = image[int(unit_y1): int(unit_y2), int(unit_x1): int(unit_x2)]
    result = text_reader.readtext(unit_region)
    units = getlines_from_extract(result)

    # Get Batches
    batch_x1, batch_y1 = template['batch_region'][0][0] * scale_x, template['batch_region'][0][1] * scale_y
    batch_x2, batch_y2 = template['batch_region'][1][0] * scale_x, template['batch_region'][1][1] * scale_y
    batch_region = image[int(batch_y1): int(batch_y2), int(batch_x1): int(batch_x2)]
    result = text_reader.readtext(batch_region)
    batches = getlines_from_extract(result)

    # Get Expiry
    exp_x1, exp_y1 = template['exp_region'][0][0] * scale_x, template['exp_region'][0][1] * scale_y
    exp_x2, exp_y2 = template['exp_region'][1][0] * scale_x, template['exp_region'][1][1] * scale_y
    exp_region = image[int(exp_y1): int(exp_y2), int(exp_x1): int(exp_x2)]
    result = text_reader.readtext(exp_region)
    expiry_dates = getlines_from_extract(result)

    # Get Quantity
    qty_x1, qty_y1 = template['qty_region'][0][0] * scale_x, template['qty_region'][0][1] * scale_y
    qty_x2, qty_y2 = template['qty_region'][1][0] * scale_x, template['qty_region'][1][1] * scale_y
    qty_region = image[int(qty_y1): int(qty_y2), int(qty_x1): int(qty_x2)]
    result = text_reader.readtext(qty_region)
    quantities = getlines_from_extract(result)

    for qty in quantities:
        print(qty)

    cv2.imshow('qty', qty_region)
    cv2.waitKey(0)

    return products, units, batches, expiry_dates, quantities


file_path = input("enter file path to proceed: ")
result_dir = convert2images(file_path)

pages = []
for r, d, files in os.walk(result_dir):
    for file in files:
        if file.split('.')[-1] in ['jpg', 'JPG', 'JPEG']:
            pages.append(file)
    pages = pages[::-1]
    break

final_products = []
final_units = []
final_batches = []
final_expiry = []
final_quantities = []

for img_name in pages:
    img = cv2.imread(result_dir + f'/{img_name}')
    print(result_dir + f'/{img_name}', type(img))
    products, units, batches, expiry_dates, quantities = extract_text(img)
    final_products.extend(products[1:])
    final_units.extend(units[1:])
    final_batches.extend(batches[1:])
    final_expiry.extend(expiry_dates[1:])
    final_quantities.extend(quantities[1:])

# print('final_products: ', final_products)
# print('final_units: ', final_units)
# print('final_batches: ', final_batches)
print('final_QTY: ', len(final_quantities))

df = pd.DataFrame({'PRODUCTS': final_products, 'UNITS': final_units,
                   'BATCHES': final_batches, 'EXPIRY': final_expiry})
sorted_csv = df.sort_values(by=['PRODUCTS'])

sorted_csv.to_csv(f'{result_dir}/final.csv', index=False)

print('Completed...')
cv2.destroyAllWindows()
