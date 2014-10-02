# pyalm

'''
pyalm library
~~~~~~~~~~~~~~~~~~~~~

pyalm is a Python client for the PLOS ALM API. Example usage:

   >>> import pyalm
   >>> pyalm.get_alm("10.1371/journal.pone.0029797", info="summary")

   <ArticleALM Ecological Guild Evolution and the Discovery of the World's Smallest Vertebrate, DOI 10.1371/journal.pone.0029797>
'''

from .cleanup import *
from .config import *
from .events import *
from .pyalm import get_alm
from .utils import *
