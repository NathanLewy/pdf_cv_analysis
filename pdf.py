import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
import langid
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification


def extract_words_with_positions(pdf_path):
    doc = fitz.open(pdf_path)
    words_with_positions = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        words = page.get_text("words")  # Récupère une liste de mots avec leurs positions
        for word in words:
            
            x0, y0, x1, y1, word_text, block_no, line_no, word_no = word  # x0, y0 = coin supérieur gauche, x1, y1 = coin inférieur droit
            word_text = ''.join(char for char in word_text if char in 'abscdefghijklmnopqrstuvwxyzôâêîûèéàçòìABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_,.@&:;!/?$()-+')  # Supprimer les caractères spéciaux
            if word_text!='':
                words_with_positions.append((word_text, x0, y0, x1, y1))
    
    return words_with_positions






def create_pdf_from_words_with_rects(words_with_positions, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    
    for word, x0, y0, x1, y1 in words_with_positions:
        c.setFont("Helvetica", 10)
        
        # Position du texte
        c.drawString(x0, 750 - y0, word)
        
        # Dessiner un rectangle autour du mot
        c.setStrokeColorRGB(1, 0, 0)  # Couleur du contour en rouge
        c.setLineWidth(0.5)
        c.rect(x0, 750 - y0, x1 - x0, y1 - y0)  # rectangle (x0, y0) à (x1, y1)
    
    c.save()

def collide(A,B):
        wA, x0A, y0A, x1A, y1A = A
        wB, x0B, y0B, x1B, y1B = B
        for x1 in [x0A, x1A]:
            for y1 in [y0A, y1A]:
                if x1 > x0B and x1 < x1B:
                    if y1 > y0B and y1 < y1B:
                        return True
        return False

def dist_box(A,B):
    if collide(A,B):
        return 0
    else:
        wA, x0A, y0A, x1A, y1A = A
        wB, x0B, y0B, x1B, y1B = B
        mindist = float('inf')
        for x1 in [x0A, x1A]:
            for y1 in [y0A, y1A]:
                for x2 in [x0B, x1B]:
                    for y2 in [y0B, y1B]:
                        if (x1-x2)**2 + (y1-y2)**2 < mindist:
                            mindist = abs(x1-x2) + abs(y1-y2)
        return mindist

def dist_cluster(C1,C2):
        dmin = float('inf')
        for i in C1:
            for j in C2:
                if dist_box(i, j)< dmin:
                    dmin = dist_box(i,j)
        return dmin

def same_size(C1,C2):
    wA, x0A, y0A, x1A, y1A = C1[0]
    wB, x0B, y0B, x1B, y1B = C2[0]
    return abs(abs(y1A - y0A) - abs(y1B - y0B))<0.1

def group_words(words_with_positions):
    clusters=[[i] for i in words_with_positions]
    fusion_happened = True
    while fusion_happened:
        #print(clusters)
        fusion_happened = False
        for c1 in clusters:
            dmin = float('inf')
            tofuse = False
            for c2 in clusters:
                if c1!=c2 and same_size(c1,c2):
                    if dist_cluster(c1,c2)<dmin:
                        dmin = dist_cluster(c1,c2)
                        tofuse = c2
            if tofuse and dmin <30:
                clusters.remove(c1)
                clusters.remove(tofuse)
                clusters.append(c1 + tofuse)
                fusion_happened = True
    return clusters

def create_pdf_clusters(clusters, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    for cluster in clusters :
        col = np.random.randint([255,255,255])/255
        for (word, x0, y0, x1, y1) in cluster:
            c.setFont("Helvetica", 10)
            
            # Position du texte
            c.drawString(x0, 750 - y0, word)
            
            # Dessiner un rectangle autour du mot
            c.setStrokeColorRGB(col[0], col[1], col[2])  # Couleur du contour en rouge
            c.setLineWidth(0.5)
            c.rect(x0, 750 - y0, x1 - x0, y1 - y0)  # rectangle (x0, y0) à (x1, y1)
    
    c.save()

def order_clusters(clusters):
    liste_paragraphe = []
    for c in clusters:
        paragraphe = []
        for i in c:
            if paragraphe==[]:
                paragraphe.append(i)
            else:
                index = 0
                found = False
                while index<=len(paragraphe)-1 and not found:
                    if paragraphe[index][2]>i[2] or (paragraphe[index][1]>i[1] and paragraphe[index][2]>=i[2]):
                        found=True      
                    else:
                        index+=1
                paragraphe.insert(index, i)
        liste_paragraphe.append([i[0] for i in paragraphe])
    return liste_paragraphe
        

def unite_paragraphs(paragraphs):
    text=''
    for p in paragraphes:
        for mot in p:
            text+=mot + ' '
    return text            


words = extract_words_with_positions("cv2.pdf")
clusters = group_words(words)

paragraphes = order_clusters(clusters)


create_pdf_from_words_with_rects(words, "output_with_rects.pdf")
create_pdf_clusters(clusters, "output_with_clusters.pdf")
cv_text = unite_paragraphs(paragraphes)
print(paragraphes)

#detect language and coose nlp model
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
    for p in paragraphes:
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

    
