python xls2json.py
mongoimport --db khdb --collection diseases --drop --file json/diseases.json --jsonArray
mongoimport --db khdb --collection patients --drop --file json/patients.json --jsonArray
mongoimport --db khdb --collection ingredients --drop --file json/ingredients.json --jsonArray
mongoimport --db khdb --collection nutrients --drop --file json/nutrients.json --jsonArray
