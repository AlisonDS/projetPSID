from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from io import BytesIO
import base64
import io
import os

app = Flask(__name__)
CORS(app)

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

# Fonction de conversion récursive
def convert_ndarray(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Si c'est un ndarray, on le convertit en liste
    elif isinstance(obj, dict):
        return {key: convert_ndarray(value) for key, value in obj.items()}  # Si c'est un dict, on applique la conversion à chaque valeur
    elif isinstance(obj, list):
        return [convert_ndarray(item) for item in obj]  # Si c'est une liste, on applique la conversion à chaque élément
    return obj  # Sinon, on laisse l'objet tel quel

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

    # Convertir le graphique en dictionnaire et le retourner comme JSON
    fig_dict = fig.to_dict()  # Conversion en dictionnaire Plotly
    fig_dict = convert_ndarray(fig_dict)  # Appliquer la conversion des ndarrays en listes
    return jsonify(fig_dict)


@app.route('/carte_but_league')
def carte_but_league():
    # Charger la carte du monde
    world = gpd.read_file("https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip")

    # Calcul du nombre total de buts par pays
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
        geojson=world.geometry,  # Assurez-vous que les données GeoJSON sont correctement liées
        locations=world.index, 
        color="goal_count",
        hover_name="NAME",
        hover_data={"goal_count": True},
        title="Répartition des buts par pays en Europe",
        color_continuous_scale="Reds",
        projection="natural earth"
    )

    fig.update_geos(fitbounds="locations", visible=False, projection_type="natural earth", showcoastlines=True)

    # Lorsque tu prépares ta figure Plotly, applique la conversion
    fig_dict = convert_ndarray(fig.to_dict())

    # Maintenant, retourne fig_dict comme réponse
    return jsonify(fig_dict)

@app.route('/pca_team_attributes')
def pca_team_attributes():
    # Étape 1 : Sélectionner les colonnes pertinentes
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

    # Convertir le graphique en image PNG dans un buffer en mémoire
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    # Encoder l'image en base64
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    # Retourner l'image encodée en base64 dans la réponse
    return jsonify({'image': f'data:image/png;base64,{img_base64}'})

@app.route('/pca_position')
def pca_position():
    # Fusion des tables pour associer les équipes à leur pays
    team_with_country = pd.merge(
        team_df,
        match_df[['home_team_api_id', 'country_id']].rename(columns={'home_team_api_id': 'team_api_id'}),
        on='team_api_id',
        how='left'
    )

    if 'country_id' not in country_df.columns:
        country_df.rename(columns={'id': 'country_id'}, inplace=True)

    team_with_country = pd.merge(team_with_country, country_df, on='country_id')
    team_with_attributes = pd.merge(team_with_country, team_attributes_df, on='team_api_id')

    # Sélection des colonnes pertinentes
    attributes = team_with_attributes.select_dtypes(include=[np.number]).columns.tolist()
    attributes = [attr for attr in attributes if attr not in ['id', 'team_fifa_api_id', 'team_api_id', 'date']]

    # Extraction et standardisation des données
    X = team_with_attributes[attributes].fillna(team_with_attributes[attributes].median())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ACP avec 2 composantes principales
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Création du DataFrame avec les résultats de l'ACP
    pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
    pca_df['country'] = team_with_attributes['name']
    pca_df['team_name'] = team_with_attributes['team_short_name']

    # Création du graphique Plotly
    fig = px.scatter(
        pca_df, 
        x='PC1', 
        y='PC2', 
        color='country', 
        hover_data=['team_name'], 
        title="ACP des équipes colorées par pays"
    )

    # Extraire les données du graphique sous forme de dictionnaire
    plot_data = fig.to_dict()

    # Appliquer la fonction convert_ndarray pour convertir tous les ndarray en listes
    plot_data_converted = convert_ndarray(plot_data)

    # Retourner les données converties dans la réponse JSON
    return jsonify({'plotData': plot_data_converted})

