import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

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
    # New complex attributes (optional so existing callers/tests keep working)
    popularity: int = 50          # 0-100 chart popularity
    release_decade: int = 2020    # e.g. 1980, 1990, 2000, 2010, 2020
    mood_tags: List[str] = field(default_factory=list)  # e.g. ["nostalgic", "euphoric"]
    language: str = "english"      # english / spanish / instrumental / ...
    explicit: bool = False         # explicit lyrics flag

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
    # New optional preferences that drive the extended scoring signals
    preferred_mood_tags: List[str] = field(default_factory=list)
    preferred_decade: Optional[int] = None
    preferred_language: Optional[str] = None
    likes_popular: bool = True
    allow_explicit: bool = True

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
    int_fields = {"id", "tempo_bpm", "popularity", "release_decade"}
    float_fields = {"energy", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key in int_fields:
                if key in row and row[key] != "":
                    row[key] = int(row[key])
            for key in float_fields:
                if key in row and row[key] != "":
                    row[key] = float(row[key])
            # mood_tags is a pipe-separated list, e.g. "nostalgic|euphoric"
            if "mood_tags" in row:
                row["mood_tags"] = [
                    tag.strip() for tag in row["mood_tags"].split("|") if tag.strip()
                ]
            # explicit is stored as 0/1 in the CSV
            if "explicit" in row and row["explicit"] != "":
                row["explicit"] = bool(int(row["explicit"]))
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

    # --- New complex-attribute signals ---------------------------------

    # Detailed mood tags: reward overlap between the listener's preferred
    # tags and the song's tags, +0.5 per shared tag (capped at +1.5).
    preferred_tags = set(user_prefs.get("mood_tags", []))
    song_tags = set(song.get("mood_tags", []))
    shared = preferred_tags & song_tags
    if shared:
        weighted = min(1.5, 0.5 * len(shared))
        score += weighted
        reasons.append(f"mood tag overlap ({', '.join(sorted(shared))}) (+{weighted:.2f})")

    # Release decade: exact match +1, adjacent decade +0.5.
    if user_prefs.get("decade") is not None and "release_decade" in song:
        gap = abs(user_prefs["decade"] - song["release_decade"])
        if gap == 0:
            score += 1
            reasons.append(f"decade match ({song['release_decade']}s) (+1.0)")
        elif gap == 10:
            score += 0.5
            reasons.append(f"adjacent decade ({song['release_decade']}s) (+0.5)")

    # Popularity: scaled 0-100 -> 0-1, weighted by how much the user cares.
    if "popularity" in song:
        pop_weight = user_prefs.get("popularity_weight", 0.0)
        if pop_weight:
            weighted = pop_weight * (song["popularity"] / 100.0)
            score += weighted
            reasons.append(f"popularity ({song['popularity']}/100) (+{weighted:.2f})")

    # Language match: +0.75 when the listener has a language preference.
    if user_prefs.get("language") and song.get("language"):
        if user_prefs["language"] == song["language"]:
            score += 0.75
            reasons.append(f"language match ({song['language']}) (+0.75)")

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    artist_penalty: float = 0.5,
    genre_penalty: float = 0.25,
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), highest first.

    A diversity penalty keeps the top results from being dominated by a single
    artist or genre. Results are chosen greedily: each time a song is picked,
    every remaining candidate that shares its artist or genre is pushed down.
    The penalty compounds, so the 2nd song by an artist is penalised once, the
    3rd twice, and so on. Set ``artist_penalty``/``genre_penalty`` to 0 to
    disable diversity re-ranking and rank purely by score.
    """
    # Expected return format: (song_dict, score, explanation)
    # Explicit content is a hard filter, not a scoring signal: if the user
    # does not allow explicit songs, drop them from the catalog entirely.
    if not user_prefs.get("allow_explicit", True):
        songs = [song for song in songs if not song.get("explicit")]

    # Score every song in the catalog using score_song as the "judge".
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no matching preferences"
        scored.append((song, score, explanation))

    # Fast path: no diversity re-ranking requested, rank purely by score.
    if artist_penalty <= 0 and genre_penalty <= 0:
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:k]

    # Greedy diversity-aware selection. At each step, apply the accumulated
    # penalty for how many already-selected songs share the artist/genre, then
    # pick the highest adjusted score. Ties fall back to the original score.
    remaining = list(scored)
    selected: List[Tuple[Dict, float, str]] = []
    artist_counts: Dict[str, int] = {}
    genre_counts: Dict[str, int] = {}

    while remaining and len(selected) < k:
        best_index = None
        best_adjusted = None
        for index, (song, score, explanation) in enumerate(remaining):
            penalty = (
                artist_penalty * artist_counts.get(song.get("artist"), 0)
                + genre_penalty * genre_counts.get(song.get("genre"), 0)
            )
            adjusted = score - penalty
            if best_adjusted is None or (adjusted, score) > best_adjusted:
                best_adjusted = (adjusted, score)
                best_index = index

        song, score, explanation = remaining.pop(best_index)
        penalty = (
            artist_penalty * artist_counts.get(song.get("artist"), 0)
            + genre_penalty * genre_counts.get(song.get("genre"), 0)
        )
        if penalty > 0:
            explanation = f"{explanation}; diversity penalty (-{penalty:.2f})"
        selected.append((song, score, explanation))
        artist_counts[song.get("artist")] = artist_counts.get(song.get("artist"), 0) + 1
        genre_counts[song.get("genre")] = genre_counts.get(song.get("genre"), 0) + 1

    return selected
