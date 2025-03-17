from read_pdf import *
import langid
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification




#detect language and coose nlp model
file = "./CV_database/cv2.pdf"
paragraphs = extract_txt(file)
cv_text = unite_paragraphs(paragraphs)
lang, _ = langid.classify(cv_text)

if lang == "fr":
    print("cv francais")
    nlp_ner = pipeline("ner", model="camembert-base", tokenizer="camembert-base")
    tag_name = ['PER']
elif lang == "en":
    print("cv anglais")
    nlp_ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
    tag_name = ['B-PER','I-PER']
else:
    print("Langue non prise en charge.")
    nlp_ner = None


if nlp_ner:
    names= []
    for p in paragraphs:
        txt = ' '.join(p)
        entities = nlp_ner(txt)
        memory_word = ''
        for e in entities:
            if e['entity'] in tag_name:
                if memory_word:
                    if e['word'].startswith('##'):
                        memory_word+=e['word'][2:]
                    else:
                        names.append(memory_word)
                        memory_word =e['word']
                else:
                    memory_word =e['word']

        if memory_word:
            names.append(memory_word)

print(names)

