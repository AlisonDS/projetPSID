import React, { useState, useEffect } from "react";
import './MatchPredictor.css';

export default function MatchPredictor() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const [countries, setCountries] = useState([]);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [matchResult, setMatchResult] = useState(null); // 'home-win', 'away-win', ou 'draw'
  const [showAnimation, setShowAnimation] = useState(false);
  
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
  
  // Détermine le résultat du match
  const determineMatchResult = (homeScore, awayScore) => {
    if (homeScore > awayScore) return 'home-win';
    if (awayScore > homeScore) return 'away-win';
    return 'draw';
  };
  
  const handlePredict = async () => {
    try {
      setError("");
      setPrediction(null);
      setShowAnimation(false);
      setMatchResult(null);
      
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
      console.log("Données reçues:", data);
      
      const homeScore = customRound(data.home_score_gb);
      const awayScore = customRound(data.away_score_gb);
      
      const result = {
        homeTeamName: data.home_team_name,
        awayTeamName: data.away_team_name,
        homeScore: homeScore,
        awayScore: awayScore
      };
      
      // Détermine le résultat du match
      const resultType = determineMatchResult(homeScore, awayScore);
      
      // Mettre à jour l'état puis déclencher l'animation
      setPrediction(result);
      
      // Attendre que le composant soit rendu avant de déclencher l'animation
      setTimeout(() => {
        setMatchResult(resultType);
        setShowAnimation(true);
      }, 300);
      
    } catch (error) {
      console.error("Erreur :", error);
      setError(error.message || "Une erreur est survenue lors de la prédiction");
    }
  };
  
  return (
    <div className="match-container">
      <h2 className="match-title">Prédiction de match</h2>

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
        <div className="error-message">
          {error}
        </div>
      )}

      {prediction && (
        <div className={`prediction-result ${matchResult}`}>
          <h3>Prédiction</h3>
          
          {/* Terrain de football avec cages et ballon */}
          <div className="field-container">
            {/* Cages de foot */}
            <div className="goalpost goalpost-left"></div>
            <div className="goalpost goalpost-right"></div>
            
            {/* Ballon de football */}
            <div className="football"></div>
          </div>
          
          <div className="score-display">
            <div className="team-block">
              <p className="team-name">{prediction.homeTeamName}</p>
              <p className={`team-score ${matchResult === 'home-win' ? 'team-winner' : ''}`}>
                {prediction.homeScore}
              </p>
            </div>
            
            <div className="vs-block">
              <p>vs</p>
            </div>
            
            <div className="team-block">
              <p className="team-name">{prediction.awayTeamName}</p>
              <p className={`team-score ${matchResult === 'away-win' ? 'team-winner' : ''}`}>
                {prediction.awayScore}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}