import ir_datasets
from ir_datasets.datasets.base import Dataset, YamlDocumentation
from ir_datasets.formats import BaseDocs, BaseQrels, BaseQueries, GenericDoc, GenericQuery, TrecQrel
from ir_datasets.indices import PickleLz4FullStore, DEFAULT_DOCSTORE_OPTIONS

_logger = ir_datasets.log.easy()

NAME = 'bright'

# StackExchange-sourced domains have both passage-level and document-level labels
STACKEXCHANGE_DOMAINS = [
    'biology',
    'earth_science',
    'economics',
    'psychology',
    'robotics',
    'stackoverflow',
    'sustainable_living',
    'pony',
]

ALL_DOMAINS = STACKEXCHANGE_DOMAINS + [
    'leetcode',
    'aops',
    'theoremqa_theorems',
    'theoremqa_questions',
]


def _parquet_iter(path):
    pq = ir_datasets.lazy_libs.pyarrow_parquet()
    batch_size = 64
    with pq.ParquetFile(path) as parquet_file:
        for record_batch in parquet_file.iter_batches(batch_size=batch_size):
            for d in record_batch.to_pylist():
                yield d


class BrightDocs(BaseDocs):
    def __init__(self, name, dlc):
        super().__init__()
        self._name = name
        self._dlc = dlc

    def docs_iter(self):
        return iter(self.docs_store())

    def _docs_iter(self):
        for d in _parquet_iter(self._dlc.path()):
            yield GenericDoc(d['id'], d['content'])

    def docs_cls(self):
        return GenericDoc

    def docs_store(self, field='doc_id', options=DEFAULT_DOCSTORE_OPTIONS):
        return PickleLz4FullStore(
            path=f'{ir_datasets.util.home_path()/NAME/self._name}/docs.pklz4',
            init_iter_fn=self._docs_iter,
            data_cls=self.docs_cls(),
            lookup_field=field,
            index_fields=['doc_id'],
            count_hint=ir_datasets.util.count_hint(f'{NAME}/{self._name}'),
            options=options,
        )

    def docs_count(self):
        if self.docs_store().built():
            return self.docs_store().count()

    def docs_namespace(self):
        return f'{NAME}/{self._name}'

    def docs_lang(self):
        return 'en'


class BrightQueries(BaseQueries):
    def __init__(self, name, dlc):
        super().__init__()
        self._name = name
        self._dlc = dlc

    def queries_iter(self):
        for d in _parquet_iter(self._dlc.path()):
            yield GenericQuery(d['id'], d['query'])

    def queries_cls(self):
        return GenericQuery

    def queries_namespace(self):
        return f'{NAME}/{self._name}'

    def queries_lang(self):
        return 'en'


class BrightQrels(BaseQrels):
    def __init__(self, dlc, gold_ids_key='gold_ids'):
        self._dlc = dlc
        self._gold_ids_key = gold_ids_key

    def qrels_iter(self):
        for d in _parquet_iter(self._dlc.path()):
            qid = d['id']
            for doc_id in d[self._gold_ids_key]:
                yield TrecQrel(qid, doc_id, 1, '0')

    def qrels_cls(self):
        return TrecQrel

    def qrels_defs(self):
        return {1: 'relevant'}


def _init():
    base_path = ir_datasets.util.home_path() / NAME
    dlc = ir_datasets.util.DownloadConfig.context(NAME, base_path)
    documentation = YamlDocumentation(f'docs/{NAME}.yaml')

    base = Dataset(documentation('_'))
    subsets = {}

    for domain in ALL_DOMAINS:
        docs = BrightDocs(domain, dlc[f'{domain}/documents'])
        queries = BrightQueries(domain, dlc[f'{domain}/examples'])
        qrels = BrightQrels(dlc[f'{domain}/examples'], gold_ids_key='gold_ids')
        subsets[domain] = Dataset(docs, queries, qrels, documentation(domain))

        if domain in STACKEXCHANGE_DOMAINS:
            long_docs = BrightDocs(f'{domain}/long_documents', dlc[f'{domain}/long_documents'])
            long_qrels = BrightQrels(dlc[f'{domain}/examples'], gold_ids_key='gold_ids_long')
            subsets[f'{domain}/long_documents'] = Dataset(
                long_docs,
                queries,
                long_qrels,
                documentation(f'{domain}/long_documents'),
            )

    ir_datasets.registry.register(NAME, base)
    for s in sorted(subsets):
        ir_datasets.registry.register(f'{NAME}/{s}', subsets[s])

    return base, subsets


base, subsets = _init()