@app.route('/pays_age')
def pays_age():
    global country_df, player_df, match_df  # Utilise les variables globales

    # Vérifier si 'id' existe dans les colonnes de `country_df`, renommer la colonne
    if 'id' in country_df.columns:
        country_df = country_df.rename(columns={'id': 'country_id'})

    # Étape 1 : Convertir les colonnes de date en datetime
    player_df['birthday'] = pd.to_datetime(player_df['birthday'])
    match_df['date'] = pd.to_datetime(match_df['date'])

    # Étape 2 : Extraire les joueurs et leur pays à partir de la table match
    home_players = match_df[['date', 'country_id'] + [f'home_player_{i}' for i in range(1, 12)]]
    away_players = match_df[['date', 'country_id'] + [f'away_player_{i}' for i in range(1, 12)]]

    # Renommer les colonnes pour faciliter la fusion
    home_players = home_players.melt(id_vars=['date', 'country_id'], value_name='player_api_id').drop(columns='variable')
    away_players = away_players.melt(id_vars=['date', 'country_id'], value_name='player_api_id').drop(columns='variable')

    # Combiner les joueurs domicile et extérieur
    all_players = pd.concat([home_players, away_players], ignore_index=True)
    all_players.dropna(subset=['player_api_id'], inplace=True)

    # Étape 3 : Fusionner avec la table player pour obtenir la date de naissance des joueurs
    player_with_birthday = pd.merge(all_players, player_df[['player_api_id', 'birthday']], on='player_api_id')

    # Étape 4 : Calculer l'âge des joueurs au moment du match
    player_with_birthday['age'] = (player_with_birthday['date'] - player_with_birthday['birthday']).dt.days / 365.25

    # Étape 5 : Fusionner avec la table country pour obtenir le nom du pays
    player_with_country = pd.merge(player_with_birthday, country_df, on='country_id')

    # Vérification après la fusion
    print(player_with_country.head())

    # Étape 6 : Création du graphique boxplot avec filtres
    fig_boxplot = px.box(
        player_with_country,
        x='name',
        y='age',
        color='name',
        title="Distribution des âges des joueurs par pays",
        labels={"name": "Pays", "age": "Âge"},
        hover_data=['age'],
    )
    fig_boxplot_dict = fig_boxplot.to_dict()
    fig_boxplot_dict = convert_ndarray(fig_boxplot_dict)  # Applique la conversion des ndarrays en listes

    # Création de l'histogramme interactif
    fig_histogram = px.histogram(
        player_with_country, 
        x="age", 
        nbins=30, 
        marginal="box",  # Ajoute un boxplot en haut pour plus de détails
        opacity=0.75, 
        color_discrete_sequence=["blue"], 
        title="Distribution des âges des joueurs",
        labels={"age": "Âge", "count": "Nombre de joueurs"}
    )
    fig_histogram_dict = fig_histogram.to_dict()
    fig_histogram_dict = convert_ndarray(fig_histogram_dict)  # Applique la conversion des ndarrays en listes

    # Retourner les deux graphiques sous forme de JSON
    return jsonify({
        "boxplot": fig_boxplot_dict,
        "histogram": fig_histogram_dict
    })

