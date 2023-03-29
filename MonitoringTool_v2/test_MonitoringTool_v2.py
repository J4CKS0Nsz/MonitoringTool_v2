import unittest
from MonitoringTool import *

def test_cpu_usage():
    assert get_current_cpu_usage_pct() >= 0
    assert get_current_cpu_usage_pct() <= 100
    
def test_ram_usage():
    assert get_current_ram_usage_pct() >= 0
    assert get_current_ram_usage_pct() <= 100
    
def test_send_mail():
    mail_message = "Testnachricht"
    mail_subject = "Testbetreff"
    assert do_report(mail_message, mail_subject) == True
