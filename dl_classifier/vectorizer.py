import numpy as np
from tqdm import tqdm
from keras.preprocessing.sequence import pad_sequences


class Vectorizer:

    def __init__(self):
        self._max_sentence_len = 100
        self._max_wordform_len = 30

        self._tag2id = {'O': 0, 'B-TIME': 1, 'I-TIME': 2, 'B-DATE': 3, 'I-DATE': 4, 'B-DURATION': 5, 'I-DURATION': 6,
                        'B-SET': 7, 'I-SET': 8}
        self._all_chars = u'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.?!:;"«»-—1234567890'
        self._chars_len = len(self._all_chars) + 1

    def vectorize_chars_and_tokens(self, sentences):
        X_chars = self.vectorize_chars_dataset(sentences)
        X_sentences = self.vectorize_sentences(sentences)
        return X_chars, X_sentences

    def vectorize_targets(self, sentences):
        y = [[self._tag2id[w[1]] for w in s] for s in tqdm(sentences, desc='Vectorizing targets')]
        y = pad_sequences(maxlen=self._max_sentence_len, sequences=y, padding="post", value=self._tag2id["O"])
        y = y.reshape(y.shape[0], y.shape[1], 1)
        print('y_shape: {}'.format(str(y.shape)))
        return y

    def vectorize_chars_dataset(self, sentences):
        X_chars = [[self._vectorize_chars_wordform(w[0]) for w in s] for s in tqdm(sentences, desc='Vectorizing chars')]
        X_chars = pad_sequences(maxlen=self._max_sentence_len, sequences=X_chars, padding="post",
                                value=np.zeros((30, self._chars_len), dtype=np.int32))
        print('X_chars.shape: {}'.format(str(X_chars.shape)))
        return X_chars

    def vectorize_sentences(self, sentences):
        X = [[w[0] for w in s] for s in tqdm(sentences, desc='Vectorizing sentences')]
        new_X = []
        for seq in X:
            new_seq = []
            for i in range(self._max_sentence_len):
                try:
                    new_seq.append(seq[i])
                except:
                    new_seq.append("__PAD__")
            new_X.append(new_seq)
        X = new_X
        print('X_sentence.shape: {}'.format(str(np.array(X).shape)))
        return np.array(X)

    def _vectorize_chars_wordform(self, wordform):

        vector = np.zeros(self._max_wordform_len * (self._chars_len))
        for i in range(len(wordform)):
            if i == self._max_wordform_len:
                break
            if wordform[i] in self._all_chars:
                ind = self._all_chars.index(wordform[i])
                vector[i * self._chars_len + ind] = 1.0
        vector = vector.reshape((self._max_wordform_len, self._chars_len))
        return vector