@app.route('/taille_poids_joueurs')
def taille_poids_joueurs():
    global player_df, player_attributes_df  # Utilise les variables globales

    # Vérifier les colonnes disponibles
    print("Colonnes dans player_attributes_df:", player_attributes_df.columns)

    # Nettoyer les données : supprimer les espaces et standardiser la casse
    player_attributes_df['attacking_work_rate'] = player_attributes_df['attacking_work_rate'].str.strip().str.title()
    player_attributes_df['defensive_work_rate'] = player_attributes_df['defensive_work_rate'].str.strip().str.title()

    # Supprimer les lignes avec des valeurs manquantes
    player_attributes_df = player_attributes_df.dropna(subset=['attacking_work_rate', 'defensive_work_rate'])

    # Fusionner les données sur player_api_id
    merged_data = pd.merge(player_df, player_attributes_df, on='player_api_id')

    # Calculer les moyennes de taille et poids par attacking_work_rate et defensive_work_rate
    attacking_avg = merged_data.groupby('attacking_work_rate').agg({
        'height': 'mean',
        'weight': 'mean'
    }).reset_index()
    attacking_avg['work_rate_type'] = 'Attacking'  # Ajouter une colonne pour le type de work rate

    defensive_avg = merged_data.groupby('defensive_work_rate').agg({
        'height': 'mean',
        'weight': 'mean'
    }).reset_index()
    defensive_avg['work_rate_type'] = 'Defensive'  # Ajouter une colonne pour le type de work rate

    # Renommer les colonnes pour fusionner les données
    attacking_avg = attacking_avg.rename(columns={'attacking_work_rate': 'work_rate'})
    defensive_avg = defensive_avg.rename(columns={'defensive_work_rate': 'work_rate'})

    # Fusionner les données pour la taille et le poids
    size_data = pd.concat([attacking_avg, defensive_avg])
    size_data['work_rate'] = pd.Categorical(size_data['work_rate'], categories=['Low', 'Medium', 'High'], ordered=True)  # Ordonner les catégories

    # Convertir les objets ndarray en liste
    size_data_converted = convert_ndarray(size_data.to_dict(orient='records'))

    # Retourner les données converties dans la réponse JSON
    return jsonify({'sizeData': size_data_converted})


import plotly.graph_objects as go
from flask import jsonify

@app.route('/Comparaison_joueurs')
def comparaison_joueurs():
    # Fusionner les données des joueurs avec leurs attributs
    merged_df = pd.merge(player_df, player_attributes_df, on="player_api_id")

    # Nettoyage des colonnes work rate
    merged_df["attacking_work_rate"] = merged_df["attacking_work_rate"].str.strip().str.lower()
    merged_df["defensive_work_rate"] = merged_df["defensive_work_rate"].str.strip().str.lower()

    # Nouvelle catégorisation des joueurs
    merged_df["profile"] = "Moyenne Générale"
    merged_df.loc[
        merged_df["attacking_work_rate"].isin(["high"]) & merged_df["defensive_work_rate"].isin(["low"]),
        "profile"
    ] = "Attaquant"
    merged_df.loc[
        merged_df["defensive_work_rate"].isin(["high"]) & merged_df["attacking_work_rate"].isin(["low"]),
        "profile"
    ] = "Défenseur"

    # Sélection des métriques importantes
    metrics = ['finishing', 'positioning', 'acceleration', 'standing_tackle', 'marking', 'strength']

    # Moyennes des métriques par profil
    average_profiles = merged_df.groupby("profile")[metrics].mean().reset_index()

    # Normalisation entre 0 et 1
    for metric in metrics:
        min_val = merged_df[metric].min()
        max_val = merged_df[metric].max()
        if max_val > min_val:  # Éviter la division par zéro
            average_profiles[metric] = (average_profiles[metric] - min_val) / (max_val - min_val)

    # Amplification des écarts pour plus de visibilité
    scale_factor = 2
    average_profiles[metrics] = average_profiles[metrics] * scale_factor

    # Création du radar chart
    fig = go.Figure()

    for _, row in average_profiles.iterrows():
        values = row[metrics].tolist()
        values += values[:1]  # Boucler pour fermer le radar chart
        metrics_with_closure = metrics + [metrics[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=metrics_with_closure,
            fill='toself',
            name=row["profile"]
        ))

    # Conversion en JSON
    fig_dict = fig.to_dict()
    fig_dict = convert_ndarray(fig_dict)  # Conversion des ndarray en liste
    return jsonify(fig_dict)

import plotly.express as px
from flask import jsonify

