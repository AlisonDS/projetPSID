from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
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

    # Étape 6 : Création du graphique interactif avec filtres
    fig = px.box(
        player_with_country,
        x='name',
        y='age',
        color='name',
        title="Distribution des âges des joueurs par pays",
        labels={"name": "Pays", "age": "Âge"},
        hover_data=['age'],
    )
    fig.show()

    # Création de l'histogramme interactif
    fig = px.histogram(
        player_with_country, 
        x="age", 
        nbins=30, 
        marginal="box",  # Ajoute un boxplot en haut pour plus de détails
        opacity=0.75, 
        color_discrete_sequence=["blue"], 
        title="Distribution des âges des joueurs",
        labels={"age": "Âge", "count": "Nombre de joueurs"}
    )

    # Amélioration de l'affichage
    fig.update_layout(
        xaxis_title="Âge",
        yaxis_title="Nombre de joueurs",
        bargap=0.05,  # Réduction de l'écart entre les barres pour un meilleur rendu
        hovermode="x unified"  # Affichage des valeurs au survol
    )

    # Affichage du graphique interactif
    fig.show()

@app.route('/taille_poids_joueurs')
def taille_poids_joueurs():
    global player_df, player_attributes_df  # Utilise les variables globales

    # Vérifier les colonnes disponibles
    print("Colonnes dans player_attributes_df:", player_attributes_df.columns)

    # Vérifier les premières lignes des colonnes work rate
    print(player_attributes_df[['attacking_work_rate', 'defensive_work_rate']].head())

    # Vérifier les valeurs uniques
    print("Valeurs uniques dans attacking_work_rate:", player_attributes_df['attacking_work_rate'].unique())
    print("Valeurs uniques dans defensive_work_rate:", player_attributes_df['defensive_work_rate'].unique())

    # Nettoyer les données : supprimer les espaces et standardiser la casse
    player_attributes_df['attacking_work_rate'] = player_attributes_df['attacking_work_rate'].str.strip().str.title()
    player_attributes_df['defensive_work_rate'] = player_attributes_df['defensive_work_rate'].str.strip().str.title()

    # Vérifier les valeurs manquantes
    print("Valeurs manquantes dans attacking_work_rate:", player_attributes_df['attacking_work_rate'].isna().sum())
    print("Valeurs manquantes dans defensive_work_rate:", player_attributes_df['defensive_work_rate'].isna().sum())

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

    # Afficher les données moyennes
    print(size_data)

    # Visualisation
    plt.figure(figsize=(14, 6))

    # Graphique pour la taille moyenne
    plt.subplot(1, 2, 1)
    sns.barplot(x='work_rate', y='height', hue='work_rate_type', data=size_data, palette='coolwarm')
    plt.title('Taille moyenne des joueurs\npar Attacking et Defensive Work Rate')
    plt.ylabel('Taille moyenne (cm)')
    plt.xlabel('Work Rate')
    plt.legend(title='Type de Work Rate', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Graphique pour le poids moyen
    plt.subplot(1, 2, 2)
    sns.barplot(x='work_rate', y='weight', hue='work_rate_type', data=size_data, palette='coolwarm')
    plt.title('Poids moyen des joueurs\npar Attacking et Defensive Work Rate')
    plt.ylabel('Poids moyen (kg)')
    plt.xlabel('Work Rate')
    plt.legend(title='Type de Work Rate', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()


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

    # Vérifier si les catégories sont bien présentes
    print("Nombre de joueurs par catégorie:")
    print(merged_df["profile"].value_counts())

    # Sélection des métriques importantes
    metrics = ['finishing', 'positioning', 'acceleration', 'standing_tackle', 'marking', 'strength']

    # Vérifier s'il y a bien des joueurs dans chaque catégorie
    average_profiles = merged_df.groupby("profile")[metrics].mean().reset_index()
    print("Catégories présentes dans average_profiles:", average_profiles["profile"].unique())

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

    # Réduction de l'échelle
    fig.update_layout(
        title="Comparaison des Profils Joueurs (Attaquant, Défenseur, Moyenne Générale)",
        polar=dict(radialaxis=dict(visible=True, range=[0, 1.6])),
        showlegend=True
    )

    fig.show()

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

    # Afficher le graphique interactif
    fig.show()

# NE PAS OUBLIER !!!!!!!!!!!!!!!!!!!!!!!!!!!
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
    fig.show()

if __name__ == '__main__':
    app.run(debug=True)
