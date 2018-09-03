import nltk


def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'PERSON':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names


def TrazerEntidadesNomeadas(path_noticia):
    with open(path_noticia, 'r') as f:
        sample = f.read()
    sentences = nltk.sent_tokenize(sample)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)
    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)

        entity_names.extend(extract_entity_names(tree))
    return entity_names


def trazer_entidades_nomeadas_v(texto):
    """ Obtem as entidades nomeadas de uma string"""
    sentences = nltk.sent_tokenize(texto)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=False)
    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)
        entity_names.extend(extract_entity_names(tree))
    '''
    nomes_completos = []
    for i in range(0, len(entity_names)):
        if i < (len(entity_names) - 1):
            name = entity_names[i] + " " + entity_names[i + 1]
            nomes_completos.append(name)
    entity_names = entity_names + nomes_completos
    for nome in entity_names:
        print(nome)
    '''
    return entity_names


# Print all entity names
#print (entity_names)

# Print unique entity names
#print (TrazerEntidadesNomeadas())