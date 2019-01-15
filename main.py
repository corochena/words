from collections import Counter
import os
import pandas as pd
import matplotlib.pyplot as plt

def read_book(title_path):
    with open(title_path, "r", encoding="utf8") as current_file:
        text = current_file.read()
        text = text.replace("\n","").replace("\r","")
    return text

def count_words(text):
    text = text.lower()
    skips = [".",",",";",":","'",'"']
    for ch in skips:
        text = text.replace(ch, "")
        
    word_counts = {}
    for word in text.split(" "):
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts
    
def count_words_fast(text):
    text = text.lower()
    skips = [".",",",";",":","'",'"']
    for ch in skips:
        text = text.replace(ch, "")
        
    word_counts = Counter(text.split(""))
    return word_counts

def word_stats(word_counts):
    num_unique = len(word_counts)
    counts = word_counts.values()
    return (num_unique, counts)

# lets compare the output of the two functions
text = "This is my test text. We're keeping this text short to keep things manegeable."
count_words(text) == count_words_fast(text) # it must return True

# lets find an extract of Romeo and Juliet
text = read_book(".Books/English/shakespeare/Romeo and Juliet.txt")
len(text)
ind = text.find("What's in a name")
sample_text = text[ind:ind+1000]

# lets do some stats
word_counts = count_words(text)
(num_unique, counts) = word_stats(word_counts)
sum(counts)

# lets compare English and German versions of Romeo and Julieth
text = read_book(".Books/English/shakespeare/Romeo and Juliet.txt")
word_counts = count_words(text)
(num_unique, counts) = word_stats(word_counts)
print(num_unique, sum(counts))

text = read_book(".Books/German/shakespeare/Romeo und Julia.txt")
word_counts = count_words(text)
(num_unique, counts) = word_stats(word_counts)
print(num_unique, sum(counts))

# reading multiple files and storing info in a pandas DataFrame
stats = pd.DataFrame(columns = ("language","author","title","length","unique"))
title_num = 1

book_dir = "./Books"
for lang in os.listdir(book_dir):
    for author in os.listdir(book_dir + "/" + lang):
        for title in os.listdir(book_dir + "/" + lang + "/" + author):
            input_file = book_dir + "/" + lang + "/" + author + "/" + title
            print(input_file)
            text = read_book(input_file)
            (num_unique, counts) = word_stats(count_words_fast(text))
            stats.loc[title_num] = lang, author.capitalize(), title.replace(".txt", ""), sum(counts), num_unique
            title_num += 1

# shows all table, head or tail
stats
stats.head()
stats.tail()

# lets plot unique words vs total length
plt.plot(stats.length, stats.unique, "bo")
# now using a loglog
plt.loglog(stats.length, stats.unique, "bo")

#lets stratify by language
plt.figure(figsize = (10,10))
subset = stats[stats.language == "English"]
plt.loglog(subset.length, subset.unique, "o", label="English", color="crimson")
subset = stats[stats.language == "French"]
plt.loglog(subset.length, subset.unique, "o", label="French", color="forestgreen")
subset = stats[stats.language == "German"]
plt.loglog(subset.length, subset.unique, "o", label="German", color="orange")
subset = stats[stats.language == "Portuguese"]
plt.loglog(subset.length, subset.unique, "o", label="Portuguese", color="blueviolet")
plt.legend()
plt.xlabel("Book length")
plt.ylabel("Number of Unique words")
plt.savefig("lang_plot.pdf")
