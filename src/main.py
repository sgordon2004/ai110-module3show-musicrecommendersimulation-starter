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

    # Starter example profile: Smooth Jazz Listener
    smooth_jazz_listener = {
        "favorite_genres": ["jazz", "r&b", "hip-hop", "reggae"],
        "favorite_moods": ["relaxed", "chill", "laid-back"],
        "target_energy": 0.4,
        "target_danceability": 0.6,
        "target_valence": 0.7
    }

    # EDGE CASE 1: Party Paradox - High energy but wants chill/relaxed moods
    # Tests if the scoring logic can handle contradictory user preferences
    # or if it gets "confused" by conflicting signals
    party_paradox = {
        "favorite_genres": ["rock", "metal", "synthwave"],
        "favorite_moods": ["relaxed", "chill"],
        "target_energy": 0.9,  # Very high energy
        "target_danceability": 0.8,
        "target_valence": 0.3  # But low positivity/happiness
    }

    # EDGE CASE 2: Lo-Fi Dancer - Low energy + High danceability
    # Tests if the system can recommend music that's paradoxical
    # (e.g., lofi hip-hop: low energy but designed for movement)
    lofi_dancer = {
        "favorite_genres": ["lofi", "ambient", "indie-pop"],
        "favorite_moods": ["focused", "chill"],
        "target_energy": 0.2,  # Very low energy
        "target_danceability": 0.85,  # But highly danceable (contradiction!)
        "target_valence": 0.5
    }

    # EDGE CASE 3: Melancholy Minimalist - Very low valence preference
    # Tests how the system weights valence (which is currently low importance)
    # and if it can find songs that match sad preferences without other matches
    melancholy_minimalist = {
        "favorite_genres": ["jazz", "ambient", "indie-pop"],
        "favorite_moods": ["moody", "intense"],
        "target_energy": 0.3,
        "target_danceability": 0.1,  # Almost no danceability
        "target_valence": 0.05  # Very sad/melancholic (extreme edge case)
    }

    # Choose which profile to test by uncommenting the desired one:
    # user_prefs = smooth_jazz_listener
    # user_prefs = party_paradox
    user_prefs = lofi_dancer
    # user_prefs = melancholy_minimalist

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
