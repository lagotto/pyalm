PyALM Docs
==========

Contents
--------
1. Basic usage
	1. Summary level information
	2. More detailed information
2. Working with histories
3. Working with events

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

To obtain more detailed information on each ALM source from the ALM API a request should 
be made for from detailed information. The options available are `event` which provides 
information on the specific events contributing to an ALM count. For instance, this will 
provide information on the individual tweets contributing to the overall count. The
`history` option provides information on the ALM over a series of timepoints. These
timepoints are those when the ALM App polled the data source rather than the date or time
of specific events. Finally the `detail` level provides both event and history data.

For each level of detail a specific set of sources can be specified from one to a list,
to all (by omitting the `source` option). Specific sources are then available via the 
`sources` attribute of the returned object.

{{  d['examples/example.py|idio|pycon|pyg']['get-event-level-cites'] }}

Quantitative information is available for the requested sources whether the info level
is set to `event`, `history`, or `detail`. Metrics are also divided into the same
categories provided by summary level info (`views`, `shares`, 
`bookmarks`, `citations`)

{{  d['examples/example.py|idio|pycon|pyg']['print-cites-metrics'] }}

The event information is available via the `events` attribute on the source. Event data 
is not currently parsed from the JSON object and needs to be handled by the user on a 
source by source basis.

{{  d['examples/example.py|idio|pycon|pyg']['print-cites-events'] }}