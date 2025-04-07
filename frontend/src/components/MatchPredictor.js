import React, { useState, useEffect } from "react";

export default function MatchPredictor() {
  const [teams, setTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState(null);

  useEffect(() => {
    fetch("/api/teams")
      .then((res) => res.json())
      .then((data) => {
        console.log("Données équipes reçues :", data);
        setTeams(data);
      });
  }, []);
  

  const handlePredict = async () => {
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          home_team: homeTeam, // contient le team_api_id de l'équipe à domicile
          away_team: awayTeam, // contient le team_api_id de l'équipe à l'extérieur
        }),
      });
  
      if (!res.ok) {
        throw new Error("Erreur lors de la prédiction");
      }
  
      const data = await res.json();
      setPrediction(data.prediction); // data.prediction devrait contenir un string ou un label comme "2-1", "Victoire domicile", etc.
    } catch (error) {
      console.error("Erreur :", error);
      setPrediction("Une erreur est survenue.");
    }
  };
  

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 border rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6 text-center">Prédiction de match</h2>

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
      </button>

      {prediction && (
        <div className="mt-6 text-center text-lg font-semibold">
          Résultat prédit : {prediction}
        </div>
      )}
    </div>
  );
}
