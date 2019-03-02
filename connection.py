import psycopg2

def getConnection():
	conn=''
	if conn !='':
		return conn
	else:	
		try:
			conn = psycopg2.connect(host="localhost",database="fighters-event", user="postgres", password="123456",port="5432")
			return conn
		except:
			print "Unable to connect"
			exit(1)
