"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
        "favorite_genres": ["jazz", "r&b", "hip-hop", "reggae"],
        "favorite_moods": ["relaxed", "chill", "laid-back"],
        "target_energy": 0.4,
        "target_danceability": 0.6,
        "target_valence": 0.7
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n{'='*70}")
    print(f"{'🎵 Music Recommender Results'}")
    print(f"{'='*70}\n")

    print(f"Loaded {len(songs)} songs from catalog\n")
    print(f"User Preferences:")
    print(f"  • Favorite genres: {', '.join(user_prefs['favorite_genres'])}")
    print(f"  • Favorite moods: {', '.join(user_prefs['favorite_moods'])}")
    print(f"  • Target energy: {user_prefs['target_energy']}")
    print(f"  • Target danceability: {user_prefs['target_danceability']}")
    print(f"  • Target valence: {user_prefs['target_valence']}\n")

    print(f"{'─'*70}\n")

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"{i}. {song['title']}")
        print(f"   Artist: {song['artist']} | Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   ⭐ Score: {score:.2f}/5.00\n")
        print(f"   Why this recommendation:")
        for reason in explanation.split('\n'):
            print(f"     ✓ {reason}")
        print(f"\n{'─'*70}\n")


if __name__ == "__main__":
    main()
