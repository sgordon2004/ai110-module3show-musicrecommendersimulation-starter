# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **Find-A-Vibe 1.0**  

---

## 2. Intended Use  

This recommender suggests 5 songs from a 20-song catalog based on user preferences for mood, genre, and energy level. It is designed for classroom exploration to understand how scoring systems can create filter bubbles and bias—not for real users—and assumes users have measurable, stable preferences that can be captured with numerical and categorical features.

---

## 3. How the Model Works  

For each song, we look at its mood, genre, how energetic it is, and how danceable it feels. We then compare these to what the user tells us they like: their favorite mood, favorite genre, and desired energy level. We give each song a score out of 5 points based on how well it matches—a perfect mood match is worth 1.5 points, genre gets 0.5 points, and how close the song's energy is to their target gets 2 points (we doubled this from the original 1.0 to emphasize that how a song *feels* matters more than its category). We then show the user the 5 songs with the highest scores.

---

## 4. Data  

The catalog contains 20 songs across 16 genres (pop, rock, lofi, jazz, classical, etc.) and 15 different moods (happy, chill, intense, relaxed, etc.). We did added 10 more songs to the original dataset of 10. However, the dataset is limited—it's missing whole musical styles like blues, country-pop hybrids, and doesn't reflect real-world listening patterns where users stream millions of songs with far greater diversity.

---

## 5. Strengths  

The system works very well for users with strong, consistent preferences—for example, someone who wants "chill lofi music with low energy" gets exactly that. It correctly captures that energy is crucial: users who specify a target energy level get songs that genuinely *feel* that way rather than just matching a genre label. The recommendations aligned with intuition when testing profiles with single, clear moods and energy preferences, showing that the scoring logic does surface relevant matches.

---

## 6. Limitations and Bias

**Energy Gap Filter Bubble**: The scoring algorithm uses a narrow Gaussian distribution (sigma=0.3) for energy matching with a 2.0 weight, which creates hard partitions between low-energy (lofi/ambient, 0.15–0.42) and high-energy (rock/pop/metal, 0.75–0.94) music. Users who prefer calm music will almost never receive energetic recommendations and vice versa, because songs outside their energy range score near zero. This prevents serendipitous discovery and locks users into narrow listening patterns based on a single preference dimension.

Additionally, the system ignores the `likes_acoustic` user preference entirely—it is defined in the profile but never used in scoring. This means users who prefer acoustic music receive no boost for acoustic songs, while acoustic music itself clusters in low-energy genres, making it impossible for a user wanting both acoustic music and high energy to find matches.

---

## 7. Evaluation

I tested the recommender with three distinct user profiles to see if it captured different musical tastes:

1. **The Lofi Chiller** (favorite_mood="chill", target_energy=0.3): Expected recommendations from lofi/ambient artists. ✓ Worked well—received songs like "Midnight Coding" and "Library Rain."

2. **The Happy Pop Fan** (favorite_mood="happy", target_energy=0.5): Wanted upbeat but not exhausting pop music. ⚠️ Problem: "Gym Hero" (intense pop, 0.93 energy) ranked almost as high as "Sunrise City" (happy pop, 0.82 energy). The algorithm cares more about genre and raw energy than about the *type* of energy the user wants.

3. **The Acoustic Lover** (likes_acoustic=True, target_energy=0.6): Expected songs with guitar and natural instruments. ✗ Failed completely—the `likes_acoustic` preference was never used, so acoustic and non-acoustic songs were scored identically.

**What Surprised Me**: The system conflates different moods ("happy" vs "intense") because they're both energetic. Users looking for relaxing happiness got energetic intensity instead. Also, the UserProfile class expects only four fields, but the scoring function tries to use target_danceability and target_valence fields that don't exist in the profile—this mismatch silently breaks personalization for those preferences.

### Algorithm Modification: Energy-Prioritized Approach

**The Experiment**: We modified the original scoring to double the weight on energy (from 1.0 to 2.0 points) and halved genre importance (from 1.0 to 0.5 points). The hypothesis was that recommending based on *how a song feels* (energy) matters more than matching exact genre categories.

**How It Changed Output**:
- **Before**: A pop fan would get any pop song that matched their mood, regardless of energy. "Gym Hero" (intense pop) ranked equally with "Sunrise City" (happy pop) if both hit the mood.
- **After**: Energy now dominates the score. Users with target_energy=0.5 see a bigger gap between 0.82-energy songs and 0.93-energy songs. Conversely, a rock fan looking for chill music (low energy) might now get an energetic pop song that matches their energy target, not their genre preference.

**The Trade-off**: This made recommendations feel more emotionally aligned but less genre-loyal. A user saying "I want jazz" might now get electronic music if it matched their energy better. For some users this was good (avoiding genre pigeonholing), but for others it felt less intuitive (why did I get this genre?). The modification exposed that there's no "right" answer—only different trade-offs between feature importance.

---

## 8. Future Work  

The biggest improvement would be to actually implement the `likes_acoustic` preference and add fuzzy mood matching so "peaceful" and "relaxed" users can find similar songs. We should also prevent the top 5 from all being the same artist and soften the energy Gaussian (wider sigma) so users get some cross-genre serendipity. Finally, showing detailed explanations—like "This song matches your energy target (0.5) but has a different mood (intense vs. happy)"—would help users understand why they're getting unexpected recommendations.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

**Biggest Learning Moment**:
I learned how many variables are in play in recommendation systems, and the difficulty that is inherent in deciding which variables should weigh more or less than other variables.

Interestingly, modifying variables that I thought were very important (i.e., halving the importance of genre and doubling the importance of energy) had less of an effect than I expected. This goes to show how my understanding of the variable weights is not yet as strong as it needs to be in order to design a usable recommendation system. After this project, I have more empathy for recommendation systems like Spotify's, which I am quick to negatively criticize.

**How did AI Help Me?**:
Claude Code did a good job of helping me decide what variables to prioritize. There were times where I needed to double-check Claude's work to ensure that it remained in line with my goals.

**What Surprised Me**:
Despite the simplicity of this system, I was surprised at how well it worked out of the box. It isn't production-level, but it helped me understand how recommendation algorithms work at a bare-bones level.

**What I'd Try Next**:
I would include more variables in the recommendation system to make the system more robust and production ready.
