#!/usr/bin/env python
# coding: utf-8


from __future__ import division, print_function, unicode_literals

import os
import word2vec
from unittest import TestCase


class TestWord2vec(TestCase):


    def setUp(self):
        print("----setUp----")
        self.input_ = os.path.abspath('data/yangben')
        self.output_phrases = os.path.abspath('data/text-phrases.txt')
        self.output_clusters = os.path.abspath('data/text-clusters.txt')
        self.output_bin = os.path.abspath('data/vectors.bin')
        self.output_txt = os.path.abspath('data/vectors.txt')




    def test_setup_module(self):
        print ("----setup_module----")
        word2vec.word2phrase(self.input_, self.output_phrases, verbose=False)
        word2vec.word2vec(self.input_, self.output_bin, size=10, binary=1, verbose=False)
        word2vec.word2vec(self.input_, self.output_txt, size=10, binary=0, verbose=False)
        word2vec.word2clusters(self.input_, self.output_clusters, 10, verbose=True)


    # def test_files_create(self):
    #     print ("----test_files_create----")
    #     assert os.path.exists(self.output_phrases)
    #     assert os.path.exists(self.output_clusters)
    #     assert os.path.exists(self.output_bin)
    #     assert os.path.exists(self.output_txt)
    #
    #
    # def test_load_bin(self):
    #     print ("----test_load_bin----")
    #     model = word2vec.load(self.output_bin)
    #     vocab = model.vocab
    #     vectors = model.vectors
    #
    #     assert vectors.shape[0] == vocab.shape[0]
    #     assert vectors.shape[0] > 3000
    #     assert vectors.shape[1] == 10
    #
    #
    # def test_load_txt(self):
    #     print ("----test_load_txt----")
    #     model = word2vec.load(self.output_txt)
    #     vocab = model.vocab
    #     vectors = model.vectors
    #
    #     assert vectors.shape[0] == vocab.shape[0]
    #     assert vectors.shape[0] > 3000
    #     assert vectors.shape[1] == 10
    #
    #
    # def test_prediction(self):
    #     print ("----test_prediction----")
    #     model = word2vec.load(self.output_bin)
    #     indexes, metrics = model.cosine('the')
    #     assert indexes.shape == (10,)
    #     assert indexes.shape == metrics.shape
    #
    #     py_response = model.generate_response(indexes, metrics).tolist()
    #     assert len(py_response) == 10
    #     assert len(py_response[0]) == 2
    #
    #
    # def test_analogy(self):
    #     print ("----test_analogy----")
    #     model = word2vec.load(self.output_txt)
    #     indexes, metrics = model.analogy(pos=['the', 'the'], neg=['the'], n=20)
    #     assert indexes.shape == (20,)
    #     assert indexes.shape == metrics.shape
    #
    #     py_response = model.generate_response(indexes, metrics).tolist()
    #     assert len(py_response) == 20
    #     assert len(py_response[0]) == 2
    #
    #
    # def test_clusters(self):
    #     print ("----test_clusters----")
    #     clusters = word2vec.load_clusters(self.output_clusters)
    #     assert clusters.vocab.shape == clusters.clusters.shape
    #     assert clusters.get_words_on_cluster(1).shape[0] > 10  # sanity check
    #     assert clusters.get_words_on_cluster(1).all()
    #
    #
    # def test_model_with_clusters(self):
    #     print ("----test_model_with_clusters----")
    #     clusters = word2vec.load_clusters(self.output_clusters)
    #     model = word2vec.load(self.output_bin)
    #     assert clusters.vocab.shape == model.vocab.shape
    #
    #     model.clusters = clusters
    #     indexes, metrics = model.analogy(pos=['the', 'the'], neg=['the'], n=30)
    #     assert indexes.shape == (30,)
    #     assert indexes.shape == metrics.shape
    #
    #     py_response = model.generate_response(indexes, metrics).tolist()
    #     assert len(py_response) == 30
    #     assert len(py_response[0]) == 3


    def tearDown(self):
        print("----tearDown----")
