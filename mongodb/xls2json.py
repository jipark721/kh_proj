import json
import xlrd

xls2json_files = {
    "xls/diseases.xlsx" : "json/diseases.json",
    "xls/patients.xlsx" : "json/patients.json",
    "xls/ingredients.xlsx" : "json/ingredients.json",
}

for xls_file_name, json_file_name in xls2json_files.items() :
    workbook = xlrd.open_workbook(xls_file_name, encoding_override="utf_8")
    worksheet = workbook.sheet_by_name("Sheet1")

    data = []
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
        data.append(row_data)

    with open(json_file_name, 'w') as json_file:
        data = json.dumps({'data': data}, indent=4, ensure_ascii=False)
        json_file.write(data)