import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";

const RepartitionDomicileExt = () => {
    const [plotData, setPlotData] = useState(null);

    useEffect(() => {
        // Utilisation d'Axios pour récupérer les données depuis Flask
        axios.get("http://127.0.0.1:5000/repartition_domicile_ext")
            .then((response) => {
                console.log(response.data); // Vérifie la structure du JSON
                setPlotData(response.data); // Stocke les données dans le state
            })
            .catch((error) => {
                console.error("Erreur de chargement des données:", error);
            });
    }, []);

    return (
        <div>
            <h2>Répartition des résultats des matchs (domicile, extérieur, égalité)</h2>
            {plotData ? (
                <Plot
                    data={plotData.data}      // Données pour Plotly
                    layout={plotData.layout}  // Layout de Plotly
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

export default RepartitionDomicileExt;
