from nltk.corpus import wordnet as wn

lst = wn.synsets('games', pos=wn.NOUN)
hyper = lambda s: s.hypernyms()
for j in range(0, len(lst)):
    synset = str(lst[j])
    synset = synset.replace("Synset('", "")
    synset = synset.replace("')", "")
    print(synset + " ----" + wn.synset(synset).definition())

person = wn.synset('game.n.05')
list(person.closure(hyper, depth=1)) == person.hypernyms()
print(list(person.closure(hyper)))