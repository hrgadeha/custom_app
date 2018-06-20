# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dony and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ExpireBatchScheduler(Document):
	pass

def sendmail():
    user_list = frappe.db.sql("""select name, employee_name from `tabEmployee` where designation = "Batch Supervisor";""")
    for user_obj in user_list:
        user = user_obj[0];
        employee = user_obj[1];
        content = "<h4>Hello, "+ employee +"</h4><p>Following Batch will be expiry soon. Please make a note for that.</p><table class='table table-bordered'><tr><th>Batch Number</th><th>Expiry Date</th></tr>"
        batch_list = frappe.db.sql("""select batch_id, expiry_date  from `tabBatch` where DATEDIFF(expiry_date, CURRENT_DATE()) < 30;""")
        for batch_obj in batch_list:
            batch = batch_obj[0]
            expiry_date = str(batch_obj[1].strftime('%d/%m/%Y'))
            content = content + "<tr><td>"+batch+"</td><td>"+expiry_date+"</td></tr>"         
        content = content + "</table>"
        recipient = frappe.get_value("Employee", user, "prefered_email")
        frappe.sendmail(recipients=[recipient],
            sender="hardikgadesha@gmail.com",
            subject="Item Batch To Be Expire", content=content)
