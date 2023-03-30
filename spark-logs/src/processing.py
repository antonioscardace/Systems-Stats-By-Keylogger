from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from elasticsearch import Elasticsearch


ES_URL = 'http://elasticsearch:9200'
ES_INDEX = 'keylogger_stats'

es = Elasticsearch(
    ES_URL,
    verify_certs=False
)  
 

def get_sentiment(text):
    if not text.isnumeric():
        text = text.replace('[ENTER]', '\n')
        text = GoogleTranslator(source='auto', target='en').translate(text)

    vader = SentimentIntensityAnalyzer()
    sentiment = vader.polarity_scores(text)
    
    sentiment.update((k, v * 100) for k, v in sentiment.items())
    sentiment['grade'] = 'Positive' if sentiment['compound'] >= 5 else ('Negative' if sentiment['compound'] <= -5 else 'Neutral')

    return sentiment

    
def process_batch(df, id):
    for idx, row in enumerate(df.collect()):
        
        doc = row.asDict()
        doc.update(get_sentiment(doc['logtext']))
        print(doc)

        id_str = '{}-{}-0'
        id = id_str.format(id, idx)

        response = es.index(index=ES_INDEX, id=id, document=doc)
        print(response)
