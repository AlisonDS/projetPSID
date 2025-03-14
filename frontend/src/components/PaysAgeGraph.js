import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";

const PaysAgeGraph = () => {
    const [boxplotData, setBoxplotData] = useState(null);
    const [histogramData, setHistogramData] = useState(null);

    useEffect(() => {
        // Utilisation d'Axios pour récupérer les données depuis Flask
        axios.get("http://127.0.0.1:5000/pays_age")
            .then((response) => {
                console.log(response.data); // Vérifie la structure du JSON
                setBoxplotData(response.data.boxplot);  // Stocke les données du boxplot
                setHistogramData(response.data.histogram);  // Stocke les données de l'histogramme
            })
            .catch((error) => {
                console.error("Erreur de chargement des données:", error);
            });
    }, []);

    return (
        <div>
            <h2>Distribution des âges des joueurs par pays</h2>
        
            {boxplotData ? (
                <Plot
                    data={boxplotData.data}      // Données pour le boxplot
                    layout={boxplotData.layout}  // Layout du boxplot
                    config={{
                        displayModeBar: false,  // Optionnel: Pour enlever la barre d'outils de Plotly
                    }}
                />
            ) : (
                <p>Chargement en cours...</p>
            )}

            <h3>Distribution des âges des joueurs</h3>
            {histogramData ? (
                <Plot
                    data={histogramData.data}      // Données pour l'histogramme
                    layout={histogramData.layout}  // Layout de l'histogramme
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

export default PaysAgeGraph;
