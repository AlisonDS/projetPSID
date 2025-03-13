import React, { useEffect, useState } from "react";
import axios from "axios";

const PcaTeamAttributes = () => {
    const [image, setImage] = useState(null);

    useEffect(() => {
        // Utilisation d'Axios pour récupérer l'image depuis Flask
        axios.get("http://127.0.0.1:5000/pca_team_attributes")
            .then((response) => {
                console.log(response.data); // Vérifie la structure du JSON
                setImage(response.data.image); // Stocke l'image base64 dans le state
            })
            .catch((error) => {
                console.error("Erreur de chargement de l'image:", error);
            });
    }, []);

    return (
        <div>
            <h2>Cercle des corrélations PCA</h2>
            {image ? (
                <img 
                    src={`data:image/png;base64,${image}`} 
                    alt="Cercle des corrélations PCA" 
                    style={{ width: '80%', height: 'auto' }} // Ajuste la taille de l'image
                />
            ) : (
                <p>Chargement en cours...</p>
            )}
        </div>
    );
};

export default PcaTeamAttributes;
