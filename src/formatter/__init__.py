#!/usr/bin/env python

"""
Formatters for RED output.
"""

__author__ = "Mark Nottingham <mnot@mnot.net>"
__copyright__ = """\
Copyright (c) 2008-2010 Mark Nottingham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from collections import defaultdict

__all__ = ['html', 'text']

default_formatter = "html"
_formatters = defaultdict(list)

def find_formatter(name, multiple=False):
    if name not in _formatters.keys():
        name = default_formatter
    # find single-preferred formatters fist
    if not multiple:
        for candidate in _formatters[name]:
            if not candidate.can_multiple:
                return candidate
    for candidate in _formatters[name]:            
        if candidate.can_multiple:
            return candidate
    raise RuntimeError, "Can't find a format"

def available_formatters():
    return _formatters.keys()

class FormatterType(type):
    """
    Type for Formatters that populates _formatters, to keep track
    of names and their mapping to Formatter-derived classes.
    """
    def __new__(mcs, name, bases, attrs):
        cls = super(FormatterType, mcs).__new__(mcs, name, bases, attrs)
        if attrs.get('name', None) != None:
            _formatters[attrs['name']].append(cls)
        return cls


class Formatter(object):
    __metaclass__ = FormatterType
#    class __metaclass__(type):
#        def __init__(cls, name, bases, attrs):
#            type.__init__(name, bases, attrs, {})
#            if attrs.get('name', None) != None:
#                _formatters[attrs['name']].append(cls)
    
    media_type = None # the media type of the format.
    name = None # name of the format.
    can_multiple = False # formatter can represent multiple responses.
    
    def __init__(self, ui_uri, uri, req_hdrs, lang, output):
        """
        Formatter for the given URI, writing
        to the callable output(uni_str). Output is Unicode; callee
        is responsible for encoding correctly.
        """
        self.ui_uri = ui_uri
        self.uri = uri
        self.req_hdrs = req_hdrs
        self.lang = lang
        self.output = output
        
    def feed(self, red, sample):
        """
        Feed a body sample to processor(s).
        """
        raise NotImplementedError
        
    def start_output(self):
        """
        Send preliminary output.
        """
        raise NotImplementedError

    def status(self, status):
        """
        Output a status message.
        """
        raise NotImplementedError        
        
    def finish_output(self, red):
        """
        Finalise output.
        """
        raise NotImplementedError

from redbot.formatter import *
