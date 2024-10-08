import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.db import connection

class ProductFilterBot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('spanish'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('spanish'))

    def preprocess_text(self, text):
        try:
            tokens = word_tokenize(text.lower())
        except LookupError:
            nltk.download('punkt')
            tokens = word_tokenize(text.lower())
        
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
        tokens = [token for token in tokens if token not in self.stop_words]
        return ' '.join(tokens)

    def filter_products(self, category):
        preprocessed_category = self.preprocess_text(category)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name, description, price
                FROM myapp_product
                WHERE LOWER(description) LIKE %s
            """, ['%' + preprocessed_category + '%'])
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]