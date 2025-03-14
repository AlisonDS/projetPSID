import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";

const BookmakersGraph = () => {
    const [bookmakersData, setBookmakersData] = useState(null);

    useEffect(() => {
        // Récupérer les données du graphique
        axios.get("http://127.0.0.1:5000/Bookmakers")
            .then((response) => {
                console.log(response.data); // Vérifie la structure du JSON
                setBookmakersData(response.data);  // Stocke les données du graphique
            })
            .catch((error) => {
                console.error("Erreur de chargement des données:", error);
            });
    }, []);

    return (
        <div>
            <h2>Comparaison des Probabilités des Bookmakers vs Fréquences Réelles</h2>
            {bookmakersData ? (
                <Plot
                    data={bookmakersData.data}      // Données pour le bar chart
                    layout={bookmakersData.layout}  // Layout du bar chart
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

export default BookmakersGraph;
