import sqlite3
class rtfm(object):

	
        def lookup(self,command):
                message = 'Sorry I do not understand what your trying to search.'
                attachment = False


                if command.startswith('rtfm'):
			sqlcmd = []
			sqltpl = []
			sqllst = []
			conn = sqlite3.connect('resources/rtfm/snips.db')
			if not ' ' in command:
				return "You need to include a search term such as RDP", attachment
			search = "{}".format(command.split(' ')[1])
			if search: 
				sqlcmd.append(" AND (c.cmd LIKE ? OR c.cmnt like ? or tc.tag LIKE ? OR c.author LIKE ?)")
				sqltpl.append("%"+search+"%")
				sqltpl.append("%"+search+"%")
				sqltpl.append("%"+search+"%")
				sqltpl.append("%"+search+"%")
				message = self.Search(conn, sqlcmd, sqltpl, sqllst)
				attachment = True
			else:
				message = "You need to include a search term such as rtfm rdp"
		return message, attachment






	def Search(self,conn, sqlcmd, sqltpl, sqllst):
		cur = conn.cursor()
		sql = "SELECT c.cmdid, c.cmd, c.cmnt, c.date, c.author, group_concat(DISTINCT tc.tag), group_concat(DISTINCT ref)"
		sql += " FROM tblcommand c JOIN tbltagmap tm ON tm.cmdid = c.cmdid JOIN tbltagcontent tc ON "
		sql += " tc.tagid = tm.tagid JOIN tblrefmap rm ON rm.cmdid = c.cmdid"
		sql += " JOIN tblrefcontent rc on rc.id = rm.refid"
		sql += " ".join(sqlcmd)
		sql += " GROUP BY c.cmdid "
		cur.execute(sql, sqltpl)
		rows = cur.fetchall()
		findings = []
		for cmd in rows:
			findings.append({"short": False, "title": "Description", "value": "{}".format(cmd[2])})
			findings.append({"short": False, "title": "Port", "value": "{}".format(str(cmd[0]))})
			findings.append({"short": False, "title": "Command", "value": "{}".format(cmd[1])})
			findings.append({"short": False, "title": "Tags", "value": "{}".format(cmd[5])})
			findings.append({"short": False, "title": "--------------------------------------", "value": ""})

		message2 = [{"fallback": "blah", "pretext": "The following RTFM entries were found:", "fields": findings}]
		return message2
