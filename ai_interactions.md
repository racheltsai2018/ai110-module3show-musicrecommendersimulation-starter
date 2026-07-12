# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Challenge 1
I asked the Claude agent to generate 5 or more attributes to the dataset, including song popularity, release decade, and detailed mood tags.

Challenge 3
I asked Claude agent to implement a diveristy penalty that prevents the recommender from suggesting too many songs from the same artist.

Challenge 4
I asked Claude agent to suggest a way to use the tabulate library to put the results in a table for the terminal.

**Prompts used:**

Challenge 1
Generate 5 or more complex attributes that are not currently present in the dataset, some example include Song Popularity, Release Decade, or Detailed Mood Tags.

Challenge 3
Implement a Diversity Penalty that prevents the recommender from suggesting too many songs from the same artist.

Challenge 4
Make suggestions to use the library tabulate to display the top recommendations. Each recommendation needs to display the reasons for each score in the table. 

**What did the agent generate or change?**

Challenge 1
5 new attributes were added to the dataset (data/songs.csv). The attributes include popularity, release_decade, mood_tags, language, and explicit. Updated the method load_songs() to add the new attributes. 

The agent then ran test to ensure the code is working properly.

python -m pytest -q 2>&1 | tail -3 && python -c "
from src.recommender import load_songs, recommend_songs
songs = load_songs('data/songs.csv')
total = len(songs)
clean = recommend_songs({'allow_explicit':False}, songs, k=99)
allsongs = recommend_songs({'allow_explicit':True}, songs, k=99)
print('catalog:', total)
print('clean-only count:', len(clean), '-> explicit titles present:', any(s['explicit'] for s,_,_ in clean))
print('allow-explicit count:', len(allsongs))
"

Challenge 3

The agent implemented greedy re-ranking in the recommended_songs method. The greedy re-ranking works by scoring the songs the same way, when a song is recommended, any other songs with the same artist or genre gets their scores docked. 

The agent ran tests to ensure the function is still working properly. 
python -m src.main --genre pop --mood happy --energy 0.8 -k 5

python -m pytest tests/ -q 2>&1 | tail -20

Challenge 4
The agent added a method called format_recommendations() in main.py. The format_recommendations() work by building rows of ID, title, artist, score, and reasons, then putting them in a table with the library tabulate.

**What did you verify or fix manually?**

Something I changed was regarding the explicit attribute. It was originally another attribute that added to the score if it matches the user's preference. I changed it to a filter, when users do not want explicit songs, explicit songs will not show on their recommended list.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
