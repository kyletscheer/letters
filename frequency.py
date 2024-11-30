import itertools
import json
from collections import Counter, defaultdict

# Step 1: Load the JSON file
with open("dictionary.json", "r") as file:
    words = json.load(file)

# Step 2: Filter only 5-letter words
five_letter_words = [word for word in words if len(word) == 5]

# Step 3: Calculate Letter Frequencies
letter_frequencies = Counter()
position_frequencies = [Counter() for _ in range(5)]  # One counter for each position

for word in five_letter_words:
    letter_frequencies.update(word)  # Count each letter
    for index, letter in enumerate(word):  # Count position-specific frequencies
        position_frequencies[index][letter] += 1

# Normalize frequencies to dictionary
letter_frequencies = dict(letter_frequencies)
position_frequencies = [dict(position) for position in position_frequencies]

# Step 4: Calculate word scores
def calculate_word_score(word):
    score = 0
    for index, letter in enumerate(word):
        score += letter_frequencies.get(letter, 0)  # General frequency
        score += position_frequencies[index].get(letter, 0)  # Positional frequency
    return score

# Rank words by their score
ranked_words = sorted(five_letter_words, key=calculate_word_score, reverse=True)

# Step 5: Find the best combination of three words
def find_best_words(words, top_n=3):
    best_combination = None
    best_score = 0

    # Iterate over all combinations of the top 100 ranked words
    for combination in itertools.combinations(ranked_words[:100], top_n):
        combined_letters = set("".join(combination))
        score = sum(letter_frequencies[letter] for letter in combined_letters)
        if score > best_score:  # Maximize unique letter coverage and frequency
            best_combination = combination
            best_score = score

    return best_combination, best_score

# Get the top 3 optimal words
best_words, best_score = find_best_words(ranked_words)

# Step 6: Output Results
print("Top 15 Most Frequent Letters:")
print(sorted(letter_frequencies.items(), key=lambda x: x[1], reverse=True)[:15])

print("\nLetter Frequencies by Position:")
for i, position in enumerate(position_frequencies):
    print(f"Position {i + 1}: {sorted(position.items(), key=lambda x: x[1], reverse=True)[:5]}")

print("\nBest Starting Words for Wordle:")
print(f"Words: {best_words}")
print(f"Combined Score: {best_score}")
