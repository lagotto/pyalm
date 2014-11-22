import requests
from utils import dictmapper, MappingRule as to
import cleanup
import config

BASE_HEADERS = {'Accept': 'application/json'}

MetricsBase = dictmapper('MetricsBase',
                         {'citations': MappingRule(['citations'],
                                          cleanup._parse_numbers_to_int),
                          'comments': MappingRule(['comments'],
                                         cleanup._parse_numbers_to_int),
                          'groups': MappingRule(['groups'],
                                       cleanup._parse_numbers_to_int),
                          'likes': MappingRule(['likes'],
                                      cleanup._parse_numbers_to_int),
                          'pdf': MappingRule(['pdf'],
                                    cleanup._parse_numbers_to_int),
                          'shares': MappingRule(['shares'],
                                       cleanup._parse_numbers_to_int),
                          'total': MappingRule(['total'],
                                      cleanup._parse_numbers_to_int)
                         }
)


class Metrics(MetricsBase):
    def __repr__(self):
        return """
<%s total:%s shares:%s citations:%s comments:%s>
""" % (type(self).__name__, self.total, self.shares, self.citations, self.comments)


SourceBase = dictmapper('SourceBase',
                        {'name': ['name'],
                         'display_name': ['display_name'],
                         'events_url': ['events_url'],
                         'update_date': MappingRule(['update_date'],
                                           cleanup._parse_dates_to_datetime),
                         'events': ['events'],
                         'metrics': MappingRule(['metrics'],
                                       lambda l: Metrics(l)
                                       if l is not None else None),
                         'histories': MappingRule(['histories'],
                                         cleanup._process_histories)
                        }
)


class Source(SourceBase):
    def __repr__(self):
        return "<%s %s:%s>" % (type(self).__name__, self.display_name, self.metrics.total)


ArticleALMBase = dictmapper('ArticleALMBase',
                            {
                                'doi': ['doi'],
                                'mendeley_id': ['mendeley'],
                                'pmcid': ['pmcid'],
                                'pmid': ['pmid'],
                                'publication_date': MappingRule(['publication_date'],
                                                       cleanup._parse_dates_to_datetime),
                                'update_date': MappingRule(['update_date'],
                                                  cleanup._parse_dates_to_datetime),
                                'url': ['url'],
                                'title': ['title'],
                                'citations': MappingRule(['citations'],
                                                cleanup._parse_numbers_to_int),
                                'bookmarks': MappingRule(['bookmarks'],
                                                cleanup._parse_numbers_to_int),
                                'shares': MappingRule(['shares'],
                                             cleanup._parse_numbers_to_int),
                                'views': MappingRule(['views'],
                                            cleanup._parse_numbers_to_int)
                            }
)


class ArticleALM(ArticleALMBase):
    _sources = {}
    _resp_json = None

    def _load_sources(self):
        for src in self._resp_json.get('sources', None):
            self._sources[src['name']] = Source(src)

    @property
    def sources(self):
        if self._sources == {}:
            self._load_sources()
        return self._sources

    def __repr__(self):
        return "<%s %s, DOI %s>" % (type(self).__name__, self.title, self.doi)


def get_alm(identifiers,
            id_type=None,
            info=None,
            source=None,
            rows=None,
            page=None,
            instance='plos'):
    """
    Get summary level alms based on an identifier or identifiers

    :param ids: One or more DOIs, PMCIDs, etc.
    :param api_key: An API key, looks for api key first, or pass one in.
    :param id_type: One of doi, pmid, pmcid, or mendeley_uuid
    :param info: One of summary or detail
    :param source: One or more of the many sources.
    :param rows: Number of results to return, use in combination with page.
    :param page: Page to return, use in combination with rows.
    :param instance: One of plos, etc., Only plos works right now.

    Usage:
    >>> import pyalm
    >>> # Get a single article
    >>> article = pyalm.get_alm("10.1371/journal.pone.0029797", info="summary")
    >>> article
    >>> article[0].title
    >>>
    >>> # Multiple articles
    >>> ids = ["10.1371/journal.pone.0029797","10.1371/journal.pone.0029798"]
    >>> articles = pyalm.get_alm(ids, info="summary")
    >>> len(articles)
    >>> for article in articles:
    >>>     print article.title,"DOI:", article.doi,
    >>>     print "Views:", article.views
    """


    if type(identifiers) != str:
        identifiers = ','.join(identifiers)

    parameters = {'ids': identifiers,
                  'api_key': config.APIS.get(instance).get('key'),
                  'type': id_type,
                  'info': info,
                  'source': source,
                  'rows': rows,
                  'page': page
    }

    url = config.APIS.get(instance).get('url')
    if url:
        resp = requests.get(url,
                            params=parameters,
                            headers=BASE_HEADERS)

        resp.raise_for_status()

        articles = []
        for article_json in resp.json()['data']:
            articles.append(_process_json_to_article(article_json))

        return articles

    else:
        raise


def _process_json_to_article(article_json):
    article = ArticleALM(article_json)
    article._sources = {}
    article._resp_json = article_json
    return article
