from flair.data import Sentence
from flair.models import SequenceTagger

# load tagger
tagger = SequenceTagger.load("flair/ner-german-legal")

# make example sentence (don't use tokenizer since Rechtstexte are badly handled)
sentence = Sentence("Herr W. verstieß gegen § 36 Abs. 7 IfSG.", use_tokenizer=False)


# predict NER tags
tagger.predict(sentence)

# print sentence
print(sentence)

# print predicted NER spans
print('The following NER tags are found:')
# iterate over entities and print
for entity in sentence.get_spans('ner'):
    print(entity)

