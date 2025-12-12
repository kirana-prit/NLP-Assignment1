import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string
from collections import Counter

# nltk.download('punkt')
# nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

# Function to fix wrapped lines
def fix_wrapped_lines(text):
    fixed = []
    buffer = ""

    for line in text.split("\n"):
        stripped = line.strip()
        if stripped == "":
            if buffer:
                fixed.append(buffer)
                buffer = ""
            fixed.append("")
        else:
            if buffer:
                buffer += " " + stripped
            else:
                buffer = stripped

            if stripped.endswith((".", "?", "!")):
                fixed.append(buffer)
                buffer = ""
    if buffer:
        fixed.append(buffer)
    return "\n".join(fixed)

def process_text(input_file):
    # open and read the input file
    print('reading input file...')
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    # fix wrapped lines
    text = fix_wrapped_lines(text)
    
    # tokenize sentences from original text before cleaning
    sentences = sent_tokenize(text)
    # perform text cleaning
    print('cleaning text...')
    text = text.lower()  # convert to lowercase
    text = text.replace('-', ' ')  # remove hyphens
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation

    text = text.replace('\t', ' ')  # replace tabs with spaces
    
    cleaned_lines = []
    for line in text.split("\n"):
        tokens = word_tokenize(line)
        filtered = [w for w in tokens if w not in stop_words]

        if len(filtered) == 0:
            cleaned_lines.append("")   # keep a blank line (but only 1)
        else:
            cleaned_lines.append(" ".join(filtered))

    # collapse multiple blank lines to 1 blank line
    cleaned_text = re.sub(r"\n\s*\n+", "\n\n", "\n".join(cleaned_lines))

    # write cleaned.txt
    with open("cleaned.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    
    print('text cleaning complete.')
    
    # perform tokenization and sentence splitting
    print('tokenizing text...')

    # tokenize words from cleaned text
    words = word_tokenize(cleaned_text.lower())
    # remove any remaining punctuation and empty strings
    words = [w for w in words if w.isalnum()]
    
    # write words.txt
    with open("words.txt", "w", encoding="utf-8") as f:
        f.write(f"Total words (after cleaning): {len(words)}\n\n")
        f.write("Words list:\n")
        f.write(", ".join(words))
        
    # write sentences.txt
    with open("sentences.txt", "w", encoding="utf-8") as f:
        for i, sentence in enumerate(sentences, 1):
            f.write(f"{i}. {sentence.strip()}\n\n")
    
    print('tokenization complete.')  
      
    # perform top 10 word frequent
    print('calculating word frequencies...')
    freq = Counter(words)
    top10 = freq.most_common(10) # get top 10 words
    # write top10words.txt
    with open("top10words.txt", "w", encoding="utf-8") as f:
        for word, count in top10:
            f.write(f"{word}: {count}\n")
    print('top 10 words calculation complete.')
    
    
    
process_text('alice29.txt')