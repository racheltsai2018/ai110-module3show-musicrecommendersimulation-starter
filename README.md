# 🎵 Music Recommender Simulation

## Project Summary

The recommender saves the user's favorite song genre, mood, and energy level. The recommender will then make song recommendations based on the user's favorite genre, mood, and energy levels.

---

## How The System Works

The real-world recommendation utilizes collaborative filter and content-based filtering to make recommendations for the users. The collaborative filtering will reference other users with similar preferences to make recommendations for the songs. The content-based filtering make recomendations on the different features. The features each 'song' use in my system includes genre, mood, and energy. Since 'Song' uses genre, mood, energy, it is important to store the favorite genre, favorite mood, and energy level in 'UserProfile'. The 'Recommender' compute a score for each song by adding +2 points if the Genre Match the user's favorite genre, +1 if it matches the user's favorite mood, and + up to 1 point the closer the energy matches. To choose which songs to recommend, after computing a score for each song, the songs are sorted, the top songs are then recommended first.

### Algorithm Recipe
Each song will start with a score of 0, if the genre matches the score will increase by 2, and if the mood matches, the score will increase by 1. The closer the value of the energy the higher the score, with the most increasing the score by 1 point. 

The system will prioritize genre over mood and energy since a matching genre will give +2 points. As a result, other songs that match the user's mood or energy may be ignored. 


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

### Phase 3 Step 4

```text
Loaded songs: 18

====================================================
  TOP RECOMMENDATIONS FOR YOU
  genre=pop  mood=happy  energy=0.8
====================================================

  1. Sunrise City - Neon Echo
     Score: 3.98
     Reasons:
       - genre match (pop) (+2.0)
       - mood match (happy) (+1.0)
       - energy closeness (song 0.82 vs target 0.80) (+0.98)

  2. Gym Hero - Max Pulse
     Score: 2.87
     Reasons:
       - genre match (pop) (+2.0)
       - energy closeness (song 0.93 vs target 0.80) (+0.87)

  3. Rooftop Lights - Indigo Parade
     Score: 1.96
     Reasons:
       - mood match (happy) (+1.0)
       - energy closeness (song 0.76 vs target 0.80) (+0.96)

  4. Concrete Prophet - Iron Verse
     Score: 1.00
     Reasons:
       - energy closeness (song 0.80 vs target 0.80) (+1.00)

  5. Night Drive Loop - Neon Echo
     Score: 0.95
     Reasons:
       - energy closeness (song 0.75 vs target 0.80) (+0.95)

====================================================
```

After performing the changes in step 3:
```text
====================================================
  TOP RECOMMENDATIONS FOR YOU
  genre=pop  mood=happy  energy=0.8
====================================================

  1. Sunrise City - Neon Echo
     Score: 3.96
     Reasons:
       - genre match (pop) (+1.0)
       - mood match (happy) (+1.0)
       - energy closeness (song 0.82 vs target 0.80) (+1.96)

  2. Rooftop Lights - Indigo Parade
     Score: 2.92
     Reasons:
       - mood match (happy) (+1.0)
       - energy closeness (song 0.76 vs target 0.80) (+1.92)

  3. Gym Hero - Max Pulse
     Score: 2.74
     Reasons:
       - genre match (pop) (+1.0)
       - energy closeness (song 0.93 vs target 0.80) (+1.74)

  4. Concrete Prophet - Iron Verse
     Score: 2.00
     Reasons:
       - energy closeness (song 0.80 vs target 0.80) (+2.00)

  5. Night Drive Loop - Neon Echo
     Score: 1.90
     Reasons:
       - energy closeness (song 0.75 vs target 0.80) (+1.90)

====================================================
```

### Phase 4 step 1

Profile 1 (favorite genre: soul, mood: melancholy, energy: 0.95)
```text
====================================================
  TOP RECOMMENDATIONS FOR YOU
  genre=soul  mood=melancholy  energy=0.95
====================================================

  1. Velvet Heartbreak - Ruby Lane
     Score: 3.53
     Reasons:
       - genre match (soul) (+2.0)
       - mood match (melancholy) (+1.0)
       - energy closeness (song 0.48 vs target 0.95) (+0.53)

  2. Neon Warfare - Grid Assault
     Score: 1.00
     Reasons:
       - energy closeness (song 0.95 vs target 0.95) (+1.00)

  3. Gym Hero - Max Pulse
     Score: 0.98
     Reasons:
       - energy closeness (song 0.93 vs target 0.95) (+0.98)

  4. Storm Runner - Voltline
     Score: 0.96
     Reasons:
       - energy closeness (song 0.91 vs target 0.95) (+0.96)

  5. Bassline Underground - Deep Cycle
     Score: 0.93
     Reasons:
       - energy closeness (song 0.88 vs target 0.95) (+0.93)

====================================================
```

