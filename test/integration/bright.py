import re
import unittest

from ir_datasets.formats import GenericDoc, GenericQuery, TrecQrel

from .base import DatasetIntegrationTest


class TestBright(DatasetIntegrationTest):
    def test_biology_docs(self):
        self._test_docs('bright/biology', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_biology_queries(self):
        self._test_queries('bright/biology', items={
            0: GenericQuery(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_biology_qrels(self):
        self._test_qrels('bright/biology', items={
            0: TrecQrel(re.compile(r'^.+$'), re.compile(r'^.+$'), 1, '0'),
        })

    def test_biology_long_documents_docs(self):
        self._test_docs('bright/biology/long_documents', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_biology_long_documents_qrels(self):
        self._test_qrels('bright/biology/long_documents', items={
            0: TrecQrel(re.compile(r'^.+$'), re.compile(r'^.+$'), 1, '0'),
        })

    def test_sustainable_living_docs(self):
        self._test_docs('bright/sustainable_living', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_sustainable_living_long_documents_docs(self):
        self._test_docs('bright/sustainable_living/long_documents', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_leetcode_docs(self):
        self._test_docs('bright/leetcode', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_aops_docs(self):
        self._test_docs('bright/aops', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_theoremqa_theorems_docs(self):
        self._test_docs('bright/theoremqa_theorems', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })

    def test_theoremqa_questions_docs(self):
        self._test_docs('bright/theoremqa_questions', items={
            0: GenericDoc(re.compile(r'^.+$'), re.compile(r'^.+$', re.DOTALL)),
        })


if __name__ == '__main__':
    unittest.main()
