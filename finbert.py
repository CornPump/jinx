import json
import os
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

BERT_FINANCIAL_MODEL = 'yiyanghkust/finbert-tone'
BERT_FINANCIAL_MODEL_MAX_TOKENS = 512
OUTPUT_FILE_NAME = 'sentiment_data.json'

class Sentiment:

    def __init__(self, dir: str,  model: str, max_tokens: int, json_data=[]):
        self.dir = dir
        if json_data:
            self.json_data = json_data
        else:
            self.json_data = os.listdir(self.dir)
        self.json_data = json_data
        self.model = model
        self.max_tokens = max_tokens
        self.sentiment_data = []

    def params(self):
        return {'dir': self.dir, 'model': self.model,
         'sentiment_data': self.sentiment_data}

    @staticmethod
    def fix_high_token_comments(comment: str) -> str:
        return ''

    def dump_sentiment_data(self):

        path = os.path.join(self.dir,OUTPUT_FILE_NAME)
        print('Dumping sentiment_data into file ', path)

        with open(path, 'w') as f:
            json.dump(self.sentiment_data,f)


    def create_file_sentiment_score(self, llm_output, file, ignore_neutral=True):

        num_comments_for_sentiment = num_comments = 0
        sentiment_score = 0

        for val in llm_output:
            num_comments += 1
            if val['label'] == 'Negative':
                sentiment_score += 1
                num_comments_for_sentiment += 1
            elif val['label'] == 'Positive':
                sentiment_score -= 1
                num_comments_for_sentiment += 1
            # Neutral
            else:
                pass
        try:
            final_score = sentiment_score/num_comments_for_sentiment
        except ZeroDivisionError:
            print("Zero comments to evaluate upon")
            final_score = 0

        self.sentiment_data.append({'file': file, 'sentiment_score': final_score,
                                    'num_comments': num_comments, 'num_comments_analyzed':num_comments_for_sentiment})
        print({'file': file, 'sentiment_score': final_score,
                                    'num_comments': num_comments, 'num_comments_analyzed':num_comments_for_sentiment})

    def sentiment_analysis(self, whole_dir=False, file_lst=[]):
        print("Starting sentiment_analysis()...")
        finbert = BertForSequenceClassification.from_pretrained(self.model, num_labels=3)
        tokenizer = BertTokenizer.from_pretrained(self.model)

        nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)
        if whole_dir:
            loop_lst = os.listdir(self.dir)
            print(f"Running on whole dir {self.dir}")
        else:
            loop_lst = file_lst
            print(f"Running on prepared json files list")

        for file in loop_lst:
            print(f"Analyzing sentiment for file {file}")
            path = os.path.join(self.dir, file)
            with open(path, 'r', encoding="utf8") as f:
                lst = json.load(f)
            file_data = []
            for comment in lst:
                comment = comment['body']
                tokens = tokenizer.encode_plus(comment, add_special_tokens=False)
                if len(tokens['input_ids']) >= BERT_FINANCIAL_MODEL_MAX_TOKENS:
                    comment = Sentiment.fix_high_token_comments(comment)
                if comment:
                    try:
                        results = nlp(comment)
                        file_data.append({'label': results[0]['label'],
                                          'score': results[0]['score']})
                    except Exception as e:
                        print(e)


            Sentiment.create_file_sentiment_score(self, file_data, file)
