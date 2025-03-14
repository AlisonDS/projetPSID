import React, { useState } from "react";
import FootballMap from "./components/FootballMap";
import RepartitionDomicileExt from "./components/RepartitionDomicileExt";
import PcaTeamAttributes from "./components/PcaTeamAttributes";
import PcaPosition from "./components/PcaPosition";
import PaysAgeGraph from "./components/PaysAgeGraph";
import TaillePoidsJoueurs from "./components/TaillePoids";
import ComparaisonJoueursGraph from "./components/ComparaisonJoueursGraph";
import OverallRatingGraph from "./components/OverallRatingGraphGraph";
import BookmakersGraph from "./components/BookmakersGraph";
import "./App.css";
 
import Footer from "./components/Footer"; 

function App() {
    const [activeTab, setActiveTab] = useState("Dashboard"); // Dashboard par défaut

    return (
        <div className="App">
            {/* Barre de navigation */}
            <nav className="navbar">
                <ul>
                    <li className={activeTab === "Accueil" ? "active" : ""} onClick={() => setActiveTab("Accueil")}>
                        Accueil
                    </li>
                    <li className={activeTab === "Modèle ML" ? "active" : ""} onClick={() => setActiveTab("Modèle ML")}>
                        Modèle ML
                    </li>
                    <li className={activeTab === "Dashboard" ? "active" : ""} onClick={() => setActiveTab("Dashboard")}>
                        Dashboard
                    </li>
                </ul>
            </nav>
            {activeTab === "Accueil" && (
                <div className="home-container">
                    <h1>📊 Projet Football Data - Prédiction des Scores</h1>

                    <section>
                        <h2>⚽ Contexte</h2>
                        <p>
                            Le football est l'un des sports les plus suivis au monde, et la prédiction des résultats 
                            des matchs est un défi passionnant qui combine statistiques, analyse de données et 
                            intelligence artificielle. Grâce aux avancées technologiques et à l'exploitation des 
                            données sportives, il est possible d'identifier des tendances et d'améliorer la précision 
                            des prévisions sur les performances des équipes.
                        </p>
                    </section>

                    <section>
                        <h2>🎯 Objectifs</h2>
                        <p>
                            L’objectif principal de ce projet est de démontrer comment l’analyse de données et le 
                            machine learning peuvent être utilisés pour prédire les scores des matchs de football 
                            avec précision.
                        </p>
                        <ul>
                            <li>📌 Collecter et nettoyer les données pour garantir leur fiabilité.</li>
                            <li>📌 Explorer et visualiser les tendances pour mieux comprendre les performances des équipes.</li>
                            <li>📌 Développer et tester des modèles prédictifs pour estimer les scores des matchs.</li>
                            <li>📌 Proposer des analyses exploitables pour affiner les stratégies de pronostics.</li>
                        </ul>
                    </section>

                    <section>
                        <h2>🛠️ Solution</h2>
                        <p>
                            Pour répondre à ces objectifs, le projet suit plusieurs étapes clés :
                        </p>
                        <ol>
                            <li>📂 <strong>Exploration et préparation des données :</strong> Sélectionner les données pertinentes 
                            (scores passés, statistiques des équipes, performances des joueurs, etc.) et assurer leur qualité.</li>
                            <li>📊 <strong>Analyse des données :</strong> Identifier les tendances, les facteurs clés influençant 
                            les résultats et établir des visualisations claires.</li>
                            <li>🤖 <strong>Modélisation prédictive :</strong> Utiliser des algorithmes de machine learning 
                            pour prédire les scores des matchs.</li>
                            <li>📈 <strong>Interprétation des résultats :</strong> Traduire les prédictions en recommandations 
                            exploitables pour améliorer la compréhension des performances des équipes.</li>
                        </ol>
                    </section>

                    <section>
                        <h2>📊 Données Utilisées</h2>
                        <p>
                            Les données exploitées pour ce projet proviennent de la base de données disponible sur Kaggle. 
                            Ce jeu de données couvre la saison 2024-2025 et contient des informations détaillées sur 
                            les joueurs et les performances des équipes :
                        </p>
                        <ul>
                            <li>📌 Statistiques individuelles des joueurs (buts, passes, minutes jouées, etc.).</li>
                            <li>📌 Résultats des matchs et performances collectives.</li>
                            <li>📌 Données avancées sur les métriques physiques et tactiques.</li>
                        </ul>
                        <p>Ces informations sont essentielles pour identifier les facteurs influençant les scores et affiner les modèles prédictifs.</p>
                    </section>
                    <Footer />
                   
                </div>
            )}
            {/* Contenu dynamique selon le menu sélectionné */}
            {activeTab === "Dashboard" && (
                <>
                    
                    <RepartitionDomicileExt />
                    <h2>Répartition des buts par pays en Europe</h2>
                    <FootballMap />
                    
                    {/* Section PCA avec style réduit */}
                    <div className="chart-container">
                        <PcaTeamAttributes />
                    </div>
                    <div className="chart-container">
                        <PcaPosition />
                    </div>

                    <PaysAgeGraph />
                    <div className="chart-container">
                        <TaillePoidsJoueurs />
                    </div>
                    <ComparaisonJoueursGraph />
                  
                    <OverallRatingGraph />
                 
                    <BookmakersGraph />
                    <Footer />
                </>
            )}
            {activeTab === "Modèle ML" && (
                <div className="dashboard-container">
                    <h1>Modèle de Machine Learning</h1>
                    <Footer /> {/* Ajout du footer ici */}
                </div>
            )}
        </div>
        
    );
}

export default App;
