"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

try:
    # Works when run as a module: python -m src.main
    from .recommender import load_songs, recommend_songs
except ImportError:
    # Works when run directly: python src/main.py
    from recommender import load_songs, recommend_songs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Music Recommender Simulation. Omit a flag to leave that "
        "preference out of the profile entirely."
    )
    parser.add_argument("--genre", help="favorite genre, e.g. pop")
    parser.add_argument("--mood", help="favorite mood, e.g. happy")
    parser.add_argument("--energy", type=float, help="target energy, e.g. 0.8")
    parser.add_argument("-k", type=int, default=5, help="number of recommendations (default 5)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Build the profile from whichever flags were supplied. If no flags are
    # given, fall back to the starter example profile.
    user_prefs = {}
    if args.genre is not None:
        user_prefs["genre"] = args.genre
    if args.mood is not None:
        user_prefs["mood"] = args.mood
    if args.energy is not None:
        user_prefs["energy"] = args.energy
    if not user_prefs:
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=args.k)

    summary = "  ".join(f"{key}={value}" for key, value in user_prefs.items())

    print()
    print("=" * 52)
    print("  TOP RECOMMENDATIONS FOR YOU")
    print(f"  {summary}")
    print("=" * 52)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  {rank}. {song['title']} - {song['artist']}")
        print(f"     Score: {score:.2f}")
        print("     Reasons:")
        for reason in explanation.split("; "):
            print(f"       - {reason}")

    print("\n" + "=" * 52)


if __name__ == "__main__":
    main()
