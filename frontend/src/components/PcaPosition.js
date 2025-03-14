import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from "react-plotly.js";
import "./PcaStyles.css"; // Import du CSS

const PcaPosition = () => {
    const [plotData, setPlotData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/pca_position")
            .then((response) => {
                console.log("Réponse de l'API :", response.data); // Debug
                if (response.data && response.data.plotData) {
                    setPlotData(response.data.plotData);
                } else {
                    setError("Données de graphique non trouvées.");
                }
            })
            .catch((error) => {
                console.error("❌ Erreur de chargement du graphique :", error);
                setError("Erreur de chargement des données.");
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    return (
        <div>
            <h2>ACP des Équipes colorées par pays</h2>
            {loading && <p>Chargement en cours...</p>}
            {error && <p className="error-message">{error}</p>}
            {plotData && (
                <Plot
                    data={plotData.data}
                    layout={{ ...plotData.layout, width: 600, height: 400 }} // Ajuste la taille
                    config={plotData.config}
                />
            )}
        </div>
    );
};

export default PcaPosition;
