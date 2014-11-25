# Higher level interface for interacting with specific classes of events
import pyalm as alm
import cleanup
from utils import dictmapper, MappingRule as to

ContributorBase = dictmapper('ContributorBase',
                              {
                               'contributor_role' : ['contributor_role'],
                               'first_author': to(['first_author'],
                                                    cleanup._text_to_bool),
                               'given_name': ['given_name'],
                               'sequence': ['sequence'],
                               'surname': ['surname']
                              }
                            )

class Contributor(ContributorBase):
    def __repr__(self):
        return '<%s: %s%s>' % (type(self).__name__, self.given_name, self.surname)


CrossrefBase = dictmapper('CrossrefBase',
                            {
                             'article_title' : ['event','article_title'],
                             'doi' : ['event','doi'],
                             'fl_count' : to(['event','fl_count'],
                                        cleanup._parse_numbers_to_int),
                             'issn' : ['event','issn'],
                             'journal_abbreviation' : ['event','journal_abbreviation'],
                             'journal_title' : ['event','journal_title'],
                             'publication_type' : ['event','publication_type'],
                             'publication_year' : to(['event','year'],
                                        cleanup._parse_numbers_to_int),
                             'first_page' : to(['event', 'first_page'],
                                        cleanup._parse_numbers_to_int),
                             'issue' : to(['event', 'issue'],
                                        cleanup._parse_numbers_to_int),
                             'volume' : to(['event', 'volume'],
                                        cleanup._parse_numbers_to_int),
                             'contributors' : to(['event','contributors', 'contributor'],
                                                lambda l: map(Contributor, l)
                                                if l is not None else None)
                            }
                          )


class CrossRef(CrossrefBase):
    def __repr__(self):
        return '<%s %s:%s>' % (type(self).__name__, self.article_title, self.doi)

TweetBase = dictmapper('TweetBase',
                    {
                     'created_at' : to(['event', 'created_at'],
                           cleanup._parse_dates_to_datetime),
                     'id' : ['event', 'id'],
                     'user' : ['event', 'user'],
                     'user_name' : ['event', 'user_name'],
                     'user_profile_image' : ['event', 'user_profile_image'],
                     'text' : ['event', 'text'],
                     'url' : ['event_url'],
                     'time' : ['event_time'],
                     'event_csl' : ['event_csl']
                     }
                   )

class Tweet(TweetBase):
    def __repr__(self):
        return '<%s %s:%s>' % (type(self).__name__, self.user, self.text)

WikiBase = dictmapper('WikiBase',
                        {
                            'ca': ['ca'],
                            'commons': ['commons'],
                            'cs': ['cs'],
                            'de': ['de'],
                            'en': ['en'],
                            'es': ['es'],
                            'fi': ['fi'],
                            'fr': ['fr'],
                            'hu': ['hu'],
                            'it': ['it'],
                            'ja': ['ja'],
                            'ko': ['ko'],
                            'nl': ['nl'],
                            'no': ['no'],
                            'pl': ['pl'],
                            'pt': ['pt'],
                            'ru': ['ru'],
                            'sv': ['sv'],
                            'total': ['total'],
                            'uk': ['uk'],
                            'vi': ['vi'],
                            'zh': ['zh']})

class WikiRef(WikiBase):
    def __repr__(self):
        return '<%s Citations:%s>' % (type(self).__name__, self.total)

# MendeleyBase = dictmapper('MendeleyBase',
#                             {
#                                 'readers' : ['events', 'readers'],
#                                 'discipline' : ['events', 'discipline'],
#                                 'country' : ['events', 'country'],
#                                 'status' : ['events', 'status'],
#                                 'events_csl' : ['events_csl']
#                             }
#                           )

# class Mendeley(MendeleyBase):
#     def __repr__(self):
#         return '<%s Readers:%s>' % (type(self).__name__, self.readers)

def mendeley_events(object):
    out = object.events
    out['url'] = object.events_url
    out['events_csl'] = object.events_csl
    out['events_url'] = object.events_url
    return out

FacebookBase = dictmapper('FacebookBase',
                            {
                                'url' : ['url'],
                                'share_count' : ['share_count'],
                                'like_count' : ['like_count'],
                                'comment_count' : ['comment_count'],
                                'click_count' : ['click_count'],
                                'total_count' : ['total_count']
                            }
                          )

class Facebook(FacebookBase):
    def __repr__(self):
        return '<%s Total:%s>' % (type(self).__name__, self.total_count)

NatureBase = dictmapper('NatureBase',
                    {
                     'blog' : ['event', 'blog'],
                     'links_to_doi' : ['event', 'links_to_doi'],
                     'percent_complex_words' : ['event', 'percent_complex_words'],
                    'popularity' : ['event', 'popularity'],
                    'created_at' : ['event', 'created_at'],
                    'title' : ['event', 'title'],
                    'body' : ['event', 'body'],
                    'updated_at' : ['event', 'updated_at'],
                    'flesch' : ['event', 'flesch'],
                    'url' : ['event', 'url'],
                    'blog_id' : ['event', 'blog_id'],
                    'id' : ['event', 'id'],
                    'hashed_id' : ['event', 'hashed_id'],
                    'num_words' : ['event', 'num_words'],
                    'published_at' : ['event', 'published_at'],
                    'fog' : ['event', 'fog'],
                    'event_time' : ['event_time'],
                    'event_url' : ['event_url'],
                    'event_csl' : ['event_csl']
                     }
                   )

class Nature(NatureBase):
    def __repr__(self):
        return '<%s :%s>' % (type(self).__name__, self.title)
