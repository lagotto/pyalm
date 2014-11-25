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
        return "<%s %s, DOI %s>" % (type(self).__name__, self.title, self.doi)


def get_alm(identifiers=None,
            id_type=None,
            info=None,
            source=None,
            publisher=None,
            order=None,
            per_page=None,
            page=None,
            instance='plos',
            **kwargs):
    """
    Get summary level alms based on an identifier or identifiers

    :param ids: One or more DOIs, PMCIDs, etc.
    :param api_key: An API key, looks for api key first, or pass one in.
    :param id_type: One of doi, pmid, pmcid, or mendeley_uuid
    :param info: One of summary or detail
    :param source: One source. To get many sources, make many calls.
    :param publisher: Filter articles to a given publisher, using a crossref_id.
    :para order: Results are sorted by descending event count when given the source
      name, e.g. &order=wikipedia. Otherwise (the default) results are sorted by
      date descending. When using &source=x, we can only sort by data or that source,
      not a different source.
    :param per_page: Number of results to return, use in combination with page.
    :param page: Page to return, use in combination with per_page.
    :param instance: One of plos, elife, crossref, pkp, pensoft, or copernicus.
    :param **kwargs: Additional named arguments passed on to requests.get

    Usage:
    >>> import pyalm
    >>>
    >>> # Get a single article
    >>> article = pyalm.get_alm("10.1371/journal.pone.0029797", info="summary")
    >>> article
    >>> article[0].title
    >>>
    >>> # Get summary or detailed data
    >>> ## summary
    >>> pyalm.get_alm("10.1371/journal.pone.0029797", info="summary")[0]._resp_json
    >>> ## detail
    >>> pyalm.get_alm("10.1371/journal.pone.0029797", info="detail")[0]._resp_json
    >>>
    >>> # Multiple articles
    >>> ids = ["10.1371/journal.pone.0029797","10.1371/journal.pone.0029798"]
    >>> articles = pyalm.get_alm(ids, info="summary")
    >>> len(articles)
    >>> for article in articles:
    >>>     print article.title,"DOI:", article.doi,
    >>>     print "Views:", article.views
    >>>
    >>> # Search by source
    >>> articles = pyalm.get_alm(source="mendeley", info="summary")
    >>>
    >>> # Search by publisher
    >>> ## first, get some publisher ids via the CrossRef API
    >>> import requests
    >>> ids = requests.get("http://api.crossref.org/members")
    >>> id = [x['id'] for x in ids.json()['message']['items']][0]
    >>> pyalm.get_alm(publisher=id, info="summary")
    >>>
    >>> # Order results
    >>> ## order by a source, orders by descending event count in that source
    >>> articles = pyalm.get_alm(order="mendeley", per_page=10)
    >>> [x.sources['mendeley'].metrics.total for x in articles]
    >>>
    >>> ## not specifying an order, results sorted by date descending
    >>> articles = pyalm.get_alm(info="summary")
    >>> [ x.update_date for x in articles ]
    >>>
    >>> # Paging
    >>> pyalm.get_alm(source="mendeley", info="summary", per_page=1)
    >>> pyalm.get_alm(source="mendeley", info="summary", per_page=2)
    >>> pyalm.get_alm(source="mendeley", info="summary", per_page=2, page=10)
    >>>
    >>> # Search against other Lagotto instances
    >>> pyalm.get_alm(instance="crossref", per_page=5)
    >>> pyalm.get_alm(instance="pkp", per_page=5)
    >>> pyalm.get_alm(instance="elife", per_page=5)
    >>> pyalm.get_alm(instance="pensoft")
    >>>
    >>> # You can pass on additional options to requests.get
    >>> pyalm.get_alm("10.1371/journal.pone.0029797", info="summary", timeout=0.001)
    >>>
    >>> # Parse events data
    >>> from pyalm import events
    >>> article = pyalm.get_alm("10.1371/journal.pone.0029797", info="detail")
    >>>
    >>> ## twitter
    >>> [events.Tweet(x) for x in article[0].sources['twitter'].events]
    >>> ## wikipedia
    >>> dat = events.WikiRef(article[0].sources['wikipedia'].events)
    >>> dat.en
    >>> dat.fr
    >>> ## Mendeley
    >>> events.mendeley_events(article[0].sources['mendeley'])
    >>> ## Facebook
    >>> out = events.Facebook(article[0].sources['facebook'].events[0])
    >>> out.click_count
    >>> articles = pyalm.get_alm(info="detail", source="facebook", per_page=10)
    >>> [events.Facebook(x.sources['facebook'].events[0]) for x in articles]
    >>> ## CrossRef
    >>> [events.CrossRef(x) for x in article[0].sources['crossref'].events]
    >>> ## Nature
    >>> [events.Nature(x) for x in article[0].sources['nature'].events]
    """


    if type(identifiers) != str and identifiers != None:
        identifiers = ','.join(identifiers)

    parameters = {'ids': identifiers,
                  'type': id_type,
                  'info': info,
                  'source': source,
                  'publisher': publisher,
                  'order': order,
                  'per_page': per_page,
                  'page': page,
                  'api_key': config.APIS.get(instance).get('key'),
    }

    url = config.APIS.get(instance).get('url')
    if url:
        resp = requests.get(url,
                            params=parameters,
                            headers=BASE_HEADERS, **kwargs)

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
