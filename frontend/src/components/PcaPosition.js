import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js"; // Importer la bibliothèque Plotly

const PcaPosition = () => {
    const [plotData, setPlotData] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/pca_position")
            .then((response) => {
                console.log('Réponse de l\'API :', response.data); // Affiche toute la réponse
                if (response.data && response.data.plotData) {
                    setPlotData(response.data.plotData);  // Si la clé 'plotData' est présente, on l'enregistre
                } else {
                    console.error('Données de graphique non trouvées dans la réponse');
                }
            })
            .catch((error) => {
                console.error("Erreur de chargement des données de graphique:", error);
            });
    }, []);

    return (
        <div>
            <h2>ACP des équipes colorées par pays</h2>
            {plotData ? (
                <Plot
                    data={plotData.data}
                    layout={plotData.layout}
                    config={plotData.config}
                    style={{ width: '80%', height: 'auto' }}
                />
            ) : (
                <p>Chargement en cours...</p>
            )}
        </div>
    );
};

export default PcaPosition;
