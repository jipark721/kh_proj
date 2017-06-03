xls2json.py
mongoimport --db khdb --collection diseases --drop --file json/diseases.json
mongoimport --db khdb --collection patients --drop --file json/patients.json
mongoimport --db khdb --collection ingredients --drop --file json/ingredients.json

