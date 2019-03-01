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
# from django.utils.encoding import smart_str
conn = psycopg2.connect(host="localhost",database="results", user="postgres", password="123456",port="5432")
cursor = conn.cursor()
query = "select fighter_id .fighters,event_id.events from fighters inner join events "
print(query)
# cursor.execute(query)
# connection.commit()










# class fighterSpider(XMLFeedSpider):
#     name = 'fighter'
#     allowed_domains = ['www.bestfightodds.com']
#     start_urls = ['https://www.bestfightodds.com/events/ufc-231-holloway-vs-ortega-1584']
#     def start_requests(self):
#         urls = [
            
#             'https://www.bestfightodds.com/events/ufc-231-holloway-vs-ortega-1584'
#         ]
#         for url in urls:
#             print url
#             yield SplashRequest(url, self.parse)
#             print 'dddddddddddddddddddddddddddddddddddddddddddd'
#     def parse(self,response):
#         print '==============================================================='
#         fighters = {}
#         fighters['name'] = response.css('div.table-outer-wrapper div.table-div div.table-inner-wrapper div.table-scroller table.odds-table tbody th span.tw::text').extract()

#         # print response
#         # print '============================='
#         # print fighters['name']
#         # connect with database
#         conn = None
#         try:
#             conn = psycopg2.connect(host="localhost",database="results", user="postgres", password="123456",port="5432")
#             # cursor = connection.cursor()
#             # print conn   
#         except:
#             print 'Error in connecting database'
#             traceback.print_exc(file=sys.stdout)

#         if conn is not None:
#             # save fighters info in database
#             self.save_fighters(conn,fighters)
#             conn.close()
            
#         # print("Existing settings: %s" % self.settings.attributes.keys())

#         print '==============================================================='

#     def save_fighters(self, conn, fighters):
#         fighter_name = fighters.get('name')
#         fighter_coun = len(fighter_name)
#         # print fighter_coun
#         # print 'pppppppppppppppppppppppppppp' 

#         if fighter_coun > 0:
#             cursor = conn.cursor()

#             for i in range(fighter_coun):
#                 fighters_name = fighter_name[i]
#                 # print fighters_name

#                 query = "INSERT INTO fighters (fighter_name) VALUES ('"+fighters_name+"')"
#                 # print query
#                 try:
#                     cursor.execute(query)
#                 except:
#                     print 'Error in executing query'
#                     traceback.print_exc(file=sys.stdout)

#         cursor.close()
#         conn.commit()

#         print 'Stores extracted and saved in database'