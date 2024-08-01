from flask import Flask, request, jsonify, render_template
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

app = Flask(__name__)

class ParagraphSummarizer:
    def __init__(self, model_name='google/pegasus-xsum'):
        self.tokenizer = PegasusTokenizer.from_pretrained(model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_name)

    def summarize(self, text, max_length=60, min_length=20, length_penalty=2.0, num_beams=4):
        tokens = self.tokenizer(text, truncation=True, padding='longest', return_tensors="pt")
        summary_ids = self.model.generate(tokens['input_ids'], 
                                          max_length=max_length, 
                                          min_length=min_length, 
                                          length_penalty=length_penalty, 
                                          num_beams=num_beams, 
                                          early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

summarizer = ParagraphSummarizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')
    summary = summarizer.summarize(text)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
