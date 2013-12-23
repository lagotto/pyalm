PyALM Docs
==========

Basic usage
-----------

###Summary Level Information###

After installation (see the README) import the library and call the API give a doi and 
the information level required (summary, event, history, detail). We are starting with 
the API call which just gives summary level information.
{{ d['examples/example.py|idio|pycon|pyg']['import-the-library'] }}
{{ d['examples/example.py|idio|pycon|pyg']['get-single-doi'] }}

The returned object provides some basic information:
{{  d['examples/example.py|idio|pycon|pyg']['print-article'] }}

We can then start getting some summary information about the returned object. With the
summary API call you obtain the basic bibliographic information (`title`, `doi`,
`url`, `publication_date`), the most recent `update_date`, the identifiers for the paper 
(`doi`, `pmid`, `pmcid`) alongside summary metrics information (`views`, `shares`, 
`bookmarks`, `citations`). In each case the relevant information can be obtained as an 
attribute of the response:	

{{  d['examples/example.py|idio|pycon|pyg']['print-biblio'] }}
{{  d['examples/example.py|idio|pycon|pyg']['print-ids'] }}
{{  d['examples/example.py|idio|pycon|pyg']['print-stats'] }}

If a single DOI is given then the returned object will be an ArticleALM object. If 
multiple DOIs are requested then the returned object will be a list.
{{  d['examples/example.py|idio|pycon|pyg']['multiple-dois'] }}

###More Detailed Information###
