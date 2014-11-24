import requests
from utils import dictmapper, MappingRule as to
import cleanup
import config

BASE_HEADERS = {'Accept': 'application/json'}

MetricsBase = dictmapper('MetricsBase',
                         {'citations': to(['citations'],
                                          cleanup._parse_numbers_to_int),
                          'comments': to(['comments'],
                                         cleanup._parse_numbers_to_int),
                          'html': to(['html'],
                                       cleanup._parse_numbers_to_int),
                          'likes': to(['likes'],
                                      cleanup._parse_numbers_to_int),
                          'pdf': to(['pdf'],
                                    cleanup._parse_numbers_to_int),
                          'readers': to(['readers'],
                                    cleanup._parse_numbers_to_int),
                          'shares': to(['shares'],
                                       cleanup._parse_numbers_to_int),
                          'total': to(['total'],
                                      cleanup._parse_numbers_to_int)
                         }
)


class Metrics(MetricsBase):
    def __repr__(self):
        return """
<%s total:%s readers:%s pdf:%s html:%s comments:%s likes:%s>
""" % (type(self).__name__, self.total, self.readers, self.pdf, self.html, self.comments, self.likes)


SourceBase = dictmapper('SourceBase',
  {
     'name': ['name'],
     'display_name': ['display_name'],
     'group_name': ['group_name'],
     'events_url': ['events_url'],
     'update_date': to(['update_date'],
                       cleanup._parse_dates_to_datetime),
     'events': ['events'],
     'events_csl': ['events_csl'],
     'metrics': to(['metrics'],
                   lambda l: Metrics(l)
                   if l is not None else None),
     'by_day': to(['by_day'],
                      cleanup._parse_day),
     'by_month': to(['by_month'],
                      cleanup._parse_month),
     'by_year': to(['by_year'],
                      cleanup._parse_year)
   }
)


class Source(SourceBase):
    def __repr__(self):
        return "<%s %s:%s>" % (type(self).__name__, self.display_name, self.metrics.total)


ArticleALMBase = dictmapper('ArticleALMBase',
                            {
                                'doi': ['doi'],
                                'mendeley_uuid': ['mendeley_uuid'],
                                'pmcid': ['pmcid'],
                                'pmid': ['pmid'],
                                'issued': to(['issued'],
                                               cleanup._parse_issued),
                                'update_date': to(['update_date'],
                                                cleanup._parse_dates_to_datetime),
                                'url': ['canonical_url'],
                                'title': ['title'],
                                'cited': to(['cited'],
                                                cleanup._parse_numbers_to_int),
                                'saved': to(['saved'],
                                                cleanup._parse_numbers_to_int),
                                'discussed': to(['discussed'],
                                             cleanup._parse_numbers_to_int),
                                'viewed': to(['viewed'],
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
        return "<%s %s\nDOI %s>" % (type(self).__name__, self.title, self.doi)


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
    :param instance: One of plos, elife, crossref, pkp, pensoft, or copernicus.

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
