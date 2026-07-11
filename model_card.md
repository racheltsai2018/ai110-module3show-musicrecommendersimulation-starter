# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **Favorite song finder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration 

The recommender makes song recommendations based on the user's favorite genre, mood, and energy levels. The recommender currently makes the assumption that each user only have one favorite genre and mood. Currently, the recommender is more suitable for classroom exploration since the tool is not complete enough for it, and the dataset is too small for the recommender to be used by real users. 

---

## 3. How the Model Works  

There are 3 features that are used for each song: genre, mood, and energy. If the song matches the user's favorite genre, the system will add 1 point to the score. If the song's mood matches the user's favorite mood, another 1 point will be added. Energy is calculated with the formula 2x(1- difference in energy), so the max amount that can be gained is +2 points if the energy matches perfectly.

---

## 4. Data  

The catalog currently contains a total of 18 songs. There are a total of 16 different genres in the dataset including pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, world soul, techno, country, classical, reggae, drum and bass. There are a total of 14 different moods including happy, chill, intense, focused, confident, mystical, melancholy, euphoric, nostalgic, somber, carefree, aggressive, moody, and relaxed. The dataset started with a total of 10 songs, and 8 songs were added. 

---

## 5. Strengths  

The system works well by making song recommendations that matches the user's preferences based on the available songs in the dataset. When there there are not songs that matches the user's favorite genre or mood, the system still makes recommendations based on matching energy levels. As a results, the system is still able to make song recommendations the users may be interested in. 

---

## 6. Limitations and Bias 

After the changes for weight shift was made in step 3, the is a bias toward energy since each song can gain a total of 2 points in the energy field. The genre and moods can only gain a total of 1 points each, therefore, genres and moods are underrepresented compared to energy. If the system want to remove this bias, the energy category can be change to gain a maximum of 1 point. 

---

## 7. Evaluation  

Some user profiles that was tested included:
User profile 1: Favorite genre: pop, mood: happy, and energy: 0.8
User profile 2: Favorite genre: soul, mood: melancholy, energy: 0.95
User profile 3: Favorite genre: pop mood: happy, and energy:2.0

Something that surprised me when testing with profile 3 was that recommended songs 4&5 gained negative points. However, analyzing the results, I realized it was because there was no more matches for genre and mood, so the points came from energy category. 

For User profile 1, the order of recommended song for Rootop Lights - Indigo Parade and Gym Hero - Max Pulse was swapped after making the changes in step 3. For User profile 2 and 3, the order of the recommended songs stayed the same and only the score for each song changed slightly, which is resonable considering the importance of energy was doubled and importance of genre was halved.

---

## 8. Future Work  

The model can be improved by making sure when the system is making recommendations, it will take into account all the available features. In the dataset, features like acousticness, danceability, valence, and tempo are all included. These feature could be used so the recommendations made could match the user's preferences more perfectly. In order to improve the system, it would also be better to add more songs to the dataset. 

---

## 9. Personal Reflection  

From this project, it gave me a basic insight on how song recommendation system works. I learned about collaborative filtering and content-based filtering, which are both concepts I have never heard of before starting this project. Using AI tools helped me speed up the programming process, however since AI tools still makes mistakes, I still double-check the code whenever AI tools make changes to the files. Something I would try next aside from the changes made in the future work section if this project was extended was adding the ability to have multiple favorite genre or mood, or allow the users to save/change their favorite genre or mood depending how they are feeling right now. An example would be I'm feeling happy so my favorite song genre would be pop and mood would be happy. However, when I am feeling sad, my favorite genre would be soul and mood would be sad or chill. 
