import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";

const ComparaisonJoueursGraph = () => {
    const [radarData, setRadarData] = useState(null);

    useEffect(() => {
        // Récupérer les données du graphique radar
        axios.get("http://127.0.0.1:5000/Comparaison_joueurs")
            .then((response) => {
                console.log(response.data); // Vérifie la structure du JSON
                setRadarData(response.data);  // Stocke les données du radar
            })
            .catch((error) => {
                console.error("Erreur de chargement des données:", error);
            });
    }, []);

    return (
        <div>
            <h2>Comparaison des Profils Joueurs (Attaquant, Défenseur, Moyenne Générale)</h2>
            {radarData ? (
                <Plot
                    data={radarData.data}      // Données pour le radar chart
                    layout={radarData.layout}  // Layout du radar chart
                    config={{
                        displayModeBar: false,  // Optionnel: Pour enlever la barre d'outils de Plotly
                    }}
                />
            ) : (
                <p>Chargement en cours...</p>
            )}
        </div>
    );
};

export default ComparaisonJoueursGraph;