After performing changes in step 3:
```text
====================================================
  TOP RECOMMENDATIONS FOR YOU
  genre=soul  mood=melancholy  energy=0.95
====================================================

  1. Velvet Heartbreak - Ruby Lane
     Score: 3.06
     Reasons:
       - genre match (soul) (+1.0)
       - mood match (melancholy) (+1.0)
       - energy closeness (song 0.48 vs target 0.95) (+1.06)

  2. Neon Warfare - Grid Assault
     Score: 2.00
     Reasons:
       - energy closeness (song 0.95 vs target 0.95) (+2.00)

  3. Gym Hero - Max Pulse
     Score: 1.96
     Reasons:
       - energy closeness (song 0.93 vs target 0.95) (+1.96)

  4. Storm Runner - Voltline
     Score: 1.92
     Reasons:
       - energy closeness (song 0.91 vs target 0.95) (+1.92)

  5. Bassline Underground - Deep Cycle
     Score: 1.86
     Reasons:
       - energy closeness (song 0.88 vs target 0.95) (+1.86)

====================================================
```

Profile 2 (favorite genre: pop, mood: happy, energy: 2.0)
```text
====================================================
  TOP RECOMMENDATIONS FOR YOU
  genre=pop  mood=happy  energy=2.0
====================================================

  1. Sunrise City - Neon Echo
     Score: 2.82
     Reasons:
       - genre match (pop) (+2.0)
       - mood match (happy) (+1.0)
       - energy closeness (song 0.82 vs target 2.00) (+-0.18)

  2. Gym Hero - Max Pulse
     Score: 1.93
     Reasons:
       - genre match (pop) (+2.0)
       - energy closeness (song 0.93 vs target 2.00) (+-0.07)

  3. Rooftop Lights - Indigo Parade
     Score: 0.76
     Reasons:
       - mood match (happy) (+1.0)
       - energy closeness (song 0.76 vs target 2.00) (+-0.24)

  4. Neon Warfare - Grid Assault
     Score: -0.05
     Reasons:
       - energy closeness (song 0.95 vs target 2.00) (+-0.05)

  5. Storm Runner - Voltline
     Score: -0.09
     Reasons:
       - energy closeness (song 0.91 vs target 2.00) (+-0.09)

====================================================
```

Results for Profile 2 after performing change in step 3:
```text
====================================================
  TOP RECOMMENDATIONS FOR YOU
  genre=pop  mood=happy  energy=2.0
====================================================

  1. Sunrise City - Neon Echo
     Score: 1.64
     Reasons:
       - genre match (pop) (+1.0)
       - mood match (happy) (+1.0)
       - energy closeness (song 0.82 vs target 2.00) (+-0.36)

  2. Gym Hero - Max Pulse
     Score: 0.86
     Reasons:
       - genre match (pop) (+1.0)
       - energy closeness (song 0.93 vs target 2.00) (+-0.14)

  3. Rooftop Lights - Indigo Parade
     Score: 0.52
     Reasons:
       - mood match (happy) (+1.0)
       - energy closeness (song 0.76 vs target 2.00) (+-0.48)

  4. Neon Warfare - Grid Assault
     Score: -0.10
     Reasons:
       - energy closeness (song 0.95 vs target 2.00) (+-0.10)

  5. Storm Runner - Voltline
     Score: -0.18
     Reasons:
       - energy closeness (song 0.91 vs target 2.00) (+-0.18)

====================================================
```

---

## Experiments You Tried

For User profile 1, the order of recommended song for Rootop Lights - Indigo Parade and Gym Hero - Max Pulse was swapped after making the changes in step 3. For User profile 2 and 3, the order of the recommended songs stayed the same and only the score for each song changed slightly, which is resonable considering the importance of energy was doubled and importance of genre was halved.

---

## Limitations and Risks

There is currently a bias toward the energy feature in this system. The dataset is also too small to be able to find songs that will match the user's preferences closely.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

The project showed me what a basic song recommendation system looks like and how it functions to make song recommendations. The system does not have to actually understand the song like humans do to make song recommendations. This system also made me realize how easy it is to make a system biased towards a feature/ category. With a simple change of doubling the influence or reducing the influence the results can change. In the current system, the results are similar because there are only 18 songs available. However, if there are thousands of songs in the dataset, the result will most likely be completely different.



