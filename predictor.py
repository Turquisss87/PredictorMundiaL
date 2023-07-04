import pandas as pd
import pickle
from scipy.stats import poisson

dict_table= pickle.load(open('dict_table', 'rb'))

df_historica_data= pd.read_csv('data_historica_mundiales.csv')

df_fixture = pd.read_csv('fixture_2002_clean.csv')


df_home = df_historica_data[['Home Team','Home goals', 'Away goals']]

df_away = df_historica_data[['Away Team','Home goals', 'Away goals']]


df_home = df_home.rename(columns={'Home Team':'Team', 'Home goals': 'Goles convertidos','Away goals':'Goles recibidos'})

df_away = df_away.rename(columns={'Away Team':'Team', 'Home goals': 'Goles recibidos','Away goals':'Goles convertidos'})

promedio = pd.concat([df_away,df_home], ignore_index=True).groupby('Team').mean()

def predict_points(homes,aways):
    if homes in promedio.index and aways in promedio.index:
        lamb_home= promedio.at[homes,'Goles convertidos'] * promedio.at[aways, 'Goles recibidos']
        lamb_away= promedio.at[aways,'Goles convertidos'] * promedio.at[homes, 'Goles recibidos']
        prob_home, prob_away, prob_tie = 0, 0, 0
        for x in range(0,11):
            for y in range(0,11):
                p= poisson.pmf(x, lamb_home)* poisson.pmf(y, lamb_away)
                if x==y:
                    prob_tie += p
                elif x >y:
                    prob_home += p
                else:
                    prob_away += p
        points_home = 3 * prob_home + prob_tie
        points_away = 3 * prob_away + prob_tie
        return  points_home, points_away 
    else:
        return (0,0)

        
df_fixture_48= df_fixture[:48].copy()

df_fixture_8vp= df_fixture[48:56].copy()

df_fixture_4to= df_fixture[56:60].copy()

df_fixture_semi= df_fixture[60:62].copy()

df_fixture_final= df_fixture[62:].copy()



for grupo in dict_table:
    teams_in_group= dict_table[grupo]['Team'].values
    df_fixture_gruop_6= df_fixture_48[df_fixture_48['home'].isin(teams_in_group)]
    for index, row in df_fixture_gruop_6.iterrows():
        homes, aways = row['home'], row['away']
        points_home, points_away = predict_points(homes, aways)
        dict_table[grupo].loc[dict_table[grupo]['Team'] == homes , 'Pts'] += points_home
        dict_table[grupo].loc[dict_table[grupo]['Team'] == aways , 'Pts'] += points_away

    dict_table[grupo] =dict_table[grupo].sort_values('Pts', ascending=False).reset_index()
    dict_table[grupo] =dict_table[grupo][['Team', 'Pts']]
    dict_table[grupo] =dict_table[grupo].round(0)


for grupo in dict_table:
    group_winner = dict_table[grupo].loc[0,'Team']
    runners_up = dict_table[grupo].loc[1,'Team']
    df_fixture_8vp.replace({f'Winners {grupo}': group_winner, f'Runners-up {grupo}': runners_up}, inplace=True)
    df_fixture_8vp['Winner'] = '?'



def get_winner(df_fixture_updated):
    for index, row in df_fixture_updated.iterrows():
        homes, aways = row['home'], row['away']     
        points_home, points_away = predict_points(homes,aways)
        if points_home>points_away:
            winner=homes
        else:
            winner= aways
        df_fixture_updated.loc[index, 'Winner'] = winner
    return  df_fixture_updated

get_winner(df_fixture_8vp)



def update_table (df_fixture_8, df_fixture_4):
    for index, row in df_fixture_8.iterrows():
        winner = df_fixture_8.loc[index, 'Winner']
        match = df_fixture_8.loc[index, 'score']
        df_fixture_4.replace({f'Winners {match}': winner}, inplace=True)
        df_fixture_4['Winner'] = '?'
    return df_fixture_4




update_table(df_fixture_8vp,df_fixture_4to)

get_winner(df_fixture_4to)



update_table(df_fixture_4to, df_fixture_semi)

get_winner(df_fixture_semi)

update_table(df_fixture_semi, df_fixture_final)

get_winner(df_fixture_final)



print(get_winner(df_fixture_8vp))
print(get_winner(df_fixture_4to))
print(get_winner(df_fixture_semi))
print(get_winner(df_fixture_final))
