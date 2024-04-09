from openpyxl import Workbook
import os

def create_output(info_list, name):
        wb = Workbook()
        ws = wb.active
        
        ws.append(("Subscriber Number", "Subscriber Status", "Additional Status", "Call-out Authority", "Call-in Authority", "Supplememtary Service"))
        for i in info_list:
            ws.append(i)
        wb.save(os.path.join("outputs", name))
