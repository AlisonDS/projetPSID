import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    // Appel de l'API Flask pour récupérer l'image du graphique
    axios.get('http://localhost:5000/carte_but_league', { responseType: 'arraybuffer' })
      .then(response => {
        // Convertir l'image binaire en base64
        const base64Image = Buffer.from(response.data, 'binary').toString('base64');
        setImageSrc(`data:image/png;base64,${base64Image}`);
      })
      .catch(error => {
        console.error('Error fetching the chart:', error);
      });
  }, []);

  return (
    <div>
      <h1>Graphique des buts par pays</h1>
      {imageSrc ? (
        <img src={imageSrc} alt="Buts par pays" />
      ) : (
        <p>Chargement du graphique...</p>
      )}
    </div>
  );
}

export default App;
