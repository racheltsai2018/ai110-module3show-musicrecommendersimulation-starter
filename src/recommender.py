import csv
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
    """Read songs from a CSV file into a list of dicts, converting numeric fields to int/float."""
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in int_fields:
                if key in row:
                    row[key] = int(row[key])
            for key in float_fields:
                if key in row:
                    row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences, returning (score, list of reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Genre match: +1 (halved from +2)
    if user_prefs.get("genre") == song.get("genre"):
        score += 1
        reasons.append(f"genre match ({song['genre']}) (+1.0)")

    # Mood match: +1
    if user_prefs.get("mood") == song.get("mood"):
        score += 1
        reasons.append(f"mood match ({song['mood']}) (+1.0)")

    # Energy closeness: the closer the song's energy is to the target,
    # the higher the score, up to a maximum of +1.
    if "energy" in user_prefs and "energy" in song:
        closeness = 1 - abs(user_prefs["energy"] - song["energy"])
        weighted = 2 * closeness  # doubled importance of energy
        score += weighted
        reasons.append(
            f"energy closeness (song {song['energy']:.2f} vs target "
            f"{user_prefs['energy']:.2f}) (+{weighted:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), highest first."""
    # Expected return format: (song_dict, score, explanation)
    # Score every song in the catalog using score_song as the "judge".
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no matching preferences"
        scored.append((song, score, explanation))

    # Rank by score, highest first, and return the top k.
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
