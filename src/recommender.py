from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    print(f"Loading songs from {csv_path}...")
    songs = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numerical values to appropriate types
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a song based on how well it matches the user's preferences.

    Scoring follows the modified algorithm recipe:
    - Categorical: mood match (+1.5), genre match (+0.5) [halved]
    - Numerical: energy (+2.0) [doubled], danceability (+0.5) [halved], valence (+0.5)
    - Total: 0 to 5.0 points

    Returns:
        Tuple of (total_score, list_of_reasons)
        where reasons explain each component of the score
    """
    import math

    score = 0.0
    reasons = []

    # Categorical scores (exact match)
    if song['genre'] in user_prefs['favorite_genres']:
        score += 0.5
        reasons.append(f"Genre match: {song['genre']} (+0.5)")

    if song['mood'] in user_prefs['favorite_moods']:
        score += 1.5
        reasons.append(f"Mood match: {song['mood']} (+1.5)")

    # Gaussian similarity for numerical features
    # Sigma controls the width of the Gaussian; 0.3 means score drops to ~0.6 at distance 0.3
    sigma = 0.3

    # Energy similarity (0 to 2.0 points - doubled importance)
    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_score = 2.0 * math.exp(-(energy_diff ** 2) / (2 * sigma ** 2))
    score += energy_score
    reasons.append(f"Energy similarity: {energy_score:.2f} (+{energy_score:.2f})")

    # Danceability similarity (0 to 0.5 points - halved to balance)
    danceability_diff = abs(song['danceability'] - user_prefs['target_danceability'])
    danceability_score = 0.5 * math.exp(-(danceability_diff ** 2) / (2 * sigma ** 2))
    score += danceability_score
    reasons.append(f"Danceability similarity: {danceability_score:.2f} (+{danceability_score:.2f})")

    # Valence similarity (0 to 0.5 points, weighted less heavily)
    valence_diff = abs(song['valence'] - user_prefs['target_valence'])
    valence_score = 0.5 * math.exp(-(valence_diff ** 2) / (2 * sigma ** 2))
    score += valence_score
    reasons.append(f"Valence similarity: {valence_score:.2f} (+{valence_score:.2f})")

    return score, reasons
    

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    scored_songs = [
        (song, score, "\n".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored_songs, key=lambda x: x[1], reverse=True)[:k]
