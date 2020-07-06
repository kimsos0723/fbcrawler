# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze

def analyze(text: str):
    document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT,
    language='ko')    
    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    return (sentiment.score, round(sentiment.magnitude,4))
