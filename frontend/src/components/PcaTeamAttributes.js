import React, { useEffect, useState } from "react";
import axios from "axios";

const PcaTeamAttributes = () => {
    const [image, setImage] = useState(null);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/pca_team_attributes")
            .then((response) => {
                console.log('Réponse de l\'API :', response.data); // Affiche toute la réponse
                if (response.data && response.data.image) {
                    setImage(response.data.image);  // Si la clé 'image' est présente, on l'enregistre
                } else {
                    console.error('Image non trouvée dans la réponse');
                }
            })
            .catch((error) => {
                console.error("Erreur de chargement de l'image:", error);
            });
    }, []);

    return (
        <div className="pca-container">
            <h2>Cercle des corrélations PCA</h2>
            {image ? (
                <img 
                    src={image}  // Affiche directement l'image encodée en base64
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