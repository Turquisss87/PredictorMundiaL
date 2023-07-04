import pandas as pd
from string import ascii_uppercase as alfabeto
import pickle



todas_las_tablas = pd.read_html("https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup")



dict_tablas ={}


for letra, _ in zip(alfabeto, range (12,68,7)):
    df =todas_las_tablas[_]
    df.rename(columns={df.columns[1]:"Team"}, inplace=True)
    df.pop("Qualification")
    dict_tablas[f"Group {letra}"] = df


with open('dict_table','wb') as output:
    pickle.dump(dict_tablas, output)




