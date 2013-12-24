### @export "import-the-library"
import pyalm.pyalm as alm

### @export "get-single-doi"
article = alm.get_alm("10.1371/journal.pone.0029797", info="summary")

### @export "print-article"
article

### @export "print-biblio"
print article.title
print article.url

### @export "print-ids"
print article.doi
print article.pmid

### @export "print-stats"
print article.views
print article.citations

### @export "multiple-dois"
articles = alm.get_alm("10.1371/journal.pone.0029797,10.1371/journal.pone.0029798", info="summary")
print "Number of articles retrieved:", len(articles), "\n"
for article in articles:
    print article.title, "DOI:", article.doi, "Views:", article.views

### @export "get-event-level-cites"
article = alm.get_alm("10.1371/journal.pone.0029797", info="event", source="crossref")
print article.sources['crossref']

### @export "print-cites-metrics"
print 'Total cites from Crossref:', article.sources['crossref'].metrics.total
print '..is the same as # cites:', article.sources['crossref'].metrics.citations
print '...and no shares:', article.sources['crossref'].metrics.shares

### @export "print-cites-events"
print 'The first recorded Crossref citation of the article:\n', article.sources['crossref'].events[0]







