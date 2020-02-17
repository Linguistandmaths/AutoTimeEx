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


class TimeModel:

    def __init__(self):
        self._max_len = 100
        self._batch_size = 20

        sess = tf.Session()
        K.set_session(sess)

        print('Loading elmo model...')
        self._elmo_model = hub.Module("http://files.deeppavlov.ai/deeppavlov_data/elmo_ru-news_wmt11-16_1.5M_steps.tar.gz",
        trainable=True)
        print('Elmo model is loaded')
        sess.run(tf.global_variables_initializer())
        sess.run(tf.tables_initializer())

        self._model = self._define_model()

    def get_model(self):
        return self._model

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

    def ElmoEmbedding(self, x):
        return self._elmo_model(inputs={
            "tokens": tf.squeeze(tf.cast(x, tf.string)),
            "sequence_len": tf.constant(self._batch_size * [self._max_len])
        },
            signature="tokens",
            as_dict=True)["elmo"]
