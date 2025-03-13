from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

def load_data():
    files = ['Match.csv', 'Player.csv', 'Player_Attributes.csv', 'Team.csv', 'Team_Attributes.csv', 'Country.csv', 'League.csv']
    data = {}

    for file in files:
        if os.path.exists(file):
            data[file.split('.')[0]] = pd.read_csv(file)
        else:
            print(f"⚠ Le fichier {file} est introuvable.")
    
    return data

data = load_data()

data['Player']['weight'] = data['Player']['weight'].apply(lambda x: round(x * 0.453592, 2))
data['Player_Attributes'] = data['Player_Attributes'][data['Player_Attributes']['attacking_work_rate'].isin(['low', 'medium', 'high'])]
data['Player_Attributes'] = data['Player_Attributes'][data['Player_Attributes']['defensive_work_rate'].isin(['low', 'medium', 'high'])]

# Supprimer les colonnes goal, shoton, shotoff, foulcommit, card, cross, corner, possession, PSH, PSD, PSA, SJH, SJD, SJA, GBH, GBD, GBA, BSH, BSD, BSA de "Match"
if 'Match' in data:
    data['Match'] = data['Match'].drop(columns=['goal', 'shoton', 'shotoff', 'foulcommit', 'card', 'cross', 'corner', 'possession', 'PSH', 'PSD', 'PSA', 'SJH', 'SJD', 'SJA', 'GBH', 'GBD', 'GBA', 'BSH', 'BSD', 'BSA'])
    # Supprimer les lignes avec des valeurs manquantes
    data['Match'] = data['Match'].dropna()

if 'Team_Attributes' in data:
    data['Team_Attributes'] = data['Team_Attributes'].drop(columns=['buildUpPlayDribbling'])
    # Supprimer les lignes avec des valeurs manquantes
    data['Team_Attributes'] = data['Team_Attributes'].dropna() 

# Supprimer les lignes vides
if 'Team' in data :
    data['Team'] = data['Team'].dropna() 
if 'Player' in data :
    data['Player'] = data['Player'].dropna()
if 'Player_Attributes' in data :
    data['Player_Attributes'] = data['Player_Attributes'].dropna()
if 'Country' in data :
    data['Country'] = data['Country'].dropna()
if 'League' in data :
    data['League'] = data['League'].dropna()

match_df = data['Match']
player_df = data['Player']
player_attributes_df = data['Player_Attributes']
team_df = data['Team']
team_attributes_df = data['Team_Attributes']
country_df = data['Country']
league_df = data['League']

@app.route('/repartition_domicile_ext')
def repartition_domicile_ext():
    # Créer une colonne indiquant si l'équipe à domicile ou l'équipe à l'extérieur a marqué le plus de buts
    match_df['result'] = match_df.apply(lambda row: 'Home' if row['home_team_goal'] > row['away_team_goal'] 
                                    else ('Away' if row['home_team_goal'] < row['away_team_goal'] else 'Draw'), axis=1)

    # Compter les occurrences de chaque résultat
    result_counts = match_df['result'].value_counts().reset_index()
    result_counts.columns = ['Result', 'Count']

    # Créer le graphique interactif avec Plotly
    fig = px.pie(result_counts, values='Count', names='Result', 
                title="Répartition des résultats des matchs (domicile, extérieur, égalité)",
                color_discrete_map={'Home': 'lightgreen', 'Away': 'lightcoral', 'Draw': 'lightblue'})

    # Afficher le graphique
    fig.show()

