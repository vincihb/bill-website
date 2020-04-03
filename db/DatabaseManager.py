import pymysql as mysql


class DatabaseManager:

	def __init__(self):
		self._connection = mysql.connect(
			host='localhost',
			user='root',
			password='',
			database='cit-test',
			charset='utf8mb4',
			cursorclass=mysql.cursors.DictCursor)

	# SELECT
	def reception_query(self, query_string, args=False):
		res = (0,)

		try:
			cursor = self._connection.cursor()
			if not args:
				cursor.execute(query_string)
			else:
				cursor.execute(query_string, args)

			res = cursor.fetchall()
			cursor.close()

		except:
			print('An error occurred trying to execute the change of state query \n' + query_string + ' -> ' +  (query_string % args))
			self._connection.rollback()
		finally:
			return res

	# INSERT, UPDATE, DELETE
	def change_of_state_query(self, query_string, args=(0,)):
		res = tuple()
		try:
			with self._connection.cursor() as cursor:
				if args == (0,):
					cursor.execute(query_string)
				else:
					cursor.execute(query_string, args)

			self._connection.commit()

		except mysql.Error:
			print('An error occurred trying to execute the change of state query \n' + query_string)
		finally:
			return res

	def build_db(self):
		table = """
				DELETE DATABASE IF EXISTS `cit-test`;
				CREATE DATABASE IF NOT EXISTS `cit-test`;
		
				CREATE TABLE `bill` (
    				`id` int(11) NOT NULL AUTO_INCREMENT,
    				`name` varchar(255) COLLATE utf8_bin NOT NULL,
    				`author` varchar(255) COLLATE utf8_bin DEFAULT NULL,
    				`state` varchar(255) COLLATE utf8_bin NOT NULL,
    				PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
				AUTO_INCREMENT=1;

				CREATE TABLE `cache` (
					`id` int(11) NOT NULL AUTO_INCREMENT,
					`first_name` varchar(255) COLLATE utf8_bin NOT NULL,
					`last_name` varchar(255) COLLATE utf8_bin NOT NULL,
					`full_name` varchar(255) COLLATE utf8_bin NOT NULL,
					`url` varchar(255) COLLATE utf8_bin NOT NULL,
					`credit` varchar(100) COLLATE utf8_bin NOT NULL,
					`cache_date` DATETIME NOT NULL DEFAULT NOW(),
					PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
				AUTO_INCREMENT=1;
				"""

		self.change_of_state_query(table)

	def __del__(self):
		self._connection.close()


dbm = DatabaseManager()
# dbm.build_db()
