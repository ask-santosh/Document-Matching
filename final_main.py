from pdf2image import convert_from_path
import os
import gc
import cv2
import easyocr
import pandas as pd
import Levenshtein as lev
from datetime import datetime


test_template_data = [{'id': 1, 'name': 'JK agency', 'height': 2338, 'width': 1653,
                       'product_region': ((167, 473), (503, 1650)),
                       'unit_region': ((511, 473), (623, 1650)),
                       'batch_region': ((610, 473), (770, 1650)),
                       'exp_region': ((770, 473), (850, 1650)),
                       'qty_region': ((1026, 473), (1100, 1650))
                       },
                      {'id': 2, 'name': 'CD Associates', 'height': 2339, 'width': 1653,
                       'product_region': ((117, 436), (630, 1929)),
                       'unit_region': ((630, 436), (723, 1929)),
                       'batch_region': ((723, 436), (870, 1929)),
                       'exp_region': ((870, 436), (950, 1929)),
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


def get_template(image, templates=[], temp_id=0):
    # get ID of template
    for template in test_template_data:
        if template['id'] == temp_id:
            gc.collect()
            return template


def getlines_from_extract(data):
    lines = []
    last_y = 0
    line = ''
    ctr = 1
    for d in data:
        if d[0][-1][1] - last_y > 20:
            lines.append(line)
            line = d[1]
            last_y = d[0][-1][1]
        else:
            line += ' ' + d[1]

        if ctr == len(data):
            lines.append(line)
        ctr += 1
    return lines


def change_date(dt_str):
    if len(dt_str) > 0:
        dt = datetime.strptime(dt_str, '%m-%y')
        return dt.strftime('%-m/%y')
    return dt_str


def extract_text(image, temp_id):
    template = get_template(image, temp_id=temp_id)

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

    if temp_id == 2:
        expiry_dates = list(map(change_date, expiry_dates))

    # Get Quantity
    qty_x1, qty_y1 = template['qty_region'][0][0] * scale_x, template['qty_region'][0][1] * scale_y
    qty_x2, qty_y2 = template['qty_region'][1][0] * scale_x, template['qty_region'][1][1] * scale_y
    qty_region = image[int(qty_y1): int(qty_y2), int(qty_x1): int(qty_x2)]
    result = text_reader.readtext(qty_region)
    quantities = getlines_from_extract(result)

    return products, units, batches, expiry_dates, quantities


def get_final_csv(result_dir, temp_id):
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
        products, units, batches, expiry_dates, quantities = extract_text(img, temp_id)
        final_products.extend(products[1:])
        final_units.extend(units[1:])
        final_batches.extend(batches[1:])
        final_expiry.extend(expiry_dates[1:])
        final_quantities.extend(quantities[1:])

    df = pd.DataFrame({'PRODUCTS': final_products, 'UNITS': final_units,
                       'BATCHES': final_batches, 'EXPIRY': final_expiry})
    sorted_csv = df.sort_values(by=['PRODUCTS'])

    sorted_csv.to_csv(f'{result_dir}/final.csv', index=False)
    return f'{result_dir}/final.csv'


def max5_similarities(list_of_tup):
    lst = len(list_of_tup)
    for i in range(0, lst):
        for j in range(0, lst - i - 1):
            if list_of_tup[j][1] > list_of_tup[j + 1][1]:
                list_of_tup[j], list_of_tup[j + 1] = list_of_tup[j + 1], list_of_tup[j]
        # print(list_of_tup)
    return list_of_tup[lst-5:][::-1]


def color_cells(x):
    global rows_to_color
    color = 'background-color: red'
    df1 = pd.DataFrame('', index=x.index, columns=x.columns)
    for i in rows_to_color:
        df1.iloc[i, :] = 'background-color: red'
    return df1


if __name__ == "__main__":
    jk_pdf = input('Give pdf of JK Agency ({specific year} template): ')
    cd_pdf = input('Give pdf of CD Associates: ')

    result_dir = convert2images(jk_pdf)
    jk_csv = get_final_csv(result_dir, 1)

    result_dir = convert2images(cd_pdf)
    cd_csv = get_final_csv(result_dir, 2)

    # ---------------------------------------------------------
    jk_df = pd.read_csv(jk_csv, usecols=['PRODUCTS', 'UNITS', 'BATCHES', 'EXPIRY'])
    # aggregation_functions
    jk_list = []
    for i, row in jk_df.iterrows():
        jk_list.append(' - '.join((row['PRODUCTS'], row['UNITS'], row['BATCHES'], row['EXPIRY'])))

    # ---------------------------------------------------------
    cd_df = pd.read_csv(cd_csv, usecols=['PRODUCTS', 'UNITS', 'BATCHES', 'EXPIRY'])
    # aggregation_functions
    cd_list = []
    for i, row in cd_df.iterrows():
        cd_list.append(' - '.join((row['PRODUCTS'], row['UNITS'], row['BATCHES'], row['EXPIRY'])))

    rows_to_color = []
    for i in range(len(cd_list)):
        ratios = [(x, round(lev.ratio(cd_list[i], x), 3)) for x in jk_list]
        ratios = max5_similarities(ratios)
        print(cd_list[i], ratios)
        # print(return_list[i], '--', ratios)
        if ratios[0][1] < 0.7:
            rows_to_color.append(i)

    excel_filename = f'verified_result/comparison of {jk_pdf.split("/")[-1].split(".")[0]} & '
    excel_filename += f'{cd_pdf.split("/")[-1].split(".")[0]}.xlsx'

    cd_df.style.apply(color_cells, axis=None).to_excel(excel_filename,
                                                       engine='openpyxl', index=False)
    print(f'result stored at "{excel_filename}"')

    os.system(f'libreoffice --calc "{excel_filename}"')
cv2.destroyAllWindows()
