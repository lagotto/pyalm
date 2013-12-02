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
articles = alm.get_alm("10.1371/journal.pone.0029797,10.1371/journal.pone.0029797", info="summary")
for article in articles:
    print article.title, "DOI:", article.doi, "Views:", article.views






