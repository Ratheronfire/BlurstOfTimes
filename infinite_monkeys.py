import distance
import random
import sys
from io import open


similarity_memo = dict()
words = []
target_sentence = 'it was the best of times it was the worst of times'


def load_words():
    global words

    words_file = open('words.txt', 'r')
    for line in words_file:
        if line.islower(): # avoid proper nouns
            words.append(line.replace("\n", ""))

    words_file.close()

def generate_sentence():
    sentence = words[random.randint(0, len(words) - 1)].lower()
    for i in range(3):
        sentence += " " + words[random.randint(0, len(words) - 1)].lower()

    return sentence

def generate_sentence_herd():
    herd = []

    for i in range(20):
        herd.append((sys.maxsize, generate_sentence()))

    return herd

def test_similarity(sentence):
    if sentence in similarity_memo:
        return similarity_memo[sentence]


    similarity = distance.levenshtein(target_sentence, sentence)
    similarity_memo[sentence] = similarity

    return similarity

def test_herd(herd):
    ranking = []

    for subject in herd:
        sentence = subject[1]

        fitness = test_similarity(sentence)

        ranking.append((fitness, sentence))

    ranking = sorted(ranking)

    return ranking[0:15]

def breed_herd(herd):
    children = []

    trimmed_herd = [sentence[1] for sentence in herd]

    for sentence_a in trimmed_herd:
        for sentence_b in trimmed_herd:

            if random.random() > .25 and not sentence_a == sentence_b:
                first = sentence_a.split(" ")
                second = sentence_b.split(" ")

                if len(first) < len(second):
                    temp = first
                    first = second
                    second = temp

                pivot = random.randint(int(len(first) / 3), int(len(first) / 1.333))

                child_words = first[:pivot] + second[pivot:]
                child = ' '.join(child_words)

                children.append((test_similarity(child), child))

    return herd + children

def mutate(herd):
    for i in range(len(herd)):
        if random.random() < .25:
            sentence_words = herd[i][1].split(" ")

            for j in range(len(sentence_words)):
                if random.random() < .25:
                    sentence_words[j] = words[random.randint(0, len(words) - 1)]

            new_sentence = ' '.join(sentence_words)
            herd[i] = (herd[i][0], new_sentence)

    return herd

def process_generation(cycles=-1.0, target_fitness=-1.0):
    load_words()

    herd = generate_sentence_herd()

    using_cycles = not cycles == -1.0
    using_fitness = not target_fitness == -1.0

    i = 0
    while True:
        try:
            herd = test_herd(herd)

            i += 1
            best_fitness = herd[0][0]

            print("Generation {0} - Best fitness ranking: {1}".format(i, best_fitness))

            herd = breed_herd(herd)
            herd = mutate(herd)

            if (using_cycles and i >= cycles) or \
                (using_fitness and best_fitness <= target_fitness):
                break
        except KeyboardInterrupt:
            break

    herd = test_herd(herd) # cull bad sentences one last time
    herd = list(set(herd)) # remove duplicate sentences

    return herd


herd = process_generation(cycles=100000, target_fitness=0)

for sentence in herd:
    print(sentence[1], "- Fitness:", sentence[0])