# [BlurstOfTimes](https://www.youtube.com/watch?v=no_elVGGgW8)

A Python script using [genetic programming](https://en.wikipedia.org/wiki/Genetic_programming) to produce a given phrase.

## How It Works

The purpose of this program is to attempt to recreate a given phrase by randomly joining together words from a massive set of possible words.  It was inspired by the well-known [infinite monkey theorem](https://en.wikipedia.org/wiki/Infinite_monkey_theorem) which suggests that an infinite number of monkeys, typing on an infinite number of keyboards, would eventually be able to produce Shakespeare's entire works (or any sequence of characters, for that matter).

I use the Python [Distance](https://pypi.python.org/pypi/Distance/) library's ``levenshtein()`` function to calculate the exact number of additions, deletions, and changes needed to convert my generated sentence into the target sentence.
This value is used to calculate that sentence's "fitness", meaning how close it is to the desired outcome.

The general process is:

* Create a set of 20 sentences, by appending random words together (I ignore proper nouns for the sake of speeding things along).
* Assign each sentence a fitness value based on how close they are to the target sentence.
* Remove all but the top 15 most fit sentences from the set, ranked from lowest distance to highest.
* "Breed" the sentences: Randomly create new sentences by splicing together the beginning of one sentence and the end of another, and then add that sentence into the set.
* Apply mutations to certain sentences by replacing some words with new words from the whole set of possible words.
* Re-test these new strings for fitness, remove all but the top 15, and so on.

This process will run until either the set number of "generations" have been created, or the desired fitness is achieved.
