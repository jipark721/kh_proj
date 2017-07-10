import pandas as pd

obj_names = ["disease", "ingredient", "nutrient", "patient"]

for obj_name in obj_names:
    pd.read_json("json/"+obj_name+".json").to_excel("xlsx/"+obj_name+".xlsx")