@app.route('/overall_rating')
def overall_rating():

    # Vérifier les colonnes de country_df
    print(country_df.columns)

    # S'assurer que la colonne 'id' existe bien, sinon l'adapter
    if 'id' not in country_df.columns:
        country_df.rename(columns={'country_id': 'id'}, inplace=True)

    # Fusionner les matchs avec la table des pays
    matches_with_country = match_df.merge(country_df, left_on='country_id', right_on='id', how='left')

    # Fusionner avec les joueurs pour récupérer leur overall_rating
    players_with_ratings = player_attributes_df[['player_api_id', 'overall_rating']]

    # Associer les joueurs aux matchs via les identifiants des joueurs (home et away)
    player_columns = [f"home_player_{i}" for i in range(1, 12)] + [f"away_player_{i}" for i in range(1, 12)]
    matches_with_ratings = matches_with_country.melt(id_vars=["country_id", "name"], 
                                                    value_vars=player_columns,
                                                    var_name="player_position", 
                                                    value_name="player_api_id")

    matches_with_ratings = matches_with_ratings.merge(players_with_ratings, on="player_api_id", how="left")

    # Calculer la moyenne du rating des joueurs par pays
    average_rating_by_country = matches_with_ratings.groupby('name')['overall_rating'].mean().reset_index()

    # 🎨 Visualisation interactive avec Plotly
    fig = px.bar(
        average_rating_by_country, 
        x='name', 
        y='overall_rating', 
        color='overall_rating', 
        title="Moyenne de l'Overall Rating des joueurs par Pays",
        labels={"name": "Pays", "overall_rating": "Note Globale Moyenne"},
        color_continuous_scale="viridis"
    )

    # Améliorer l'affichage
    fig.update_layout(xaxis=dict(title="Pays", tickangle=-45), yaxis=dict(title="Note Globale Moyenne"))

    # Conversion en JSON
    fig_dict = fig.to_dict()
    fig_dict = convert_ndarray(fig_dict)  # Conversion des ndarray en liste
    return jsonify(fig_dict)


@app.route('/Bookmakers')
def Bookmakers():
    global match_df  # Utilise la variable globale match_df

    # Liste des colonnes des bookmakers pour chaque issue
    bookmakers = ['B365', 'BW', 'IW', 'LB', 'WH', 'VC']
    columns_H = [f"{b}H" for b in bookmakers]
    columns_D = [f"{b}D" for b in bookmakers]
    columns_A = [f"{b}A" for b in bookmakers]

    # Vérifier que toutes les colonnes existent dans le dataset
    all_columns = columns_H + columns_D + columns_A
    match_df = match_df.dropna(subset=all_columns)

    # Calculer la moyenne des cotes pour chaque issue
    match_df['Avg_H'] = match_df[columns_H].mean(axis=1)
    match_df['Avg_D'] = match_df[columns_D].mean(axis=1)
    match_df['Avg_A'] = match_df[columns_A].mean(axis=1)

    # Calculer les probabilités implicites à partir des cotes moyennes
    match_df['P_H'] = 1 / match_df['Avg_H']
    match_df['P_D'] = 1 / match_df['Avg_D']
    match_df['P_A'] = 1 / match_df['Avg_A']

    # Normaliser pour que la somme des probabilités = 1
    total_prob = match_df[['P_H', 'P_D', 'P_A']].sum(axis=1)
    match_df['P_H_norm'] = match_df['P_H'] / total_prob
    match_df['P_D_norm'] = match_df['P_D'] / total_prob
    match_df['P_A_norm'] = match_df['P_A'] / total_prob

    # Déterminer les résultats réels
    match_df['result'] = np.where(
        match_df['home_team_goal'] > match_df['away_team_goal'], 'Home Win',
        np.where(match_df['home_team_goal'] == match_df['away_team_goal'], 'Draw', 'Away Win')
    )

    # Calculer les fréquences réelles des résultats
    real_freq = match_df['result'].value_counts(normalize=True).reindex(['Home Win', 'Draw', 'Away Win'], fill_value=0)

    # Calculer les probabilités moyennes prédites par les bookmakers
    predicted_freq = match_df[['P_H_norm', 'P_D_norm', 'P_A_norm']].mean()

    # Créer un DataFrame pour la visualisation
    comparison_df = pd.DataFrame({
        'Result': ['Home Win', 'Draw', 'Away Win'],
        'Real Frequency': real_freq.values,
        'Predicted Probability': predicted_freq.values
    })

    # 📊 Graphique interactif avec Plotly
    fig = px.bar(
        comparison_df.melt(id_vars='Result', var_name='Type', value_name='Probability'),
        x='Result',
        y='Probability',
        color='Type',
        barmode='group',
        title="Comparaison des Probabilités des Bookmakers vs Fréquences Réelles",
        labels={"Result": "Résultat du Match", "Probability": "Probabilité", "Type": "Source"},
    )

    fig.update_layout(xaxis_title="Résultat du Match", yaxis_title="Probabilité / Fréquence")

    # Conversion en JSON
    fig_dict = fig.to_dict()
    fig_dict = convert_ndarray(fig_dict)  # Conversion des ndarray en liste
    return jsonify(fig_dict)

    # MACHINE LEARNING :
