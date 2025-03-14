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

function App() {
    const [activeTab, setActiveTab] = useState("Accueil");

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

            {/* Contenu dynamique selon le menu sélectionné */}
            {activeTab === "Accueil" && (
                  <>
                 
              </>
            )}

            {activeTab === "Modèle ML" && (
                <>
                   
                </>
            )}

            {activeTab === "Dashboard" && (
             <>
             <h1>Foot Score - Répartition des Résultats</h1>
             <RepartitionDomicileExt />
             <h1>Foot Score - Carte des Buts</h1>
             <FootballMap />
             <h1>Foot Score - Cercle des Corrélations PCA</h1>
             <PcaTeamAttributes />
             <h1>Foot Score - ACP des équipes colorées par pays</h1>
             <PcaPosition />
             <h1>Foot Score - Distribution des âges des joueurs par pays</h1>
             <PaysAgeGraph />
             <h1>Foot Score - Taille et Poids des joueurs par Work Rate</h1>
             <TaillePoidsJoueurs />
             <h1>Foot Score - Comparaison des joueurs</h1>
             <ComparaisonJoueursGraph />
             <h1>Foot Score - Moyenne de l'Overall Rating des joueurs par Pays</h1>
             <OverallRatingGraph />
             <h1>Foot Score - Comparaison des Bookmakers</h1>
             <BookmakersGraph />
         </>
     )}
 </div>
    );
}

export default App;
