from transformers import pipeline

# Initialisierung der Modelle
twitter_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")

def classifier(comment):
    # Kommentar wird ins Englische übersetzt
    translated_results = translator(comment, src_lang="de", tgt_lang="en")
    
    # Extrahieren des übersetzten Textes aus dem Ergebnis
    translated_text = translated_results[0]['translation_text']

    # Klassifizierung des übersetzten Textes
    result = twitter_model(translated_text)

    labels = [item['label'] for item in result]

    return labels[0]
