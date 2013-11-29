import requests
from utils import dictmapper, MappingRule as to
import datetime
import pprint
import config

BASE_HEADERS = {'Accept':'application/json'}

def _parse_numbers_to_int(response):
    if (type(response) == str) or (type(response) == unicode):
        return int(response)
    else:
        return response

def _parse_dates_to_datetime(response):
    if (type(response) == str) or (type(response) == unicode):
        return datetime.datetime.strptime(response, '%Y-%m-%dT%H:%M:%SZ')
    else:
        return response

def _process_histories(history):
    timepoints= []
    for timepoint in history:
        timepoints.append([_parse_dates_to_datetime(timepoint.get('update_date')),
                           _parse_numbers_to_int(timepoint.get('total'))])

    timepoints.sort(key=lambda l: l[0])
                    #if (len(timepoints) != len(counts)) or (len(timepoints) == 0):
                    # return None
    return timepoints#, counts


MetricsBase = dictmapper('MetricsBase',
                             {'citations' :to( ['citations'], _parse_numbers_to_int),
                              'comments' : to(['comments'], _parse_numbers_to_int) ,
                              'groups' : to(['groups'], _parse_numbers_to_int),
                              'likes' :to( ['likes'], _parse_numbers_to_int),
                              'pdf' : to(['pdf'], _parse_numbers_to_int),
                              'shares' : to(['shares'], _parse_numbers_to_int),
                              'total' : to(['total'], _parse_numbers_to_int)
                              }
                        )

class Metrics (MetricsBase):
    def __repr__(self):
        return """
<%s total:%s shares:%s citations:%s comments:%s>
""" % (type(self).__name__, self.total, self.shares, self.citations, self.comments)

SourceBase = dictmapper('SourceBase',
                            {'name' : ['name'],
                             'display_name' : ['display_name'],
                             'events_url' : ['events_url'],
                             'update_date' : ['update_date'],
                             'events' : ['events'],
                             'metrics' : to(['metrics'],
                                            lambda l: Metrics(l)
                                               if l is not None else None),
                             'histories' : to(['histories'],
                                                 _process_histories)
                            }
                        )

class Source(SourceBase):
    def __repr__(self):
        return "<%s %s:%s>" % (type(self).__name__, self.display_name, self.metrics.total)


ArticleALMBase = dictmapper('ArticleALMBase',
                                {
                                'doi'   : ['doi'],
                                'mendeley_id' : ['mendeley'],
                                'pmcid' : ['pmcid'],
                                'pmid' : ['pmid'],
                                'publication_date' : to(['publication_date'],
                                                          _parse_dates_to_datetime),
                                'update_date' : to(['update_date'],
                                                      _parse_dates_to_datetime),
                                'url' : ['url'],
                                'title' : ['title'],
                                'citations' : to(['citations'], _parse_numbers_to_int),
                                'bookmarks' : to(['bookmarks'], _parse_numbers_to_int),
                                'shares' : to(['shares'], _parse_numbers_to_int),
                                'views' : to(['views'], _parse_numbers_to_int)
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
            type = None,
            info = None,
            source = None,
            days = None,
            months = None,
            years = None,
            instance = 'plos'):
    """
    Get summary level alms based on an identifier or identifiers
    """

    parameters = {'ids' : identifiers,
                  'api_key' : config.APIS.get(instance).get('key'),
                  'type' : type,
                  'info' : info,
                  'source' : source,
                  'days' : days,
                  'months' : months,
                  'years' : years
                  }

    url  = config.APIS.get(instance).get('url')
    if url:
        resp = requests.get(url,
                        params = parameters,
                        headers = BASE_HEADERS)

        if resp.status_code != 200:
            print "\nStatus Code:", resp.status_code

        if len(resp.json()) == 1:
            return _process_json_to_article(resp.json()[0])
        elif len(resp.json()) > 1:
            articles = []
            for article_json in resp.json():
                articles.append(_process_json_to_article(article_json))

            return articles

    else:
        raise

def _process_json_to_article(article_json):
    article = ArticleALM(article_json)
    article._sources = {}
    article._resp_json = article_json
    return article


