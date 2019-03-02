import connection

if __name__ == '__main__':
	conn = connection.getConnection()
	cursor = conn.cursor()

	query = "SELECT fighter_name FROM fighters WHERE fighter_name LIKE ANY(array['% A%' ,'% B%' ,'% C%'])"
	cursor.execute(query)
	result=cursor.fetchall()
	for i in result:
		print i[0]