@app.route('/api/countries')
def get_countries():
    # Assurer que la colonne 'country_id' existe bien
    if 'id' in country_df.columns:
        country_df.rename(columns={'id': 'country_id'}, inplace=True)

    countries = country_df[['country_id', 'name']].dropna().to_dict(orient='records')
    return jsonify(countries)

  
# Route pour récupérer la liste des équipes
# @app.route('/api/teams')
# def get_teams():
#     teams = team_df[['team_api_id', 'team_long_name', 'team_short_name']].to_dict(orient='records')
#     return jsonify(teams)

# # MACHINE LEARNING - Version mise à jour avec seulement les variables spécifiées
# # Préparer les données d'entraînement avec seulement les variables importantes
# selected_features = [
#     'buildUpPlaySpeed', 'buildUpPlayPassing', 'chanceCreationPassing', 
#     'chanceCreationCrossing', 'chanceCreationShooting', 'defencePressure', 
#     'defenceAggression', 'defenceTeamWidth'
# ]
@app.route('/api/teams')
def get_teams():
    country_id = request.args.get('country_id')  # récupère l'ID du pays si présent
       
    filtered_df = team_df.copy()
    if country_id:
        country_id = int(country_id)
        filtered_df = match_df[match_df['country_id'] == country_id][['home_team_api_id']].drop_duplicates()
        team_ids = filtered_df['home_team_api_id'].unique()
        filtered_df = team_df[team_df['team_api_id'].isin(team_ids)]
    
    teams = filtered_df[['team_api_id', 'team_long_name', 'team_short_name']].dropna().to_dict(orient='records')
    return jsonify(teams)

selected_features = [
    'buildUpPlaySpeed', 'buildUpPlayPassing', 'chanceCreationPassing', 
    'chanceCreationCrossing', 'chanceCreationShooting', 'defencePressure', 
    'defenceAggression', 'defenceTeamWidth'
]

# Fonction pour préparer les données d'un match
def prepare_match_data(home_team_id, away_team_id):
    # Récupérer les attributs des équipes
    home_team_attr = team_attributes_df[team_attributes_df['team_api_id'] == home_team_id][selected_features].iloc[0]
    away_team_attr = team_attributes_df[team_attributes_df['team_api_id'] == away_team_id][selected_features].iloc[0]
    
    # Renommer les colonnes pour distinguer domicile et extérieur
    home_features = {f'home_{col}': val for col, val in home_team_attr.items()}
    away_features = {f'away_{col}': val for col, val in away_team_attr.items()}
    
    # Combiner les caractéristiques
    match_features = {**home_features, **away_features}
    return pd.DataFrame([match_features])

# Préparer le dataset d'entraînement
match_data = []
home_scores = []
away_scores = []

