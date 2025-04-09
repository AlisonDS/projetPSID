import React, { useState, useEffect } from "react";
import './MatchPredictor.css'

export default function MatchPredictor() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState("");
  
  useEffect(() => {
    // Charger la liste des pays
    fetch("/api/countries")
      .then((res) => res.json())
      .then((data) => {
        setCountries(data);
      })
      .catch((err) => {
        console.error("Erreur chargement pays:", err);
        setError("Impossible de charger les pays");
      });
  }, []);
  
  useEffect(() => {
    if (!selectedCountry) return;
    
    fetch(`/api/teams?country_id=${selectedCountry}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Équipes filtrées :", data);
        setTeams(data);
      })
      .catch((err) => {
        console.error("Erreur chargement équipes:", err);
        setError("Impossible de charger les équipes");
      });
  }, [selectedCountry]);
  
  // Fonction pour arrondir selon la règle spécifiée
  const customRound = (value) => {
    const decimal = value - Math.floor(value);
    if (decimal === 0.5) return Math.round(value); // Cas particulier pour 0.5 (arrondi standard)
    return decimal > 0.5 ? Math.ceil(value) : Math.floor(value);
  };
  
  const handlePredict = async () => {
    try {
      setError("");
      setPrediction(null);
      
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          home_team: homeTeam,
          away_team: awayTeam,
        }),
      });
  
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.message || "Erreur lors de la prédiction");
      }
  
      const data = await res.json();
      // Utiliser les données correctement selon la structure renvoyée par le backend
      console.log("Données reçues:", data);
      
      // Appliquer l'arrondissement personnalisé aux scores
      // const homeScore = customRound(data.home_score);
      // const awayScore = customRound(data.away_score);
      
      // setPrediction({
      //   homeTeamName: data.home_team_name,
      //   awayTeamName: data.away_team_name,
      //   homeScore: homeScore,
      //   awayScore: awayScore,
      //   rawHomeScore: data.home_score,  // Conserver les scores bruts pour affichage optionnel
      //   rawAwayScore: data.away_score
      // });
      setPrediction({
        homeTeamName:data.home_team_name,
        awayTeamName:data.away_team_name,
        homeScore: customRound(data.home_score_stack), 
        awayScore: customRound(data.away_score_stack)
        // rawHomeScore: customRound(data.home_score_stack),
        // rawAwayScore: customRound(data.away_score_stack)
      });
      
    } catch (error) {
      console.error("Erreur :", error);
      setError(error.message || "Une erreur est survenue lors de la prédiction");
    }
  };
  
  return (
    <div className="match-container">
      <h2 className="match-title">Prédiction de match</h2>


      {/* <div className="mb-4">
        <label className="block mb-2 font-medium">Pays</label>
        <select
          value={selectedCountry}
          onChange={(e) => {
            setSelectedCountry(e.target.value);
            setHomeTeam("");
            setAwayTeam("");
            setTeams([]);
          }}
          className="w-full p-2 border rounded"
        >
          <option value="">-- Choisir un pays --</option>
          {countries.map((country) => (
            <option key={country.country_id} value={country.country_id}>
              {country.name}
            </option>
          ))}
        </select>
      </div>

      <div className="mb-4">
        <label className="block mb-2 font-medium">Équipe à domicile</label>
        <select
            value={homeTeam}
            onChange={(e) => setHomeTeam(e.target.value)}
            className="w-full p-2 border rounded"
            >
            <option value="">-- Choisir --</option>
            {teams.map((team) => (
                <option key={team.team_api_id} value={team.team_api_id}>
                {team.team_long_name}
                </option>
            ))}
        </select>
      </div>

      <div className="mb-4">
        <label className="block mb-2 font-medium">Équipe à l'extérieur</label>
        <select
            value={awayTeam}
            onChange={(e) => setAwayTeam(e.target.value)}
            className="w-full p-2 border rounded"
            >
            <option value="">-- Choisir --</option>
            {teams.map((team) => (
                <option key={team.team_api_id} value={team.team_api_id}>
                {team.team_long_name}
                </option>
            ))}
        </select>
      </div>
    
      <button
        onClick={handlePredict}
        disabled={!homeTeam || !awayTeam}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        Prédire le résultat
      </button> */}
      <div className="select-block">
        <label className="select-label">Pays</label>
        <select
          value={selectedCountry}
          onChange={(e) => {
            setSelectedCountry(e.target.value);
            setHomeTeam("");
            setAwayTeam("");
            setTeams([]);
          }}
          className="select-input"
        >
          <option value="">-- Choisir un pays --</option>
          {countries.map((country) => (
            <option key={country.country_id} value={country.country_id}>
              {country.name}
            </option>
          ))}
        </select>
      </div>

      <div className="select-block">
        <label className="select-label">Équipe à domicile</label>
        <select
          value={homeTeam}
          onChange={(e) => setHomeTeam(e.target.value)}
          className="select-input"
        >
          <option value="">-- Choisir --</option>
          {teams.map((team) => (
            <option key={team.team_api_id} value={team.team_api_id}>
              {team.team_long_name}
            </option>
          ))}
        </select>
      </div>

      <div className="select-block">
        <label className="select-label">Équipe à l'extérieur</label>
        <select
          value={awayTeam}
          onChange={(e) => setAwayTeam(e.target.value)}
          className="select-input"
        >
          <option value="">-- Choisir --</option>
          {teams.map((team) => (
            <option key={team.team_api_id} value={team.team_api_id}>
              {team.team_long_name}
            </option>
          ))}
        </select>
      </div>

      <button
        onClick={handlePredict}
        disabled={!homeTeam || !awayTeam}
        className="predict-button"
      >
        Prédire le résultat
      </button>


      {error && (
        <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {prediction && (
        <div className="prediction-result">
          <h3 className="text-xl font-bold text-center mb-3">Prédiction</h3>
          <div className="flex justify-between items-center">
            <div className="text-center w-2/5">
              <p className="font-medium">{prediction.homeTeamName}</p>
              <p className="text-3xl font-bold">{prediction.homeScore}</p>
              {/* <p className="text-xs text-gray-500">
                (Score brut: {prediction.rawHomeScore?.toFixed(2)})
              </p> */}
            </div>
            <div className="text-center">
              <p className="text-lg font-medium">vs</p>
            </div>
            <div className="text-center w-2/5">
              <p className="font-medium">{prediction.awayTeamName}</p>
              <p className="text-3xl font-bold">{prediction.awayScore}</p>
              {/* <p className="text-xs text-gray-500">
                (Score brut: {prediction.rawAwayScore?.toFixed(2)})
              </p> */}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}