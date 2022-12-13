import spacy
nlp = spacy.load("de_dep_news_trf")
doc = nlp("Dies ist ein Satz.")
print([(w.text, w.pos_) for w in doc])