@app.route('/carte_but_league')
def carte_but_league():
    # Charger la carte du monde depuis une source externe
    world = gpd.read_file("https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip")

    # Calculer le nombre total de buts par pays
    match_df['total_goals'] = match_df['home_team_goal'] + match_df['away_team_goal']
    goal_count = match_df.groupby('country_id')['total_goals'].sum().reset_index()
    goal_count.columns = ['country_id', 'goal_count']

    # Fusionner avec les noms des pays
    goal_count = goal_count.merge(country_df, left_on='country_id', right_on='id')[['name', 'goal_count']]

    # Correction du nom "England" → "United Kingdom" pour correspondre à la carte
    goal_count.loc[goal_count['name'] == 'England', 'name'] = 'United Kingdom'

    # Liste des pays européens à conserver
    european_countries = [
        'France', 'Germany', 'Italy', 'Spain', 'United Kingdom', 'Netherlands', 'Belgium', 'Portugal', 
        'Switzerland', 'Austria', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Poland', 'Czech Republic', 
        'Hungary', 'Slovakia', 'Slovenia', 'Croatia', 'Serbia', 'Bosnia and Herzegovina', 'Montenegro', 
        'Albania', 'Greece', 'Romania', 'Bulgaria', 'Ukraine', 'Ireland', 'Iceland', 'Lithuania', 
        'Latvia', 'Estonia'
    ]

    # Filtrer la carte pour afficher uniquement l'Europe
    world = world[world['NAME'].isin(european_countries)]

    # Fusionner les données de buts avec la carte
    world = world.merge(goal_count, left_on='NAME', right_on='name', how='left')
    world['goal_count'] = world['goal_count'].fillna(0)  # Remplacer NaN par 0

    # Créer la carte interactive avec Plotly
    fig = px.choropleth(
        world, 
        geojson=world.geometry, 
        locations=world.index, 
        color="goal_count",
        hover_name="NAME",
        hover_data={"goal_count": True},
        title="Répartition des buts par pays en Europe",
        color_continuous_scale="Reds",
        projection="natural earth"
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.show()

    return fig

@app.route('/pca_team_attributes')
def pca_team_attributes():
    # Étape 1 : Sélectionner les colonnes pertinentes
    # Exclure les colonnes non numériques ou non pertinentes (comme 'id', 'team_fifa_api_id', 'team_api_id', 'date')
    attributes = team_attributes_df.select_dtypes(include=[np.number]).columns.tolist()
    attributes = [attr for attr in attributes if attr not in ['id', 'team_fifa_api_id', 'team_api_id', 'date', 'buildUpPlaySpeedClass', 'buildUpPlayDribblingClass', 'buildUpPlayPassingClass', 'buildUpPlayPositioningClass', 'chanceCreationPassingClass', 'chanceCreationCrossingClass', 'chanceCreationShootingClass', 'chanceCreationPositioningClass', 'defencePressureClass', 'defenceAggressionClass', 'defenceTeamWidthClass']]

    # Extraire les données pertinentes
    X = team_attributes_df[attributes]

    # Gérer les valeurs manquantes (par exemple, remplacer par la médiane)
    X = X.fillna(X.median())

    # Standardiser les données (moyenne = 0, écart-type = 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Étape 2 : Appliquer l'ACP
    pca = PCA(n_components=2)  # Choisir 2 composantes principales pour la visualisation 2D
    X_pca = pca.fit_transform(X_scaled)

    # Étape 3 : Calculer les corrélations entre les variables et les composantes principales
    # Les composantes principales sont déjà standardisées (car les données ont été standardisées)
    correlations = np.corrcoef(X_scaled.T, X_pca.T)[:len(attributes), len(attributes):]

    # Créer un DataFrame pour les corrélations
    correlations_df = pd.DataFrame(correlations, columns=['PC1', 'PC2'], index=attributes)

    # Étape 4 : Tracer le cercle des corrélations
    plt.figure(figsize=(8, 8))
    ax = plt.gca()

    # Tracer un cercle de rayon 1
    circle = plt.Circle((0, 0), 1, color='blue', fill=False)
    ax.add_artist(circle)

    # Tracer les flèches (vecteurs) pour chaque variable
    for i, var in enumerate(attributes):
        plt.arrow(0, 0, correlations_df.loc[var, 'PC1'], correlations_df.loc[var, 'PC2'], 
                head_width=0.05, head_length=0.05, color='red')
        plt.text(correlations_df.loc[var, 'PC1'] * 1.1, correlations_df.loc[var, 'PC2'] * 1.1, var, color='black')

    # Ajouter des lignes horizontales et verticales pour le centre
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')

    # Ajuster les limites du graphique
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1)

    # Ajouter des labels et un titre
    plt.xlabel('Composante Principale 1 (PC1)')
    plt.ylabel('Composante Principale 2 (PC2)')
    plt.title('Cercle des corrélations')
    plt.show()

if __name__ == '__main__':
    app.run(debug=True)