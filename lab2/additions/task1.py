text = []
sentences = []
with open('text.txt', 'r') as file:
    data = file.read()
    words = data.split()
    sentences = data.split('.')
    sentences.remove('')
    text = [word.rstrip(',.?!').lower() for word in words]

#print(text)

def words_dict(text):
    stats = {}
    for word in text:
        if len(stats.keys()) == 0:
            stats[word] = 1
        else:
            was_mansioned = False
            for key in stats.keys():
                if key == word:
                    stats[word] += 1
                    was_mansioned = True
                    break
            if not was_mansioned:
                stats[word] = 1
    return stats

def words_per_sentences(sentences, text):
    return len(text) / len(sentences)

def median_words(sentences):
    sorted_lens = [len(sentence.split()) for sentence in sentences]
    sorted_lens.sort()
    return sorted_lens[int(len(sentences) / 2)]

def n_gramm(text): pass
print(median_words(sentences))