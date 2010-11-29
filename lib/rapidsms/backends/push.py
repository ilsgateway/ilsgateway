#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from rapidsms.backends.http import RapidHttpBacked
from django.http import HttpResponse, HttpResponseBadRequest
import datetime
from urllib import urlencode
from urllib2 import urlopen
from elementtree import ElementTree as ET
import urllib2
from rapidsms.conf import settings
import logging

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
        """
        <methodCall>
            <methodName>EAPIGateway.SendSMSItem</methodName>
            <params>
                <param>
                    <value>
                        <struct>
                            <member>
                                <name>Password</name>
                                <value>p487fhem</value>
                            </member>
                            <member>
                                <name>Channel</name>
                                <value><int>9840</int></value>
                            </member>
                            <member>
                                <name>Service</name>
                                <value><int>124524</int>
                                </value>
                            </member>
                            <member>
                                <name>SMSText</name>
                                <value>[text]</value>
                            </member>
                            <member>
                                <name>Numbers</name>
                                <value>[number]</value>
                            </member>                        
                        </struct>
                    </value>
                </param>
            </params>
        </methodCall>    
        """
        url = "https://dragon.operatelecom.com:1089/Gateway"
        password = "p487fhem"
        channel = "9840"
        service = "124524"
        numbers = message.connection.identity
        text = message.text
        
        root = ET.Element("methodCall")
        
        methodName = ET.SubElement(root, "methodName")
        methodName.text = "EAPIGateway.SendSMS"
        params = ET.SubElement(root, "params")
        param = ET.SubElement(params, "param")
        paramValue = ET.SubElement(param, "value")
        struct = ET.SubElement(paramValue, "struct")
        member1 = ET.SubElement(struct, "member")
        member1Name = ET.SubElement(member1, "name")
        member1Name.text = "Password"    
        member1Value = ET.SubElement(member1, "value")
        member1Value.text = password
        member2 = ET.SubElement(struct, "member")
        member2Name = ET.SubElement(member2, "name")
        member2Name.text = "Channel"    
        member2Value = ET.SubElement(member2, "value")
        member2Int = ET.SubElement(member2Value, "int")
        member2Int.text = channel
        member3 = ET.SubElement(struct, "member")
        member3Name = ET.SubElement(member3, "name")
        member3Name.text = "Service"    
        member3Value = ET.SubElement(member3, "value")
        member3Int = ET.SubElement(member3Value, "int")
        member3Int.text = service
        member4 = ET.SubElement(struct, "member")
        member4Name = ET.SubElement(member4, "name")
        member4Name.text = "Numbers"    
        member4Value = ET.SubElement(member4, "value")
        member4Value.text = numbers
        member5 = ET.SubElement(struct, "member")
        member5Name = ET.SubElement(member5, "name")
        member5Name.text = "SMSText"    
        member5Value = ET.SubElement(member5, "value")
        member5Value.text = text
        
        req = urllib2.Request(url=url, 
                              data=ET.tostring(root), 
                              headers={'Content-Type': 'application/xml'})
        
        if settings.ROUTER_MODE == 'PRODUCTION':
            logging.debug("PRODUCTION MODE")
            return ""
#            try:
#                handle = urllib2.urlopen(req)
#            except e:
#                print e   
#            print  HttpResponse(handle.read())
#            return HttpResponse(handle.read())
        elif settings.ROUTER_MODE == 'TEST':
            logging.debug("TEST MODE")
            return ""