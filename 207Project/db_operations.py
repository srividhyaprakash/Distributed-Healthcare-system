def update_patient_scan_report:
	if request.method == 'POST':
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			scan_report_name = request.form['reportName']	# have scan_report_name field as reportName in html code
			p_id = request.form['uname']					# have username field as uname
			cur = conn.cursor()
			cur.execute("""UPDATE patient SET p_scan_report = ? where p_id = ?""",(scan_report_name,p_id))
			
			conn.commit()
			msg = "Record successfully updated"
		except:
			print("error in database connection or access")
			msg = "error in update operation"
			conn.rollback()
		finally:
			print("closing connection")
			conn.close()
			return render_template('patient.html', msg = msg)		# go back to patient.html and render with the msg block dynamically


def delete_patient_record:
	if request.method == 'POST':
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			p_id = request.form['uname']					# have username field as uname
			cur.execute('DELETE FROM tasks WHERE id=?',(p_id,))
			cur = conn.cursor()
			conn.commit()
			msg = "Your data has been successfully deleted"
		except:
			print("error in database connection or access")
			msg = "error in delete operation"
			conn.rollback()
		finally:
			print("closing connection")
			conn.close()
			return render_template('input.html', msg = msg)		# go back to input.html and render with the msg block dynamically

def check_insurance_result():
	if request.method == 'POST':
		try:
			conn = sql.connect('db_1.0.db')
			print("Opened database successfully")
			i_name = request.form['insurance_comp_name']

			cur = conn.cursor()
			cur.execute("select patient.p_name from patient, insurance where i_company_name = ? and insurance.i_p_id = patient.p_id", (i_name,))

			rows = cur.fetchall()
			for row in rows:
				print(row[0])		# check the type here and print accordingly or append to a list and send that to check_insurance_result.html
		except:
			print("error in database connection or access")
		finally:
			print("closing database connection")
			conn.close()
