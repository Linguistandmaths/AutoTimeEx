

import tensorflow as tf
import tensorflow_hub as hub
from keras import backend as K
from keras.models import Model, Input
from keras.layers.merge import add, concatenate
from keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, Lambda
import numpy as np
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras_contrib.layers import CRF

from dl_classifier.dataset_loader import DatasetLoader
from dl_classifier.vectorizer import Vectorizer

print(tf.__version__)


class Trainer:

    def __init__(self):
        data_dir = '/Users/bruches/Documents/Students/Mezenceva_Zavarzina/csv_dataset/train'
        self._data_loader = DatasetLoader(data_dir)
        self._vectorizer = Vectorizer()

        self._sentences = self._data_loader.load_dataset()[:5600]
        self._X_chars, self._X_sentences = self._vectorizer.vectorize_chars_and_tokens(self._sentences)
        self._y = self._vectorizer.vectorize_targets(self._sentences)

        self._batch_size = 20
        self._max_len = 100

        sess = tf.Session()
        K.set_session(sess)

        print('Loading elmo model...')
        self._elmo_model = hub.Module("http://files.deeppavlov.ai/deeppavlov_data/elmo_ru-news_wmt11-16_1.5M_steps.tar.gz",
        trainable=True)
        print('Elmo model is loaded')
        sess.run(tf.global_variables_initializer())
        sess.run(tf.tables_initializer())

        self._model = self._define_model()

    def ElmoEmbedding(self, x):
        return self._elmo_model(inputs={
            "tokens": tf.squeeze(tf.cast(x, tf.string)),
            "sequence_len": tf.constant(self._batch_size * [self._max_len])
        },
            signature="tokens",
            as_dict=True)["elmo"]

    def _define_model(self):
        input_chars = Input(shape=(self._max_len, 30, 74))
        chars = TimeDistributed(Bidirectional(LSTM(units=25,
                                                   recurrent_dropout=0.5)))(input_chars)

        input_text = Input(shape=(self._max_len,), dtype="string")
        embedding = Lambda(self.ElmoEmbedding, output_shape=(self._max_len, 1024))(input_text)
        x = Bidirectional(LSTM(units=512, return_sequences=True,
                               recurrent_dropout=0.2, dropout=0.2))(embedding)
        x_rnn = Bidirectional(LSTM(units=512, return_sequences=True,
                                   recurrent_dropout=0.2, dropout=0.2))(x)

        x = concatenate([x_rnn, chars])  # residual connection to the first biLSTM
        crf = CRF(9, sparse_target=True)  # CRF layer
        out = crf(x)  # output

        model = Model([input_chars, input_text], out)
        model.summary()

        model.compile(optimizer="adam", loss=crf.loss_function, metrics=[crf.accuracy])
        return model

    def get_model(self):
        return self._model

    def train(self):
        modelPath = "/Users/bruches/PycharmProjects/aspi/term_extraction/dl_model/weights/weights_chars_elmo_crf.h5"
        # model.load_weights(modelPath)
        saver = ModelCheckpoint(modelPath, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
        stopper = EarlyStopping(monitor='val_loss', patience=3, verbose=1, mode='auto')
        history = self._model.fit([self._X_chars, self._X_sentences], np.array(self._y), batch_size=self._batch_size, epochs=50,
                            validation_split=0.2,
                            verbose=1, callbacks=[saver, stopper])
        return history


if __name__ == '__main__':
    trainer = Trainer()
    trainer.train()
