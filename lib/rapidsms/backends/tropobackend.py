#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from rapidsms.backends.http import RapidHttpBacked
from django.http import HttpResponse, HttpResponseBadRequest
import datetime
import urllib2
import urllib
from tropo import Tropo, Session

class TropoBackend(RapidHttpBacked):
    """ A RapidSMS backend for Tropo SMS API """

    def configure(self, config=None, **kwargs):
        self.config = config
        super(TropoBackend, self).configure(**kwargs)

    def handle_request(self, request):
	if request.method != 'POST':
		return HttpResponse('Not a post!')
        self.debug('This is the tropo Request (raw): %s' % request.raw_post_data)
        message = self.message(request.POST)
        if message:
            self.route(message)
	s = Session(request.raw_post_data)
        t = Tropo()
        t.hangup()
        return HttpResponse(t.RenderJson())

    def message(self, data):
        sms = data.get('msg', '')
        sender = data.get('user', '')
        if not sms or not sender:
            self.error('Missing from or text: %s' % data)
            return None
        now = datetime.datetime.utcnow()
        return super(TropoBackend, self).message(sender, sms, now)

    def send(self, message):
	import time
        time.sleep(3)
        tropo_token = '1c58694261c3714c9598abaa13d22bdc9c859f31383805bb8445a3fe40e0e19d3017b06ed4e56ae582695210'
#        url = 'http://api.tropo.com/1.0/sessions'
        url = 'http://api.tropo.com/1.0/sessions?action=create&token=1c58694261c3714c9598abaa13d22bdc9c859f31383805bb8445a3fe40e0e19d3017b06ed4e56ae582695210'

#        data = urllib.urlencode({'token':tropo_token,
#	         		 'action': 'create'})
	data = None
        req = urllib2.Request(url, data)
        try:
            self.debug('Sending: %s with params %s' % (url, data))
            response = urllib2.urlopen(url, data)
        except Exception, e:
            self.exception(e)
            return
        self.debug(response.read())

