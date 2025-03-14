import React, { useEffect, useState } from "react";
import axios from "axios";
import Plot from 'react-plotly.js';

const TaillePoidsJoueurs = () => {
    const [sizeData, setSizeData] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/taille_poids_joueurs")
            .then((response) => {
                console.log('Réponse de l\'API :', response.data);  // Affiche toute la réponse
                if (response.data && response.data.sizeData) {
                    setSizeData(response.data.sizeData);  // Données de taille et poids
                } else {
                    console.error('Données non trouvées dans la réponse');
                }
            })
            .catch((error) => {
                console.error("Erreur de chargement des données:", error);
            });
    }, []);

    // Préparer les données pour le graphique
    const attackingData = sizeData?.filter(item => item.work_rate_type === 'Attacking');
    const defensiveData = sizeData?.filter(item => item.work_rate_type === 'Defensive');

    return (
        <div>
            <h2>Taille et Poids des joueurs par Work Rate</h2>
            {sizeData && (
                <div>
                    <h3>Taille et Poids selon le Work Rate</h3>
                    <Plot
                        data={[
                            {
                                x: attackingData.map(item => item.work_rate),
                                y: attackingData.map(item => item.height),
                                type: 'bar',
                                name: 'Attacking Work Rate',
                                marker: { color: 'blue' },
                            },
                            {
                                x: defensiveData.map(item => item.work_rate),
                                y: defensiveData.map(item => item.height),
                                type: 'bar',
                                name: 'Defensive Work Rate',
                                marker: { color: 'red' },
                            }
                        ]}
                        layout={{
                            title: 'Taille moyenne des joueurs',
                            xaxis: { title: 'Work Rate' },
                            yaxis: { title: 'Taille moyenne (cm)' },
                            barmode: 'group',
                        }}
                    />
                    <Plot
                        data={[
                            {
                                x: attackingData.map(item => item.work_rate),
                                y: attackingData.map(item => item.weight),
                                type: 'bar',
                                name: 'Attacking Work Rate',
                                marker: { color: 'blue' },
                            },
                            {
                                x: defensiveData.map(item => item.work_rate),
                                y: defensiveData.map(item => item.weight),
                                type: 'bar',
                                name: 'Defensive Work Rate',
                                marker: { color: 'red' },
                            }
                        ]}
                        layout={{
                            title: 'Poids moyen des joueurs',
                            xaxis: { title: 'Work Rate' },
                            yaxis: { title: 'Poids moyen (kg)' },
                            barmode: 'group',
                        }}
                    />
                </div>
            )}
        </div>
    );
};

export default TaillePoidsJoueurs;
