from db.SqlExecutor import SqlExecutor


class CommitteeCache:
    def __init__(self):
        self.db = SqlExecutor()

    def store_committee_data(self, comm_name, comm_id, year_created, comm_purpose):
        sql = 'INSERT INTO `COMMITTEE` (NAME, ID, YEAR_CREATED, PURPOSE) VALUES(?, ?, ?, ?)'
        self.db.exec_insert(sql, (comm_name, comm_id, year_created, comm_purpose))

    def get_all_committee_data(self):
        sql = 'SELECT * FROM `COMMITTEE`'
        result = self.db.exec_select(sql).fetchall()
        return result

    def get_committee_data_using_name(self, name):
        sql = 'SELECT * FROM `COMMITTEE` WHERE NAME=?'
        result = self.db.exec_select(sql, (name,)).fetchall()
        return result

    def get_committee_data_using_id(self, comm_id):
        sql = 'SELECT * FROM `COMMITTEE` WHERE ID=?'
        result = self.db.exec_select(sql, (comm_id,)).fetchall()
        return result

    def store_memberships(self, mem_id, comm_id, session_num):
        sql = 'INSERT INTO `COMMITTEE_MEMBERSHIP` (MEMBER_ID, COMMITTEE_ID, SESSION) VALUES(?, ?, ?)'
        self.db.exec_insert(sql, (mem_id, comm_id, session_num))

    def get_all_current_committee_members_comm_id(self, comm_id, session_num):
        sql = 'SELECT * FROM `COMMITTEE_MEMBERSHIP` INNER JOIN `MEMBER` ON `COMMITTEE_MEMBERSHIP`.MEMBER_ID=`MEMBER`.ID ' \
              'WHERE COMMITTEE_ID=?'
        result = self.db.exec_select(sql, (comm_id, session_num)).fetchall()
        return result

    def get_all_committees_of_member(self, mem_id, session_num):
        sql = 'SELECT * FROM `COMMITTEE_MEMBERSHIP` INNER JOIN `COMMITTEE` ' \
              'ON `COMMITTEE_MEMBERSHIP`.COMMITTEE_ID=`COMMITTEE`.ID ' \
              'WHERE MEMBER_ID=?'
        result = self.db.exec_select(sql, (mem_id, session_num)).fetchall()
        return result

