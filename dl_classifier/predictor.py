import numpy as np
from nltk.tokenize import WordPunctTokenizer

from dl_classifier.vectorizer import Vectorizer
from dl_classifier.model import TimeModel


class Predictor:

    def __init__(self):
        self._vectorizer = Vectorizer()
        self._tokenizer = WordPunctTokenizer()
        time_model = TimeModel()
        self._model = time_model.get_model()
        self._model.load_weights('/Users/bruches/PycharmProjects/AutoTimeEx/dl_classifier/weights/weights_chars_elmo_crf.h5')
        self._tag2id = {'O': 0, 'B-TIME': 1, 'I-TIME': 2, 'B-DATE': 3, 'I-DATE': 4, 'B-DURATION': 5, 'I-DURATION': 6,
                        'B-SET': 7, 'I-SET': 8}
        self._id2tag = self._get_id2tag()

    def _get_id2tag(self):
        id2tag = dict()
        for tag, id in self._tag2id.items():
            id2tag[id] = tag
        return id2tag

    def _process_input_sentence(self, sentence):
        tokens = self._tokenizer.tokenize(sentence)
        tokens_to_process = [(token, 'O') for token in tokens]
        input_tokens = []
        for i in range(20):
            input_tokens.append(tokens_to_process)
        X_chars, X_sequence = self._vectorizer.vectorize_chars_and_tokens(sentences=input_tokens)
        return X_chars, X_sequence, tokens

    def predict(self, text):
        X_chars, X_sequence, tokens = self._process_input_sentence(text)
        predicts = self._model.predict([X_chars, X_sequence])[0]
        result = []
        for i, token in enumerate(tokens):
            tag = self._id2tag[np.argmax(predicts[i])]
            result.append((token, tag))
        return result

if __name__ == '__main__':
    predictor = Predictor()
    text = 'The season about a month earlier than usual, sparking concerns it might turn into the worst in a decade.'
    result = predictor.predict(text)
    for r in result:
        print(r)
