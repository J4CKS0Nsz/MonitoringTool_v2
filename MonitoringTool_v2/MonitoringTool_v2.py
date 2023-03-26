from datetime import datetime
import configparser
import smtplib
import time
from icmplib import ping
import psutil


##READCONFIG
conf = configparser.ConfigParser()
conf.read("MonitoringTool.ini")
conf_mail_server = conf.get("alertmail", "server")
conf_mail_sslport = conf.getint("alertmail", "sslport")
conf_mail_from = conf.get("alertmail", "from")
conf_mail_pass = conf.get("alertmail", "pass")
conf_mail_to = conf.get("alertmail", "to")
conf_cpu_warn_maxpct = conf.getfloat("cpu", "warn_maxpct")
conf_ram_warn_maxpct = conf.getfloat("ram", "warn_maxpct")
conf_ram_warn_maxmb = conf.getint("ram", "warn_maxmb")
conf_disk_path = conf.get("disk", "checkpath")
conf_disk_warn_maxpct = conf.getfloat("disk", "warn_maxpct")
conf_disk_warn_maxgb = conf.getint("disk", "warn_maxgb")


##LOG
def do_log(log_message):
    print(log_message)
    log_file = open(str(get_current_date())+"_monitoring.log", "a")
    log_file.write("\n"+log_message)
    log_file.close
    return True

##SENDALARTMAIL
def do_report(mail_message,mail_subjekt):
    mail_content = """From: MonitoringTool <{}>
To: {} <{}>
Subject: {}

{}""".format(conf_mail_from,conf_mail_to,conf_mail_to,mail_subjekt,mail_message)
    print(mail_content)
    mail_server = smtplib.SMTP_SSL(host=conf_mail_server,port=conf_mail_sslport)
    mail_server.login(conf_mail_from,conf_mail_pass)
    mail_server.sendmail(conf_mail_from,conf_mail_to,mail_content)
    mail_server.quit()
    return True

##TIME
def get_current_datetime():
    return datetime.now().replace(microsecond=0)

def get_current_date():
    return datetime.today().date()

##CPU
def get_current_cpu_usage_pct():
    return psutil.cpu_percent(interval=0.1)

##RAM
def get_current_ram_usage_pct():
    return psutil.virtual_memory().percent

def get_current_ram_usage():
    return int(float(psutil.virtual_memory().used)/1024/1024)

def get_ram_total():
    return int(float(psutil.virtual_memory().total)/1024/1024)

##DISK
def get_current_disk_usage_pct():
    return psutil.disk_usage(conf_disk_path).percent

def get_current_disk_usage():
    return int(float(psutil.disk_usage(conf_disk_path).used)/1024/1024/1024)

def get_disk_total():
    return int(float(psutil.disk_usage(conf_disk_path).total)/1024/1024/1024)

##Network
def get_ping():
    return ping("google.com", count=4, interval=1, timeout=1).avg_rtt

#do_report("hello","Warnung")
while True:
    do_log("-------------------------------------------------------------------------------------")

    cpu_usage_pct = get_current_cpu_usage_pct()
    if cpu_usage_pct >= conf_cpu_warn_maxpct:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : CPU              : Auslastung ueber "+str(conf_cpu_warn_maxpct)+" %")
        while cpu_usage_pct >= conf_cpu_warn_maxpct:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : CPU              : Auslastung: "+str(cpu_usage_pct)+" %")
            time.sleep(1)
            cpu_usage_pct = get_current_cpu_usage_pct()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : CPU              : Auslastung unter "+str(conf_cpu_warn_maxpct)+" % (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : CPU              : Auslastung: "+str(cpu_usage_pct)+" %")


    ram_usage_pct = get_current_ram_usage_pct()
    if ram_usage_pct >= conf_ram_warn_maxpct:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : Ueber "+str(conf_ram_warn_maxpct)+" % belegt")
        while ram_usage_pct >= conf_ram_warn_maxpct:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : In Verwendung: "+str(ram_usage_pct)+" %")
            time.sleep(1)
            ram_usage_pct = get_current_ram_usage_pct()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : RAM              : Unter "+str(conf_ram_warn_maxpct)+" % belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : RAM              : In Verwendung: "+str(ram_usage_pct)+" %")


    ram_usage = get_current_ram_usage()
    if ram_usage >= conf_ram_warn_maxmb:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : Ueber "+str(conf_ram_warn_maxmb)+" MB belegt")
        while ram_usage >= conf_ram_warn_maxmb:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : In Verwendung: "+str(ram_usage)+" MB von "+str(get_ram_total())+" MB")
            time.sleep(1)
            ram_usage = get_current_ram_usage()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : RAM              : Unter "+str(conf_ram_warn_maxmb)+" MB belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : RAM              : In Verwendung: "+str(ram_usage)+" MB von "+str(get_ram_total())+" MB")


    disk_usage_pct = get_current_disk_usage_pct()
    if disk_usage_pct >= conf_disk_warn_maxpct:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : Ueber "+str(conf_disk_warn_maxpct)+" % belegt")
        while disk_usage_pct >= conf_disk_warn_maxpct:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(disk_usage_pct)+" %")
            time.sleep(1)
            disk_usage_pct = get_current_disk_usage_pct()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : Datentraeger "+conf_disk_path+" : Unter "+str(conf_disk_warn_maxpct)+" % belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(disk_usage_pct)+" %")


    disk_usage = get_current_disk_usage()
    if disk_usage >= conf_disk_warn_maxgb:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : Ueber "+str(conf_disk_warn_maxgb)+" GB belegt")
        while disk_usage >= conf_disk_warn_maxgb:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(disk_usage)+" GB von "+str(get_disk_total())+" GB")
            time.sleep(1)
            disk_usage = get_current_disk_usage()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : Datentraeger "+conf_disk_path+" : Unter "+str(conf_disk_warn_maxgb)+" % belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(disk_usage)+" GB von "+str(get_disk_total())+" GB")


    do_log(str(get_current_datetime())+" :: <OK>         : Netzwerk         : Ping: "+str(get_ping())+" ms")


    time.sleep(2)
exit