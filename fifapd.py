import pandas as pd

df_data_historica = pd.read_csv('historical_data.csv')

df_data_faltante = pd.read_csv('fifa_worlds_cups.csv')

df_fixture = pd.read_csv('fixture_2022b.csv')



df_fixture['home']= df_fixture['home'].str.strip()

df_fixture['away'] = df_fixture['away'].str.strip()


df_data_historica['home']= df_data_historica['home'].str.strip()

df_data_historica['away'] = df_data_historica['away'].str.strip()


df_data_faltante['home']= df_data_faltante['home'].str.strip()

df_data_faltante['away'] = df_data_faltante['away'].str.strip()

#print(df_data_faltante[df_data_faltante['home'].isnull()])

df_data_faltante.dropna(inplace=True)

df_data_historica = pd.concat([df_data_faltante, df_data_historica], ignore_index=True)


df_data_historica.drop_duplicates(inplace=True)

df_data_historica.sort_values('year', inplace=True)


index_a_eliminar = df_data_historica[ df_data_historica['home'].str.contains('Sweden') &
df_data_historica['away'].str.contains('Austria')].index

df_data_historica.drop(index_a_eliminar, inplace=True)


#df_data_historica[df_data_historica['score'].str.contains('[^/d]')]

df_data_historica['score'] = df_data_historica['score'].str.replace('[^\d–]','', regex=True)






df_data_historica[['Home goals', 'Away goals']]= df_data_historica['score'].str.split('–', expand=True)



df_data_historica.drop('score', axis=1,inplace=True)


df_data_historica.rename(columns={'home': 'Home Team', 'away': 'Away Team', 'year': 'Year'}, inplace=True)




df_data_historica= df_data_historica.astype({'Home goals':int, 'Away goals':int})



df_data_historica['Total Goals per match'] = df_data_historica['Home goals'] + df_data_historica ['Away goals']


df_data_historica.to_csv('data_historica_mundiales.csv', index=False)

df_fixture.to_csv('fixture_2002_clean.csv')