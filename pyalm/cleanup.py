import email.utils
import datetime

def _text_to_bool(response):
    if (type(response) == str) or (type(response) == unicode):
        return response == 'true'

    else:
        return response

def _parse_dates_to_datetime(response):
    if (type(response) == str) or (type(response) == unicode):
        try:
            return datetime.datetime.strptime(response, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            tup = email.utils.parsedate_tz(response)[0:6]
            return datetime.datetime(*tup)

    else:
        return response

def _parse_issued(issued):
    return datetime.datetime.strptime('-'.join([str(x) for x in issued['date-parts'][0]]), '%Y-%m-%d')

def _parse_numbers_to_int(response):
    if (type(response) == str) or (type(response) == unicode):
        return int(response)
    else:
        return response

def _process_histories(history):
    timepoints= []
    for timepoint in history:
        timepoints.append([_parse_dates_to_datetime(timepoint.get('update_date')),
                           _parse_numbers_to_int(timepoint.get('total'))])

    timepoints.sort(key=lambda l: l[0])
    return timepoints

def _parse_by_date(datedict):
    for d in datedict:
        date = '-'.join({ str(d[key]) for key in ['day','month','year'] })
        date = datetime.datetime.strptime(date, '%m-%d-%Y')
        d['date'] = date
    return datedict
