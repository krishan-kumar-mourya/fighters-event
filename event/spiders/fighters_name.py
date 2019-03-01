# -*- coding: utf-8 -*-
import sys
import os
import traceback
import scrapy
import scrapy.spiders
import psycopg2
from scrapy.conf import settings
from django.utils.encoding import smart_str

class fighterSpider(scrapy.Spider):
    name = 'fighter'
    allowed_domains = ['www.bestfightodds.com']
    start_urls = ['https://www.bestfightodds.com/events/ufc-231-holloway-vs-ortega-1584']

    def parse(self,response):
        print '==============================================================='
        event = {}
        event['name'] = response.css('div.table-outer-wrapper div.table-div div.table-header a::text').extract_first()
        event['date'] = response.css('div.table-outer-wrapper div.table-div div.table-header span.table-header-date::text').extract_first()
        
        fighters = {}
        fighters['name'] = response.css('div.table-outer-wrapper div.table-div div.table-inner-wrapper div.table-scroller table.odds-table tbody th span.tw::text').extract()

        # connect with database
        conn = None
        try:
            conn = psycopg2.connect(host="localhost",database="results", user="postgres", password="123456",port="5432") 
              
        except:
            print 'Error in connecting database'
            traceback.print_exc(file=sys.stdout)

        if conn is not None:
                # save event info in database
            event_id = self.save_event(conn,event)

                # save fighters info in database
            fighters_ids = self.save_fighters(conn,fighters)

                # save event fighter mapping
            self.event_fighter_mapping(conn,event_id,fighters_ids)
            conn.close()
            
        # print("Existing settings: %s" % self.settings.attributes.keys())

        print '==============================================================='

    def save_event(self, conn, event):
        event_name = event.get('name')
        event_date = event.get('date')
        cursor = conn.cursor()
        query = "select event_id,event_name from events where event_name='"+event_name+"'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result < 0:
           
            query = "INSERT INTO events (event_name,event_date) VALUES ('"+event_name+"','"+event_date+"')RETURNING event_id;"           
            try:
                # cursor = conn.cursor()
                cursor.execute(query)
                event_id = cursor.fetchone()[0]
                return event_id
            except:
                print 'Error in executing query'
                traceback.print_exc(file=sys.stdout)                

            cursor.close()
            conn.commit()
            # return event_id 
        else:
            print"Event already exists in the database!!!"
            event_id=result[0]
            return event_id

    def save_fighters(self, conn, fighters):
        fighter_name = fighters.get('name')
        fighter_coun = len(fighter_name)
        fighters_ids = []

        if fighter_coun > 0:
            cursor = conn.cursor()

            for i in range(fighter_coun):
                fighters_name = fighter_name[i]
                # print fighters_name
                query = "select fighter_name from fighters where fighter_name='"+fighters_name+"'"
                cursor.execute(query)
                result = cursor.fetchone()
                # print result
                if result < 0:
                    # print "eeeeeeeeeeee"
                    query = "INSERT INTO fighters (fighter_name) VALUES ('"+fighters_name+"')RETURNING fighter_id;"

                    # print query
                    try:
                        cursor.execute(query)
                        
                        fighters_id = cursor.fetchone()[0]
                        # return fighters['id']return fighters
                        # print fighters['id']
                        # print "fffffffffffffffffffffffffffffff"
                        fighters_ids.append(fighters_id)
                        # print fighters['id']
                    except:
                        print 'Error in executing query'
                        traceback.print_exc(file=sys.stdout)
                else:
                    print ("Fighter name already insert change name !!!! ")
                    # print i   
            
        cursor.close()
        conn.commit()
        return fighters_ids

    def event_fighter_mapping(self,conn,event_id,fighters_ids):
        event_id = event_id
        # print event_id
        fighters_id = fighters_ids
        # print fighters_id
        fighters_id_count = len(fighters_id)
        # print fighters_id_count
        cursor = conn.cursor()

        # print fighters_id_count
        for i in range(fighters_id_count):
            fighter_id = fighters_id[i]
            # print event_id 
            # print fighter_id
            query = "INSERT INTO juction (fighter_id,event_id) VALUES (%s,%s)"
            # print query
            try:
                cursor.execute(query,(event_id,fighter_id))
            except:
                print 'Error in executing query'
                traceback.print_exc(file=sys.stdout)    
        cursor.close()
        conn.commit()

    print 'Fighters extracted and saved in database'