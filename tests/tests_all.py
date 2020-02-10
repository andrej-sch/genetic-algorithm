"""
Module and unit tests.
"""



import unittest
import numpy as np
from genetic_algorithm.algorithm import algorithm
from genetic_algorithm.benchmark import _decode
from genetic_algorithm.utils import chromosome_length

class TestDecoding(unittest.TestCase):
    '''Tests decoding function in benchmark module.'''

    def setUp(self):

        self.params = {}
        self.params['searchDomain']['lowerBound'] = -2
        self.params['searchDomain']['upperBound'] = 2
        self.params['searchDomain']['precision'] = 0.01

        # self.params = {
        #     'lower_bound': -2,
        #     'upper_bound': 2,
        #     'precision': 0.01
        # }


        self.dim_num = 1
        self.length = chromosome_length()

        self.chrom_zeros = np.zeros(size=(1, self.length))
        self.chrom_ones = np.ones(size=(1, self.length))
        
        #self.chroms = np.vstack(chrom1, chrom2)

    def test_left_bound(self):
        '''Tests lower bound value.'''

        real_value = _decode(self.chrom_zeros, self.dim_num, self.length, self.params)()
        self.assertAlmostEqual(real_value, self.params['lower_bound'])

    def test_right_bound(self):
        '''Tests upper bound value.'''

        real_value = _decode(self.chrom_ones, self.dim_num, self.length, self.params)()
        self.assertAlmostEqual(real_value, self.params['upper_bound'])




from os import path
import sys
sys.path.append(path.join(path.realpath(path.dirname(__file__)), '../..'))
sys.path.append(path.join(path.realpath(path.dirname(__file__)), '../../metrics'))
#print(sys.path)

import argparse


# to test as identical docs as well as against a precomp score
HYP_TEXT = "../../metrics/_sample_data/as_text_hyp.json"
REF_TEXT = "../../metrics/_sample_data/as_text_ref.json"

# to test as identical docs
REF_SENT = "../../metrics/_sample_data/sentences_ref.json"

# to test as no macth docs
HYP_NOMATCH = "../../metrics/_sample_data/nomatch_hyp.json"
REF_NOMATCH = "../../metrics/_sample_data/nomatch_ref.json"

class TestWer(unittest.TestCase):
    """Tests WER metric."""

    def setUp(self):
        """Sets class variables used in test functions."""

        self.metric = mt.Metric.WER
        self.scorer = mt.Scorer([self.metric], "")

    def test_text_score_zero(self):
        """Test that WER yields zero against identicals documents as texts."""

        hyps, refs = get_input(REF_TEXT, REF_TEXT)
        scores = self.scorer.compute_scores(hyps, refs)
        self.assertEqual(scores[self.metric], 0.)


    def test_sent_score_zero(self):
        """Test that WER yields zero against identicals documents as sentences."""

        hyps, refs = get_input(REF_SENT, REF_SENT)
        scores = self.scorer.compute_scores(hyps, refs)
        self.assertEqual(scores[self.metric], 0.)

    def test_text_score_precomp(self):
        """Test a WER's outcome against a precomputed score."""

        hyps, refs = get_input(HYP_TEXT, REF_TEXT)
        scores = self.scorer.compute_scores(hyps, refs)
        self.assertAlmostEqual(scores[self.metric], 0.11707317073170732)

class TestMeteor(unittest.TestCase):
    """Tests METEOR metric."""

    def setUp(self):
        """Sets class variables used in test functions."""

        self.metric = mt.Metric.METEOR
        self.scorer = mt.Scorer([self.metric], mt.METEOR_JAR)

    def test_score_zero(self):
        """
        Tests that METEOR yields zero against non matching documents."""

        hyps, refs = get_input(HYP_NOMATCH, REF_NOMATCH)
        score = self.scorer.compute_scores(hyps, refs)
        self.assertEqual(score[self.metric], 0.)


    def test_text_score_one(self):
        """
        Tests that METEOR yields one against identical documents as texts."""

        hyps, refs = get_input(REF_TEXT, REF_TEXT)
        score = self.scorer.compute_scores(hyps, refs)
        self.assertEqual(score[self.metric], 1.)

    def test_sent_score_one(self):
        """
        Tests that METEOR yields one against identical documents as sentences."""

        hyps, refs = get_input(REF_SENT, REF_SENT)
        score = self.scorer.compute_scores(hyps, refs)
        self.assertAlmostEqual(score[self.metric], 1.)

