### @export "import-the-library"
import pyalm.pyalm as alm

### @export "get-single-doi"
article = alm.get_alm("10.1371/journal.pone.0029797", info="summary")

### @export "print-article"
article

### @export "print-biblio"
article.title
article.url

### @export "print-ids"
article.doi
article.pmid

### @export "print-stats"
article.views
article.citations

### @export "multiple-dois"
articles = alm.get_alm(
               "10.1371/journal.pone.0029797,10.1371/journal.pone.0029798",
               info="summary")
len(articles)
for article in articles:
    print "DOI:", article.doi,
    print "Views:", article.views

### @export "get-event-level-cites"
article = alm.get_alm("10.1371/journal.pone.0029797",
                      info="event", source="crossref")
article.sources['crossref']

### @export "print-cites-metrics"
article.sources['crossref'].metrics.total
article.sources['crossref'].metrics.citations
article.sources['crossref'].metrics.shares

### @export "print-cites-events"
article.sources['crossref'].events[0]







