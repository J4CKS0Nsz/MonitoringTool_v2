import unittest
from MonitoringTool_v2 import *

class test_MonitoringTool_v2 (unittest.Testcase):
    def test_cpu_usage(self):
        self.assertGreaterEqual(get_current_cpu_usage_pct(), 0)
        self.assertLessEqual(get_current_cpu_usage_pct(), 100)
    def test_ram_usage():
        self.assertGreaterEqual(get_current_ram_usage_pct(), 0)
        self.assertLessEqual(get_current_ram_usage_pct(), 100)
    def test_send_mail():
        mail_message = "Testnachricht"
        mail_subject = "Testbetreff"
        self.assertTrue (do_report(mail_message, mail_subject))
