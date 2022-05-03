# app 程序的入口
from uis.Scan_app import Scan_APP
import sys

app = Scan_APP()
status = app.exec_()
sys.exit(status)

