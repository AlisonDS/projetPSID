import React from "react";
import FootballMap from "./components/FootballMap";
import RepartitionDomicileExt from "./components/RepartitionDomicileExt";
import "./App.css";
import PcaTeamAttributes from "./components/PcaTeamAttributes";

function App() {
    return (
        <div className="App">
            <h1>Foot Score - Répartition des Résultats</h1>
            <RepartitionDomicileExt />
            <h1>Foot Score - Carte des Buts</h1>
            <FootballMap />
            <h1>Foot Score - Cercle des Corrélations PCA</h1>
            <PcaTeamAttributes />
        </div>
    );
}

export default App;
