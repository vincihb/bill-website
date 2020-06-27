from db.SqlExecutor import SqlExecutor


class AMemberCache:
	_member_table = None
	_session_table = None
	_db = None

	def _setup(self, member_table, session_table):
		self._member_table = member_table
		self._session_table = session_table
		self._db = SqlExecutor()

	def store_member_to_session(self, session_num, member_id):
		sql = 'INSERT INTO `%s` (SESSION_NUMBER, MEMBER_ID) VALUES(?, ?)' % self._member_table
		self._db.exec_insert(sql, (session_num, member_id))

	def get_all(self):
		sql = 'SELECT * FROM `%s`' % self._member_table
		result = self._db.exec_select(sql).fetchall()
		return result

	def get_by_id(self, member_id):
		sql = 'SELECT * FROM `%s` WHERE ID=?' % self._member_table
		result = self._db.exec_select(sql, (member_id,)).fetchone()
		return result

	def get_by_last_name(self, member_last_name):
		sql = 'SELECT * FROM `%s` WHERE LAST_NAME=?' % self._member_table
		result = self._db.exec_select(sql, (member_last_name,)).fetchall()
		return result

	def get_by_first_name(self, member_first_name):
		sql = 'SELECT * FROM `%s` WHERE FIRST_NAME=?' % self._member_table
		result = self._db.exec_select(sql, (member_first_name,)).fetchall()
		return result

	def get_by_district(self, district):
		sql = 'SELECT * FROM `%s` WHERE DISTRICT=?' % self._member_table
		result = self._db.exec_select(sql, (district,)).fetchall()
		return result

	def get_from_session(self, session_number):
		sql = 'SELECT * FROM `%s` INNER JOIN `%s` ON ' \
			  '`%s`.MEMBER_ID=`%s`.ID '\
			  'WHERE SESSION_NUMBER=?' \
			  % self._session_table, self._member_table, self._session_table, self._member_table
		result = self._db.exec_select(sql, (session_number,)).fetchall()
		return result

	def get_session_by_id(self, member_id):
		sql = 'SELECT * FROM `%s` INNER JOIN `CONGRESSIONAL_SESSION` ON ' \
			  '`%s`.SESSION_NUMBER=`CONGRESSIONAL_SESSION`.NUMBER ' \
			  'WHERE MEMBER_ID=?'  % self._session_table, self._session_table
		result = self._db.exec_select(sql, (member_id,)).fetchall()
		return result