for idx, match in match_df.iterrows():
    home_team_id = match['home_team_api_id']
    away_team_id = match['away_team_api_id']
    
    try:
        # Préparer les données du match
        features = prepare_match_data(home_team_id, away_team_id)
        match_data.append(features)
        
        # Ajouter les scores
        home_scores.append(match['home_team_goal'])
        away_scores.append(match['away_team_goal'])
    except (IndexError, KeyError):
        # Ignorer les matchs où les données sont manquantes
        continue

# Combiner tous les matchs en un seul DataFrame
if match_data:
    X = pd.concat(match_data, ignore_index=True)
    y_home = np.array(home_scores)
    y_away = np.array(away_scores)
    
    # Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
    _, _, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)
    
    # Entraîner les modèles Random Forest Regressor pour prédire les scores
    model_home = RandomForestRegressor(n_estimators=100, random_state=42)
    model_home.fit(X_train, y_train_home)
    
    model_away = RandomForestRegressor(n_estimators=100, random_state=42)
    model_away.fit(X_train, y_train_away)
else:
    print("Erreur: Aucune donnée de match valide n'a été trouvée.")

# Route pour prédire le score du match
@app.route('/api/predict', methods=['POST'])
def predict():
    # Récupère les données de la requête
    data = request.get_json()
    home_team_id = int(data['home_team'])
    away_team_id = int(data['away_team'])
    
    try:
        # Préparer les données du match pour la prédiction
        match_features = prepare_match_data(home_team_id, away_team_id)
        
        # Prédire les scores
        predicted_home_score = max(0, round(float(model_home.predict(match_features)[0]), 1))
        predicted_away_score = max(0, round(float(model_away.predict(match_features)[0]), 1))
        
        # Retourner les résultats de la prédiction
        return jsonify({
            "home_score": predicted_home_score,
            "away_score": predicted_away_score,
            "home_team_name": team_df[team_df['team_api_id'] == home_team_id]['team_long_name'].iloc[0],
            "away_team_name": team_df[team_df['team_api_id'] == away_team_id]['team_long_name'].iloc[0]
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Erreur lors de la prédiction du score. Vérifiez que les équipes sélectionnées ont des données complètes."
        }), 400

