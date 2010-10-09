#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from rapidsms.backends.http import RapidHttpBacked
from django.http import HttpResponse, HttpResponseBadRequest
import datetime
from urllib import urlencode
from urllib2 import urlopen

class Push(RapidHttpBacked):
    """ A RapidSMS backend for PUSH SMS
    
    Example POST:
    
    RemoteNetwork=celtel-tz&IsReceipt=NO&BSDate-tomorrow=20101009&Local=*15522&ReceiveDate=2010-10-08%2016:46:22%20%2B0000&BSDate-today=20101008&ClientID=1243&MessageID=336876061&ChannelID=9840&ReceiptStatus=&ClientName=OnPoint%20-%20TZ&Prefix=JSI&MobileDevice=&BSDate-yesterday=20101007&Remote=%2B255785000017&MobileNetwork=celtel-tz&State=11&ServiceID=124328&Text=test%203&MobileNumber=%2B255785000017&NewSubscriber=NO&RegType=1&Subscriber=%2B255785000017&ServiceName=JSI%20Demo&Parsed=&BSDate-thisweek=20101004&ServiceEndDate=2010-10-30%2023:29:00%20%2B0300&Now=2010-10-08%2016:46:22%20%2B0000
    
    """

    def configure(self, config=None, **kwargs):
        self.config = config
        super(Push, self).configure(**kwargs)

    def handle_request(self, request):
        if request.method != 'POST':
            return HttpResponse('Not a post!')
        #self.debug('This is the entire request (raw): %s' % request)
        self.debug('This is the PUSH inbound POST data: %s' % request.raw_post_data)
        message = self.message(request.POST)
        if message:
                self.route(message)
        #We may need to return some XML here, but the current config is sending URL-encoded POST data and not XML, so we'll just send back a 200 OK
        return HttpResponse('OK')

    def message(self, data):
        text = data.get('Text', '')
        mobile_number = data.get('MobileNumber', '')
        if not text or not mobile_number:
            self.error('Missing mobile number or text: %s' % data)
            return None
        now = datetime.datetime.utcnow()
        return super(Push, self).message(mobile_number, text, now)
        self.debug(data)
    def send(self, message):
#    base_url = 'http://api.tropo.com/1.0/sessions'
#    token = '1c58694261c3714c9598abaa13d22bdc9c859f31383805bb8445a3fe40e0e19d3017b06ed4e56ae582695210'        # Insert your token here
#    token = '8dedf13d8330b24dade023972bf72db1eb347eefbcbf46aea81ea94a794385eeba9951d94debd9918b5f61b3'
#    action = 'create'
#    number = '14122677933'    
#
#    params = urlencode([('action', action), ('token', token), ('numberToDial', message.connection.identity), ('msg', message.text)])
#    self.debug("%s?%s" % (base_url, params))
#    data = urlopen('%s?%s' % (base_url, params)).read()
     self.debug(message)

