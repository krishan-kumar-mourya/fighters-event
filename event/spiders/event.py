# -*- coding: utf-8 -*-
import sys
import traceback
import scrapy

# import connection
import connection


class fighterSpider(scrapy.Spider):
    conn = connection.getConnection()
    
    name = 'event'
    allowed_domains = ['www.bestfightodds.com']
    start_urls = ['https://www.bestfightodds.com/events/ufc-231-holloway-vs-ortega-1584']

    def parse(self,response):
        print '==============================================================='
        event = {}
        event['name'] = response.css('div.table-outer-wrapper div.table-div div.table-header a::text').extract_first()
        event['date'] = response.css('div.table-outer-wrapper div.table-div div.table-header span.table-header-date::text').extract_first()
        
        fighters = {}
        fighters['name'] = response.css('div.table-outer-wrapper div.table-div div.table-inner-wrapper div.table-scroller table.odds-table tbody th span.tw::text').extract()

        if self.conn is not None:
            # save event info in database
            event_id = self.save_event(self.conn, event)
            # save fighters info in database
            fighters_ids = self.save_fighters(self.conn, fighters)
            # save event fighter mapping
            self.event_fighter_mapping(self.conn, event_id, fighters_ids)
            self.conn.close()

            print 'Event and Fighters extracted and saved in database'
        else:
            print 'Not able to connect to database'

        print '==============================================================='

    def save_event(self, conn, event):
        event_name = event.get('name')
        event_date = event.get('date')

        cursor = conn.cursor()
        query = "select event_id,event_name from events where event_name=%s"
        cursor.execute(query,(event_name,))
        result = cursor.fetchone()
        if result < 0:
            query = "INSERT INTO events (event_name,event_date) VALUES (%s,%s)RETURNING event_id;"           
            try:
                cursor.execute(query,(event_name,event_date))
                event_id = cursor.fetchone()[0]
                return event_id
            except:
                print 'Error in executing query'
                traceback.print_exc(file=sys.stdout)                

            cursor.close()
            conn.commit()
        else:
            print"Event already exists in the database!!!"
            event_id=result[0]
            return event_id

    def save_fighters(self, conn, fighters):
        fighter_name = fighters.get('name')
        fighter_coun = len(fighter_name)
        fighters_ids = []

        cursor = conn.cursor()

        if fighter_coun > 0:
            for i in range(fighter_coun):
                fighters_name = fighter_name[i]
                query = "select fighter_id,fighter_name from fighters where fighter_name=%s"
                cursor.execute(query,(fighters_name,))
                result = cursor.fetchone()

                if result < 0:
                    query = "INSERT INTO fighters (fighter_name) VALUES (%s)RETURNING fighter_id;"
                    try:
                        cursor.execute(query,(fighters_name,))
                        fighters_id = cursor.fetchone()[0]
                        fighters_ids.append(fighters_id)
                    except:
                        print 'Error in executing query'
                        traceback.print_exc(file=sys.stdout)
                else:
                   fighters_id = result[0]
                   fighters_ids.append(fighters_id)

                    
        cursor.close()
        conn.commit()
        return fighters_ids

    def event_fighter_mapping(self,conn,event_id,fighters_ids):
        event_id = event_id
        fighters_id = fighters_ids
        fighters_id_count = len(fighters_id)

        cursor = conn.cursor()

        for i in range(fighters_id_count):
            fighter_id = fighters_id[i]

            query = "select fighter_id,event_id from event_fighter_mapping where fighter_id = %s AND event_id = %s"
            cursor.execute(query,(str(fighter_id), str(event_id)))
            result=cursor.fetchone()
            
            if result < 0:
                query = "INSERT INTO event_fighter_mapping (fighter_id,event_id) VALUES (%s,%s)"
                try:
                    cursor.execute(query,(fighter_id, event_id))
                except:
                    print 'Error in executing query'
                    traceback.print_exc(file=sys.stdout) 

        cursor.close()
        conn.commit()