@app.route('/api/model_metrics')
def model_metrics():
    global X_test, y_test_home, y_test_away, model_home, model_away
    
    try:
        # Prédictions sur l'ensemble de test
        y_pred_home = model_home.predict(X_test)
        y_pred_away = model_away.predict(X_test)
        
        # Calculer les métriques pour le modèle de l'équipe à domicile
        mae_home = mean_absolute_error(y_test_home, y_pred_home)
        mse_home = mean_squared_error(y_test_home, y_pred_home)
        rmse_home = np.sqrt(mse_home)
        r2_home = r2_score(y_test_home, y_pred_home)
        
        # Calculer les métriques pour le modèle de l'équipe à l'extérieur
        mae_away = mean_absolute_error(y_test_away, y_pred_away)
        mse_away = mean_squared_error(y_test_away, y_pred_away)
        rmse_away = np.sqrt(mse_away)
        r2_away = r2_score(y_test_away, y_pred_away)
        
        # Préparation de la visualisation des résultats réels vs prédictions
        # Limiter à un échantillon pour ne pas surcharger le graphique
        sample_size = min(100, len(y_test_home))
        sample_indices = np.random.choice(len(y_test_home), sample_size, replace=False)
        
        # Préparer les données pour le graphique de comparaison
        comparison_data = {
            'index': list(range(sample_size)),
            'actual_home': y_test_home[sample_indices].tolist(),
            'predicted_home': y_pred_home[sample_indices].tolist(),
            'actual_away': y_test_away[sample_indices].tolist(),
            'predicted_away': y_pred_away[sample_indices].tolist()
        }
        
        # Création des graphiques Plotly
        # 1. Graphique pour les buts à domicile
        fig_home = px.scatter(
            x=comparison_data['actual_home'], 
            y=comparison_data['predicted_home'],
            labels={'x': 'Buts réels (domicile)', 'y': 'Buts prédits (domicile)'},
            title="Comparaison des buts réels vs prédits (équipe à domicile)"
        )
        
        # Ajouter une ligne de référence x=y pour montrer la prédiction parfaite
        fig_home.add_trace(
            go.Scatter(
                x=[min(comparison_data['actual_home']), max(comparison_data['actual_home'])],
                y=[min(comparison_data['actual_home']), max(comparison_data['actual_home'])],
                mode='lines',
                name='Prédiction parfaite',
                line=dict(color='red', dash='dash')
            )
        )
        
        # 2. Graphique pour les buts à l'extérieur
        fig_away = px.scatter(
            x=comparison_data['actual_away'], 
            y=comparison_data['predicted_away'],
            labels={'x': 'Buts réels (extérieur)', 'y': 'Buts prédits (extérieur)'},
            title="Comparaison des buts réels vs prédits (équipe à l'extérieur)"
        )
        
        # Ajouter une ligne de référence x=y pour montrer la prédiction parfaite
        fig_away.add_trace(
            go.Scatter(
                x=[min(comparison_data['actual_away']), max(comparison_data['actual_away'])],
                y=[min(comparison_data['actual_away']), max(comparison_data['actual_away'])],
                mode='lines',
                name='Prédiction parfaite',
                line=dict(color='red', dash='dash')
            )
        )
        
        # 3. Graphique de l'importance des variables pour le modèle domicile
        feature_importance_home = model_home.feature_importances_
        feature_names = X_test.columns
        
        importance_df_home = pd.DataFrame({
            'feature': feature_names,
            'importance': feature_importance_home
        }).sort_values('importance', ascending=False)
        
        fig_importance_home = px.bar(
            importance_df_home.head(10),
            x='importance',
            y='feature',
            orientation='h',
            title="Importance des variables (modèle domicile)",
            labels={'importance': 'Importance', 'feature': 'Variable'}
        )
        
        # 4. Graphique de l'importance des variables pour le modèle extérieur
        feature_importance_away = model_away.feature_importances_
        
        importance_df_away = pd.DataFrame({
            'feature': feature_names,
            'importance': feature_importance_away
        }).sort_values('importance', ascending=False)
        
        fig_importance_away = px.bar(
            importance_df_away.head(10),
            x='importance',
            y='feature',
            orientation='h',
            title="Importance des variables (modèle extérieur)",
            labels={'importance': 'Importance', 'feature': 'Variable'}
        )
        
        # Convertir les graphiques en dictionnaires
        fig_home_dict = convert_ndarray(fig_home.to_dict())
        fig_away_dict = convert_ndarray(fig_away.to_dict())
        fig_importance_home_dict = convert_ndarray(fig_importance_home.to_dict())
        fig_importance_away_dict = convert_ndarray(fig_importance_away.to_dict())
        
        # Métriques générales sur le jeu de données
        train_size = len(X_train)
        test_size = len(X_test)
        total_size = train_size + test_size
        train_ratio = train_size / total_size * 100
        test_ratio = test_size / total_size * 100
        
        # Retourner toutes les informations
        return jsonify({
            'metrics': {
                'home_model': {
                    'mae': mae_home,
                    'mse': mse_home,
                    'rmse': rmse_home,
                    'r2': r2_home
                },
                'away_model': {
                    'mae': mae_away,
                    'mse': mse_away,
                    'rmse': rmse_away,
                    'r2': r2_away
                }
            },
            'dataset_info': {
                'train_size': train_size,
                'test_size': test_size,
                'total_size': total_size,
                'train_ratio': train_ratio,
                'test_ratio': test_ratio
            },
            'plots': {
                'home_comparison': fig_home_dict,
                'away_comparison': fig_away_dict,
                'home_importance': fig_importance_home_dict,
                'away_importance': fig_importance_away_dict
            }
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Erreur lors du calcul des métriques du modèle'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
