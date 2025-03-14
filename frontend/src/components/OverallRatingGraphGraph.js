import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";

const OverallRatingGraph = () => {
    const [ratingData, setRatingData] = useState(null);

    useEffect(() => {
        // Récupérer les données du graphique
        axios.get("http://127.0.0.1:5000/overall_rating")
            .then((response) => {
                console.log(response.data); // Vérifie la structure du JSON
                setRatingData(response.data);  // Stocke les données du graphique
            })
            .catch((error) => {
                console.error("Erreur de chargement des données:", error);
            });
    }, []);

    return (
        <div>
            <h2>Moyenne de la note globale des joueurs par pays</h2>
            {ratingData ? (
                <Plot
                    data={ratingData.data}      // Données pour le bar chart
                    layout={ratingData.layout}  // Layout du bar chart
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

export default OverallRatingGraph;
