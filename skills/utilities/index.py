def read_stopwords(filename):
    with open(filename, 'r') as file:
        stopwords = [line.strip() for line in file]
    return stopwords

def filter_arr(words, stopwords):

    # Filter out stopwords
    filtered_words = [word for word in words if word not in stopwords]

    return filtered_words
