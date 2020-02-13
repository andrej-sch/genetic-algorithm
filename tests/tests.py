"""
Unit tests.
"""

import unittest
import numpy as np
from genetic_algorithm.benchmark import _decode
from genetic_algorithm.utils import chromosome_length

class TestDecoding(unittest.TestCase):
    '''Tests decoding function in benchmark module.'''

    def setUp(self):

        self.params = {}
        self.params['searchDomain'] = {}
        self.params['searchDomain']['lowerBound'] = -2
        self.params['searchDomain']['upperBound'] = 2
        self.params['searchDomain']['precision'] = 0.01

        self.dim_num = 1
        self.length = chromosome_length(self.params)

        self.chrom_zeros = np.zeros(shape=(1, self.length))
        self.chrom_ones = np.ones(shape=(1, self.length))

        self.chroms = np.vstack((self.chrom_zeros, self.chrom_ones))

    def test_left_bound(self):
        '''Tests lower bound value.'''

        real_value = _decode(self.chrom_zeros, self.dim_num, self.length, self.params)()
        self.assertAlmostEqual(real_value, self.params['searchDomain']['lowerBound'])

    def test_right_bound(self):
        '''Tests upper bound value.'''

        real_value = _decode(self.chrom_ones, self.dim_num, self.length, self.params)()
        self.assertAlmostEqual(real_value, self.params['searchDomain']['upperBound'])

    def test_size(self):
        '''Test that two chomosomes return two values'''

        real_nums = _decode(self.chroms, self.dim_num, self.length, self.params)()
        self.assertEqual(real_nums.size, 2)

if __name__ == '__main__':
    unittest.main()
