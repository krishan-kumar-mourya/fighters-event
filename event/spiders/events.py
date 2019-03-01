# -*- coding: utf-8 -*-
import sys
import os
import traceback
import scrapy
from scrapy.spiders import XMLFeedSpider
from scrapy.selector import HtmlXPathSelector
import scrapy.spiders
from scrapy.selector import Selector
from scrapy.conf import settings
from scrapy_splash import SplashRequest
import psycopg2
from django.utils.encoding import smart_str
class eventSpider(XMLFeedSpider):
    name = 'event'
    allowed_domains = ['www.bestfightodds.com']
    start_urls = ['https://www.bestfightodds.com/events/ufc-231-holloway-vs-ortega-1584']
    def start_requests(self):
        urls = [
            
            'https://www.bestfightodds.com/events/ufc-231-holloway-vs-ortega-1584'
        ]
        for url in urls:
            print url
            yield SplashRequest(url, self.parse)
            print 'dddddddddddddddddddddddddddddddddddddddddddd'
    def parse(self,response):
        print '==============================================================='
        events = {}
        events['name'] = response.css('div.table-outer-wrapper div.table-div div.table-header a::text').extract()
        # print events['name']
        events['date'] = response.css('div.table-outer-wrapper div.table-div div.table-header span.table-header-date::text').extract()
        # print events['date']
        # print response   
        # connect with database
        conn = None
        try:
            conn = psycopg2.connect(host="localhost",database="results", user="postgres", password="123456",port="5432")
            # cursor = connection.cursor()
            # print conn   
        except:
            print 'Error in connecting database'
            traceback.print_exc(file=sys.stdout)

        if conn is not None:
            # save fighters info in database
            self.save_event(conn,events)
            conn.close()
            
        # print("Existing settings: %s" % self.settings.attributes.keys())

        print '==============================================================='

    def save_event(self, conn, events):
        event_name = events.get('name')
        event_date = events.get('date')
        event_coun = len(event_name)
        # print event_coun
        # print 'pppppppppppppppppppppppppppp' 

        if event_coun > 0:
            cursor = conn.cursor()

            for i in range(event_coun):
                event_name = event_name[i]
                event_date = event_date[i]
                # print event_name
                # print event_date

                query = "INSERT INTO events (event_name,event_date) VALUES ('"+event_name+"','"+event_date+"')"
                print query
                try:
                    cursor.execute(query)
                except:
                    print 'Error in executing query'
                    traceback.print_exc(file=sys.stdout)

        cursor.close()
        conn.commit()

        print 'Events extracted and saved in database'