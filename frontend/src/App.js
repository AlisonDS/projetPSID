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
            {/* Bandeau supérieur avec le logo */}
            <div className="top-banner">
            <img src="/logo-footscore.jpg" alt="Foot Score Logo" />
            </div>

            {/* Bandeau inférieur avec le menu */}
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

            {/* Contenu dynamique */}
            <div className="content">
                {activeTab === "Accueil" && <h1>🏠 Bienvenue sur l'Accueil</h1>}
                {activeTab === "Modèle ML" && <h1>🤖 Section Modèle ML</h1>}
                {activeTab === "Dashboard" && <h1>📊 Dashboard des statistiques</h1>}
            </div>

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
                        Les données exploitées pour ce projet proviennent de la base de données disponible sur Kaggle, couvrant la saison 2008-2016. Ce jeu de données contient des informations détaillées sur les joueurs et les performances des équipes :
                        </p>
                        <ul>
                            <li>📌 Statistiques individuelles des joueurs (buts, passes, minutes jouées, etc.).</li>
                            <li>📌Données avancées sur les métriques physiques et tactiques, incluant des informations provenant de la série de jeux vidéo FIFA d'EA Sports avec des mises à jour hebdomadaires.</li>
                            <li>📌 Résultats des matchs et performances collectives.</li>
                            <li>📌 Données avancées sur les métriques physiques et tactiques.
                            Ces informations sont essentielles pour identifier les facteurs influençant les scores, affiner les modèles prédictifs et mieux comprendre les dynamiques des équipes et des joueurs.</li>
                        </ul>
                        <p>Ces informations sont essentielles pour identifier les facteurs influençant les scores et affiner les modèles prédictifs.</p>
                    </section>
                    <Footer />
                   
                </div>
            )}
            {/* Contenu dynamique selon le menu sélectionné */}
            {activeTab === "Dashboard" && (
                <>
                    <div className="analysis-container">
                    <RepartitionDomicileExt />

                    <p>
                        Ce graphique illustre la distribution des résultats des matchs selon l’issue du match :
                        victoire de l’équipe jouant à domicile (Home), victoire de l’équipe jouant à l’extérieur (Away) et match nul (Draw).
                        Il met en évidence l’influence du facteur terrain sur la performance des équipes et la fréquence des matchs nuls.
                    </p>

                    <h3>📌 L’avantage du terrain : une tendance marquée</h3>
                    <p>On observe que les victoires à domicile représentent <strong>45,9%</strong> des matchs, ce qui en fait l’issue la plus fréquente. Cette dominance du facteur terrain s’explique par :</p>
                    <ul>
                        <li>🏟️ <strong>Le soutien du public</strong>, qui booste la motivation des joueurs et peut influencer l’arbitrage.</li>
                        <li>⚽ <strong>La familiarité avec le terrain</strong>, qui améliore la performance des équipes locales.</li>
                        <li>🛌 <strong>Moins de fatigue liée aux déplacements</strong>, favorisant une meilleure récupération.</li>
                    </ul>

                    <h3>📉 Un écart notable avec les victoires à l’extérieur</h3>
                    <p>Les victoires à l’extérieur (<strong>28,8%</strong>) sont bien moins fréquentes que celles à domicile, confirmant la difficulté de jouer en déplacement :</p>
                    <ul>
                        <li>🎭 <strong>Un environnement hostile</strong> avec un public adverse.</li>
                        <li>🚍 <strong>Des contraintes logistiques</strong> et de voyage impactant la fatigue.</li>
                        <li>🛑 <strong>Des stratégies plus défensives</strong> pour limiter les risques.</li>
                    </ul>

                    <h3>⚖️ Les matchs nuls : une issue non négligeable</h3>
                    <p>Les matchs nuls (<strong>25,3%</strong>) traduisent une homogénéité entre certaines équipes et des stratégies prudentes :</p>
                    <ul>
                        <li>📊 Rencontres entre équipes de <strong>niveau similaire</strong>.</li>
                        <li>🎯 Matchs à enjeu où les équipes <strong>prennent moins de risques</strong>.</li>
                        <li>🛡️ Styles de jeu défensifs favorisant les égalités.</li>
                    </ul>

                    <h3>📊 Comparaison avec les tendances générales</h3>
                    <p>Dans le football, l’avantage du terrain est une constante, bien que son impact varie selon les championnats :</p>
                    <ul>
                        <li>🏆 <strong>Qualité des équipes</strong> : Dans certains championnats, les équipes dominantes gagnent aussi bien à domicile qu’à l’extérieur.</li>
                        <li>✈️ <strong>Évolution des conditions de jeu</strong> : Les infrastructures modernes réduisent progressivement l’impact du facteur domicile.</li>
                        <li>🎮 <strong>Approches tactiques modernes</strong> : Certaines équipes jouent un pressing haut, minimisant l’influence du terrain.</li>
                    </ul>
                    <h3>📝 Conclusion</h3>
                    <p>Ce graphique met en évidence l’importance du <strong>facteur domicile</strong> dans les performances des équipes et souligne la fréquence des <strong>matchs nuls</strong>. Ces tendances sont cruciales pour l’analyse des résultats et la prédiction des scores.</p>
                </div>

                <div className="analysis-container">
                    <FootballMap />
                        <p>
                        Cette carte illustre la distribution des buts marqués en Europe, avec une échelle de couleurs allant de 0 à 8000 buts.
                        Plus une nation est foncée, plus elle a enregistré un nombre élevé de buts sur la période étudiée.
                    </p>

                    <h3>⚽ Une répartition inégale des buts en Europe</h3>
                    <p>
                        On constate que certains pays dépassent 8000 buts, tandis que d’autres se situent entre 6000 et 8000 buts, 
                        et certains affichent 0 buts (car ces pays ne sont pas présents sur notre dataset). Ces écarts reflètent plusieurs réalités :
                    </p>
                    <ul>
                        <li>📊 <strong>Le volume de matchs disputés</strong> : Plus un championnat est long et avec beaucoup d’équipes, plus il génère de buts.</li>
                        <li>⚡ <strong>Le niveau offensif des compétitions</strong> : Certaines ligues favorisent un jeu rapide et ouvert.</li>
                        <li>🎭 <strong>L’écart de niveau entre les équipes</strong> : Plus une ligue est déséquilibrée, plus les équipes dominantes marquent.</li>
                    </ul>

                    <h3>🌍 Focus sur les pays les plus prolifiques</h3>
                    <p>En observant l’intensité des couleurs sur la carte :</p>
                    <ul>
                        <li>🔥 <strong>Les nations à +8000 buts</strong> : Angleterre, Espagne... qui affichent les championnats les plus compétitifs.</li>
                        <li>⚽ <strong>Les pays entre 6000 et 8000 buts</strong> : Ligues dynamiques où les attaquants brillent.</li>
                        <li>🛡️ <strong>Les pays entre 2000 et 6000 buts</strong> : Ligues plus tactiques et défensives.</li>
                    </ul>

                    <h3>📊 Facteurs expliquant ces écarts</h3>
                    <ul>
                        <li>🎯 <strong>La présence de grands buteurs</strong> : Certains championnats attirent les meilleurs attaquants mondiaux.</li>
                        <li>⚔️ <strong>Les stratégies de jeu</strong> : Plus offensif = plus de buts.</li>
                        <li>📋 <strong>Arbitrage et penalties</strong> : Plus de penalties = plus de buts.</li>
                    </ul>

                    <h3>🔍 Conclusion</h3>
                    <p>
                        Cette carte permet de visualiser les pays où le nombre de buts est le plus élevé et d’identifier les tendances du football européen.
                        Ces données sont essentielles pour analyser les performances des ligues et affiner les prédictions des scores en fonction des caractéristiques propres à chaque pays.
                    </p>
                    </div>

                <div className="analysis-container">
                    
                        <PcaTeamAttributes />
                        <p>
                            Ce cercle des corrélations illustre la répartition des variables dans un plan défini par les deux premières composantes principales (PC1 et PC2).
                        </p>

                        <h3>🛡️ Variables liées à la défense (en haut à droite)</h3>
                        <ul>
                            <li>⚔️ <strong>defencePressure</strong></li>
                            <li>🏟️ <strong>defenceTeamWidth</strong></li>
                            <li>🛑 <strong>defenceAggression</strong></li>
                        </ul>
                        <p>Ces variables sont fortement corrélées entre elles et influencent principalement la première composante principale (PC1).</p>

                        <h3>⚡ Variables liées à la construction du jeu et à la création d’occasions (en bas à droite)</h3>
                        <ul>
                            <li>⚡ <strong>buildUpPlayPassing</strong></li>
                            <li>🚀 <strong>buildUpPlaySpeed</strong></li>
                            <li>🎯 <strong>chanceCreationPassing</strong></li>
                            <li>🎭 <strong>chanceCreationCrossing</strong></li>
                        </ul>
                        <p>
                            Ces variables sont également fortement corrélées entre elles et influencent significativement PC1. 
                            Elles reflètent le style de jeu basé sur la circulation du ballon et la vitesse de construction des actions.
                        </p>

                        <h3>🔄 Opposition entre styles de jeu</h3>
                        <p>
                            Les équipes qui privilégient la construction rapide et la création d’occasions par le jeu de passes 
                            (<strong>buildUpPlay</strong> et <strong>chanceCreation</strong>) sont opposées aux équipes qui misent sur une 
                            <strong>défense agressive et une forte pression défensive</strong>.
                        </p>
                        <p>
                            Cette opposition montre que **PC1** distingue les équipes par leur approche du jeu :
                            <strong>offensive et basée sur la possession d’un côté</strong>, 
                            <strong>défensive et axée sur la pression de l’autre</strong>.
                        </p>
                    </div>
                
                <div className="analysis-container">
                        <PcaPosition />
                    
                </div>
                <div className="analysis-container">
                    <PaysAgeGraph />
                    <p>
                        Cette boîte à moustaches illustre la répartition des âges des joueurs dans différents pays européens.
                        Chaque boîte représente la médiane, les quartiles et la dispersion des âges, offrant une comparaison visuelle des tendances entre les nations.
                    </p>

                    <h3>📊 Une répartition homogène avec quelques variations</h3>
                    <p>
                        La majorité des joueurs évoluent dans une fourchette d’âge comprise entre 20 et 35 ans, avec des médianes proches de 25-27 ans selon les pays.
                        Toutefois, certaines différences se dégagent :
                    </p>
                    <ul>
                        <li>🏴 <strong>Angleterre (27 ans)</strong>,  <strong>Italie (27 ans)</strong> et  <strong>France (26 ans)</strong> 
                            affichent des médianes plus élevées, traduisant une présence plus marquée de joueurs expérimentés.</li>
                        <li> <strong>Pays-Bas (24 ans)</strong> et  <strong>Allemagne (25 ans)</strong> montrent une répartition plus large, 
                            avec des jeunes joueurs et des vétérans.</li>
                        <li>🏴 <strong>Écosse</strong> et  <strong>Espagne</strong> ont une dispersion similaire, avec une répartition bien centrée autour de 25-26 ans.</li>
                    </ul>

                    <h3>📌 Présence de joueurs très jeunes et plus âgés</h3>
                    <p>Les points situés au-dessus et en dessous des moustaches indiquent des valeurs atypiques :</p>
                    <ul>
                        <li>🧑‍🎓 <strong>Les Pays-Bas et l’Écosse</strong> comptent plusieurs jeunes joueurs dès 16-17 ans.</li>
                        <li>👴 <strong>L’Angleterre, l’Italie et l’Allemagne</strong> possèdent plus de joueurs dépassant 35 ans, certains atteignant 42-43 ans.</li>
                    </ul>

                    <h3>🔍 Explications possibles des différences</h3>
                    <ul>
                        <li>🏆 <strong>Politiques de formation</strong> : Les Pays-Bas misent sur la jeunesse, tandis que l’Italie et l’Angleterre intègrent plus de vétérans.</li>
                        <li>⚽ <strong>Styles de jeu et exigences physiques</strong> : Les ligues physiques favorisent des joueurs expérimentés, tandis que d’autres privilégient la vitesse des jeunes.</li>
                        <li>💰 <strong>Opportunités de transfert</strong> : Certains pays attirent des joueurs en fin de carrière avec des contrats avantageux.</li>
                    </ul>

                    <h3>🔎 Conclusion</h3>
                    <p>
                        Cette distribution met en lumière la diversité des profils d’âge selon les pays.
                        Elle reflète les stratégies de recrutement et d’évolution des joueurs, offrant une meilleure compréhension du marché des joueurs et des dynamiques des championnats.
                    </p>
                    <p>
                        Le deuxième graphique présente l’histogramme de répartition des âges des joueurs, accompagné d’une boîte à moustaches 
                        pour une meilleure visualisation des tendances et des valeurs extrêmes.
                    </p>

                    <h3>📊 Analyse des valeurs clés</h3>
                    <ul>
                        <li>🔹 <strong>Âge minimum :</strong> 16.36 ans</li>
                        <li>📍 <strong>1er quartile (Q1) :</strong> 23.68 ans</li>
                        <li>⚖️ <strong>Médiane :</strong> 26.48 ans</li>
                        <li>📍 <strong>3e quartile (Q3) :</strong> 29.50 ans</li>
                        <li>📈 <strong>Limite supérieure :</strong> 38.23 ans</li>
                        <li>🔹 <strong>Âge maximum :</strong> 43.30 ans</li>
                    </ul>

                    <h3>📌 Répartition des joueurs</h3>
                    <ul>
                        <li>⚽ <strong>La majorité des joueurs ont entre 20 et 35 ans</strong>, avec un pic autour de 25-27 ans.</li>
                        <li>🚀 <strong>Très peu de joueurs ont moins de 18 ans ou plus de 38 ans</strong>.</li>
                        <li>📊 <strong>La boîte à moustaches montre une forte concentration entre 23 et 30 ans</strong>, 
                            indiquant que la plupart des joueurs professionnels évoluent dans cette tranche d’âge.</li>
                        <li>🎭 <strong>Certains joueurs atypiques dépassent 40 ans</strong>, ce qui reste rare dans le football de haut niveau.</li>
                    </ul>
                </div>

                <div className="analysis-container">
                        <TaillePoidsJoueurs />
                            <p>
                                Ces graphiques comparent la <strong>taille moyenne (cm)</strong> et le <strong>poids moyen (kg)</strong> des joueurs 
                                en fonction de leur <strong>Work Rate</strong> offensif (<em>Attacking</em>) et défensif (<em>Defensive</em>), 
                                répartis en trois catégories : <strong>Low (faible)</strong>, <strong>Medium (moyen)</strong> et <strong>High (élevé)</strong>.
                            </p>

                            <h3>📏 Taille moyenne des joueurs</h3>
                            <ul>
                                <li>📊 <strong>La taille des joueurs varie peu</strong> en fonction du Work Rate, restant globalement autour de 180 cm.</li>
                                <li>🛡️ <strong>Les joueurs avec un Work Rate défensif élevé</strong> sont légèrement plus grands que ceux avec un Work Rate offensif élevé.</li>
                                <li>📉 Aucune tendance forte ne se dégage entre Work Rate et taille, suggérant que ce critère n’a pas d’impact majeur sur la morphologie des joueurs.</li>
                            </ul>

                            <h3>⚖️ Poids moyen des joueurs</h3>
                            <ul>
                                <li>🏋️ <strong>Les joueurs défensifs</strong> ont généralement un poids moyen légèrement plus élevé que les joueurs offensifs.</li>
                                <li>📉 <strong>Le poids moyen tourne autour de 75-78 kg</strong>, avec une variation mineure entre les différentes catégories.</li>
                                <li>🛡️ <strong>Les joueurs ayant un Work Rate défensif élevé</strong> semblent être un peu plus lourds que ceux avec un Work Rate offensif élevé, 
                                    ce qui pourrait s’expliquer par une nécessité de robustesse physique pour la récupération du ballon.</li>
                            </ul>

                            <h3>📊 Conclusion générale </h3>
                            <p>En combinant ces analyses avec la distribution des âges des joueurs, plusieurs tendances se dégagent :</p>
                            <ul>
                                <li>📅 <strong>La majorité des joueurs ont entre 23 et 30 ans</strong>, période où leurs performances physiques et tactiques sont à leur apogée.</li>
                                <li>📏 <strong>La taille et le poids moyens des joueurs restent relativement constants</strong> selon le Work Rate, 
                                    bien que les profils défensifs soient souvent plus grands et plus lourds.</li>
                                <li>⚽ <strong>L’impact du Work Rate sur la morphologie des joueurs semble limité</strong>, 
                                    bien que les joueurs défensifs tendent à être légèrement plus physiques.</li>
                            </ul> 
                        
                </div>    
                <div className="analysis-container">
                <ComparaisonJoueursGraph />
                <p>
                    Ce radar compare les attributs des joueurs selon leur rôle : 
                    <span style={{ color: "blue" }}><strong> attaquants (bleu)</strong></span>, 
                    <span style={{ color: "red" }}><strong> défenseurs (rouge)</strong></span> et 
                    <span style={{ color: "green" }}><strong> moyenne générale (vert)</strong></span>. 
                    Chaque axe représente une compétence clé, mettant en évidence les différences entre les profils.
                </p>

                <h3>📊 Tendances générales</h3>
                <ul>
                    <li>⚡ <strong>Les attaquants</strong> se distinguent par une meilleure <strong>accélération</strong>, <strong>finition</strong> et <strong>positionnement</strong>, 
                        essentiels pour marquer des buts et se démarquer en attaque.</li>
                    <li>🛡️ <strong>Les défenseurs</strong> sont largement supérieurs en <strong>tacle</strong>, <strong>marquage</strong> et <strong>force</strong>, 
                        des compétences fondamentales pour bloquer les adversaires et récupérer le ballon.</li>
                    <li>⚖️ <strong>La moyenne générale</strong> (en vert) se situe entre ces deux extrêmes, illustrant un équilibre entre les différentes compétences.</li>
                </ul>

                <h3>📌 Différences marquées entre profils</h3>
                <ul>
                    <li>🏃‍♂️ <strong>Accélération et positionnement :</strong> Les attaquants surpassent les autres joueurs, 
                        ce qui leur permet de se placer efficacement et de prendre de vitesse les défenseurs.</li>
                    <li>🎯 <strong>Finition (finishing) :</strong> Attribut clé des attaquants, cet aspect est nettement inférieur chez les défenseurs.</li>
                    <li>🛑 <strong>Tacle et marquage :</strong> Les défenseurs dominent largement ces domaines, leur permettant de stopper les attaques adverses.</li>
                    <li>🏋️ <strong>Force physique (strength) :</strong> Les défenseurs affichent une force bien plus élevée que les attaquants, 
                        un atout crucial pour les duels aériens et les confrontations physiques.</li>
                </ul>

                <h3>📊 Conclusion</h3>
                <p>
                    Cette analyse montre que chaque rôle est spécialisé : 
                    <strong>les attaquants misent sur la vitesse et la précision devant le but</strong>, 
                    tandis que <strong>les défenseurs privilégient la puissance, la rigueur défensive et la récupération du ballon</strong>.
                </p>
            </div>


                <div className="analysis-container">
                    <OverallRatingGraph />  
                    <p>
                        Ce graphique montre la <strong>note globale moyenne des joueurs par pays</strong>, 
                        mettant en évidence les écarts de niveau moyen entre les nations.
                    </p>

                    <h3>📊 Tendances générales</h3>
                    <ul>
                        <li>🏆 <strong>Angleterre (75.07)</strong>, <strong>Italie (74.66)</strong> et  <strong>Espagne (74.62)</strong> 
                            affichent les meilleures notes moyennes, ce qui témoigne d’un effectif globalement plus compétitif.</li>
                        <li> <strong>Allemagne (73.96)</strong> et  <strong>France (71.89)</strong> suivent de près avec des notes élevées, 
                            confirmant la qualité de leur formation.</li>
                        <li> <strong>Portugal (71.25)</strong> et <strong>Pays-Bas (69.39)</strong> présentent une moyenne légèrement inférieure, 
                            bien qu’ils soient reconnus pour leurs talents émergents.</li>
                        <li><strong>Belgique (67.79)</strong> et 🏴 <strong>Écosse (64.86)</strong> ferment la marche avec les notes les plus basses, 
                            traduisant un effectif globalement moins bien noté.</li>
                    </ul>
                    <h3>📌 Analyse rapide</h3>
                    <ul>
                        <li>🏅 <strong>Les pays du top 3 (Angleterre, Italie, Espagne)</strong> dominent en termes de qualité moyenne des joueurs.</li>
                        <li>📉 <strong>L’Écosse se démarque avec la note la plus basse (64.86)</strong>, montrant un écart net avec les autres nations.</li>
                        <li>⚽ <strong>Le classement reflète partiellement le niveau des championnats nationaux</strong>, 
                            où les ligues les plus compétitives attirent de meilleurs joueurs.</li>
                    </ul>
                    <h3>🔎 Conclusion</h3>
                    <p>
                        Les pays ayant les meilleures notes moyennes sont ceux dont les championnats attirent les joueurs les plus talentueux.
                        <strong> L’Angleterre, l’Italie et l’Espagne</strong> bénéficient d’effectifs globalement mieux notés, 
                        tandis que <strong>l’Écosse et la Belgique</strong> affichent des moyennes plus basses, traduisant un niveau global inférieur en termes de notation.
                    </p>
                </div>

                <div className="analysis-container">
                    <BookmakersGraph />
                    <p>
                        Ce graphique met en parallèle les <strong>probabilités de résultats de match</strong> estimées par les bookmakers et les <strong>fréquences réelles</strong> observées.
                        Il permet d’évaluer la précision des prévisions et d’identifier d’éventuelles tendances dans l’ajustement des cotes.
                    </p>

                    <h3>📊 Une correspondance globale avec de légères différences</h3>
                    <p>
                        On constate que les probabilités prédites et les fréquences réelles sont relativement proches pour les trois types de résultats, 
                        ce qui indique que <strong>les bookmakers ajustent correctement leurs modèles</strong> en fonction des tendances du football. 
                        Cependant, de légers écarts sont visibles :
                    </p>

                    <ul>
                        <li>🏠 <strong>Les victoires à domicile sont légèrement sous-estimées</strong>
                            <ul>
                                <li>🔹 <strong>Probabilité estimée :</strong> 44,8 %</li>
                                <li>📊 <strong>Fréquence réelle :</strong> 45,9 %</li>
                                <li>📉 Cette différence, bien que minime, suggère que <strong>les équipes jouant à domicile gagnent un peu plus souvent</strong> que ce qui est anticipé.</li>
                            </ul>
                        </li>
                        <li>⚖️ <strong>Les matchs nuls sont bien anticipés</strong>
                            <ul>
                                <li>🔹 <strong>Probabilité estimée :</strong> 25,9 %</li>
                                <li>📊 <strong>Fréquence réelle :</strong> 25,3 %</li>
                                <li>✅ <strong>L’écart est quasi inexistant</strong>, ce qui montre que le modèle de prédiction capture bien cette tendance.</li>
                            </ul>
                        </li>
                        <li>🛫 <strong>Les victoires à l’extérieur sont légèrement surestimées</strong>
                            <ul>
                                <li>🔹 <strong>Probabilité estimée :</strong> 29,4 %</li>
                                <li>📊 <strong>Fréquence réelle :</strong> 28,8 %</li>
                                <li>📉 Ce biais peut être lié à une tendance à considérer que <strong>l’écart entre les équipes est plus faible qu’en réalité</strong>.</li>
                            </ul>
                        </li>
                    </ul>

                    <h3>📌 Explications possibles des différences</h3>
                    <ul>
                        <li>📢 <strong>Influence du public et des conditions de jeu :</strong> Les équipes à domicile bénéficient d’un avantage souvent sous-évalué.</li>
                        <li>💪 <strong>Facteurs psychologiques et fatigue :</strong> Jouer à l’extérieur est plus éprouvant, ce qui peut expliquer une surestimation des victoires des visiteurs.</li>
                        <li>💰 <strong>Ajustements des cotes :</strong> Les bookmakers intègrent d’autres paramètres comme les mises des parieurs, ce qui peut légèrement biaiser les prévisions.</li>
                    </ul>

                    <h3>🔎 Conclusion</h3>
                    <p>
                        Cette analyse montre que <strong>les bookmakers sont globalement précis</strong>, 
                        avec des écarts inférieurs à 1 % pour chaque type de résultat.
                        Toutefois, une légère <strong>sous-estimation des victoires à domicile</strong> et une <strong>surestimation des succès à l’extérieur</strong> peuvent être observées.
                        Cela illustre la complexité de la modélisation des résultats de match et l’importance de prendre en compte les dynamiques réelles du terrain.
                    </p>
                </div>

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