class TestCider(unittest.TestCase):
    """Tests CIDEr metric."""

    def setUp(self):
        """Sets class variables used in test functions."""

        self.metric = mt.Metric.CIDER
        self.scorer = mt.Scorer([self.metric], "")

    def test_score_zero(self):
        """
        Tests that CIDEr yields zero against non matching documents."""

        hyps, refs = get_input(HYP_NOMATCH, REF_NOMATCH)
        scores = self.scorer.compute_scores(hyps, refs)
        self.assertEqual(scores[self.metric], 0.)

    # def test_text_score_ten(self):
    #     """Tests that CIDEr yields ten against identical documents as texts."""

    #     hyps, refs = get_input(REF_TEXT, REF_TEXT)
    #     scores = scorer.compute_scores(hyps, refs)
    #     self.assertEqual(scores[0], 10.) # returns 0.0


    def test_sent_score_ten(self):
        """
        Tests that CIDEr yields ten against identical documents as sentences."""

        hyps, refs = get_input(REF_SENT, REF_SENT)
        scores = self.scorer.compute_scores(hyps, refs)
        self.assertEqual(scores[self.metric], 10.)

class SanityCheck(unittest.TestCase):
    """
    Tests metrics.py module.
    """

    def test_set_metrics(self):
        """
        Tests that a function 'set_metrics()' updates
        the class' attribute 'metrics' interactively.
        """

        hyps, refs = get_input(REF_SENT, REF_SENT)

        # set up the scorer
        metrics = [mt.Metric.WER]
        scorer = mt.Scorer(metrics, mt.METEOR_JAR)
        scores = scorer.compute_scores(hyps, refs)
        self.assertEqual(len(scores), 1)

        # add another metrics
        metrics.append(mt.Metric.METEOR)
        scorer.set_metrics(metrics)
        scores = scorer.compute_scores(hyps, refs)
        self.assertEqual(len(scores), 2)

        # add another metrics
        metrics.append(mt.Metric.CIDER)
        scorer.set_metrics(metrics)
        scores = scorer.compute_scores(hyps, refs)
        self.assertEqual(len(scores), 3)

    def test_get_scorer_wer(self):
        """
        Tests that a function _get_scorer() retuns a Wer() object
        when enum Metric.WER is passed.
        """

        scorer = mt.Scorer([mt.Metric.WER], "")
        scorer = scorer._get_scorer(mt.Metric.WER)
        self.assertIsInstance(scorer, mt.Wer)

    def test_get_scorer_meteor(self):
        """
        Tests that a function _get_scorer() retuns a Meteor() object
        when enum Metric.METEOR is passed.
        """

        scorer = mt.Scorer([mt.Metric.METEOR], "")
        scorer = scorer._get_scorer(mt.Metric.METEOR)
        self.assertIsInstance(scorer, mt.Meteor)

    def test_get_scorer_cider(self):
        """
        Tests that a function _get_scorer() retuns a Cider() object
        when enum Metric.CIDER is passed.
        """

        scorer = mt.Scorer([mt.Metric.CIDER], "")
        scorer = scorer._get_scorer(mt.Metric.CIDER)
        self.assertIsInstance(scorer, mt.Cider)

#--------------------------------------------------------------

def get_input(hypotheses: str, references: str):
    """
    Reads and preprcocess hyp and ref documents.

    Args:
        hypotheses(str): path to hypotheses json file
        references(str): path to references json file

    Returns:
        tuple(list, list): preprocced hyps and refs
    """

    params = {
        'lower_bound': -2,
        'upper_bound': 2,
        'precision': 0.01
    }

    length = None # !!!!!
    crom1 = np.ones(size=(1, length))
    chom2 = np.zeros(size=(1, lenth))
    chroms = np.vstack(chom1, chrom2)





    # read json files
    hyps = mt.read_json(hypotheses)
    refs = mt.read_json(references)

    # convert dictionary format to list format
    hyps = mt.dic_to_list(hyps)
    refs = mt.dic_to_list(refs)

    # tokenize
    hyps = mt.tokenize(hyps, mt.TOKENIZER_JAR)
    refs = mt.tokenize(refs, mt.TOKENIZER_JAR)

    # flatten hypotheses
    hyps = [hyp for sublist in hyps for hyp in sublist]

    return hyps, refs

if __name__ == '__main__':
    unittest.main()
