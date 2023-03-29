from datetime import datetime
from time import sleep
from configparser import ConfigParser as configparser
from smtplib import SMTP_SSL as smtp_ssl
from psutil import cpu_percent, virtual_memory, disk_usage
from icmplib import ping, exceptions as pingexc
import os


##READCONFIG
conf = configparser()
conf.read("MonitoringTool.ini")
conf_mail_server = conf.get("alertmail", "server")
conf_mail_sslport = conf.getint("alertmail", "sslport")
conf_mail_from = conf.get("alertmail", "from")
conf_mail_pass = conf.get("alertmail", "pass")
conf_mail_to = conf.get("alertmail", "to")
conf_cpu_warn_maxpct = conf.getfloat("cpu", "warn_maxpct")
conf_ram_warn_maxpct = conf.getfloat("ram", "warn_maxpct")
conf_ram_warn_maxmb = conf.getint("ram", "warn_maxmb")
conf_disk_path = os.path.sep ##conf.get("disk", "checkpath")
conf_disk_warn_maxpct = conf.getfloat("disk", "warn_maxpct")
conf_disk_warn_maxgb = conf.getint("disk", "warn_maxgb")
conf_network_ping_address = conf.get("network", "ping_address")
conf_network_warn_maxping = conf.getfloat("network", "warn_maxping")


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
    mail_server = smtp_ssl(host=conf_mail_server,port=conf_mail_sslport)
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
    return cpu_percent(interval=0.1)

##RAM
def get_current_ram_usage_pct():
    return virtual_memory().percent

def get_current_ram_usage():
    return int(float(virtual_memory().used)/1024/1024)

def get_ram_total():
    return int(float(virtual_memory().total)/1024/1024)

##DISK
def get_current_disk_usage_pct():
    return disk_usage(conf_disk_path).percent

def get_current_disk_usage():
    return int(float(disk_usage(conf_disk_path).used)/1024/1024/1024)

def get_disk_total():
    return int(float(disk_usage(conf_disk_path).total)/1024/1024/1024)

##Network
def get_current_ping():
    try:
        current_ping = ping(conf_network_ping_address, count=4, interval=1, timeout=1).avg_rtt
    except pingexc.NameLookupError:
        return 0
    else:
        return current_ping


#do_report("hello","Warnung")
while True:
    do_log("-------------------------------------------------------------------------------------")


    get_cpu_usage_pct = get_current_cpu_usage_pct()
    if get_cpu_usage_pct >= conf_cpu_warn_maxpct:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : CPU              : Auslastung ueber "+str(conf_cpu_warn_maxpct)+" %")
        while get_cpu_usage_pct >= conf_cpu_warn_maxpct:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : CPU              : Auslastung: "+str(get_cpu_usage_pct)+" %")
            sleep(1)
            get_cpu_usage_pct = get_current_cpu_usage_pct()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : CPU              : Auslastung unter "+str(conf_cpu_warn_maxpct)+" % (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : CPU              : Auslastung: "+str(get_cpu_usage_pct)+" %")


    get_ram_usage_pct = get_current_ram_usage_pct()
    if get_ram_usage_pct >= conf_ram_warn_maxpct:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : Ueber "+str(conf_ram_warn_maxpct)+" % belegt")
        while get_ram_usage_pct >= conf_ram_warn_maxpct:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : In Verwendung: "+str(get_ram_usage_pct)+" %")
            sleep(1)
            get_ram_usage_pct = get_current_ram_usage_pct()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : RAM              : Unter "+str(conf_ram_warn_maxpct)+" % belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : RAM              : In Verwendung: "+str(get_ram_usage_pct)+" %")


    get_ram_usage = get_current_ram_usage()
    if get_ram_usage >= conf_ram_warn_maxmb:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : Ueber "+str(conf_ram_warn_maxmb)+" MB belegt")
        while get_ram_usage >= conf_ram_warn_maxmb:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : RAM              : In Verwendung: "+str(get_ram_usage)+" MB von "+str(get_ram_total())+" MB")
            sleep(1)
            get_ram_usage = get_current_ram_usage()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : RAM              : Unter "+str(conf_ram_warn_maxmb)+" MB belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : RAM              : In Verwendung: "+str(get_ram_usage)+" MB von "+str(get_ram_total())+" MB")


    get_disk_usage_pct = get_current_disk_usage_pct()
    if get_disk_usage_pct >= conf_disk_warn_maxpct:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : Ueber "+str(conf_disk_warn_maxpct)+" % belegt")
        while get_disk_usage_pct >= conf_disk_warn_maxpct:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(get_disk_usage_pct)+" %")
            sleep(1)
            get_disk_usage_pct = get_current_disk_usage_pct()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : Datentraeger "+conf_disk_path+" : Unter "+str(conf_disk_warn_maxpct)+" % belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(get_disk_usage_pct)+" %")


    get_disk_usage = get_current_disk_usage()
    if get_disk_usage >= conf_disk_warn_maxgb:
        incident_start = get_current_datetime()
        do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : Ueber "+str(conf_disk_warn_maxgb)+" GB belegt")
        while get_disk_usage >= conf_disk_warn_maxgb:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(get_disk_usage)+" GB von "+str(get_disk_total())+" GB")
            sleep(1)
            get_disk_usage = get_current_disk_usage()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : Datentraeger "+conf_disk_path+" : Unter "+str(conf_disk_warn_maxgb)+" % belegt (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : Datentraeger "+conf_disk_path+" : In Verwendung: "+str(get_disk_usage)+" GB von "+str(get_disk_total())+" GB")

        
    get_ping = get_current_ping()
    if get_ping >= conf_network_warn_maxping or get_ping == 0:
        incident_start = get_current_datetime()
        if get_ping >= conf_network_warn_maxping:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : Netzwerk         : Ping ueber "+str(conf_network_warn_maxping)+" ms")
        else:
            do_log(str(get_current_datetime())+" :: <WARNUNG>    : Netzwerk         : Ping nicht moeglich")
        while get_ping >= conf_network_warn_maxping or get_ping == 0:
            if get_ping >= conf_network_warn_maxping:
                do_log(str(get_current_datetime())+" :: <WARNUNG>    : Netzwerk         : Ping: "+str(get_ping)+" ms")
            else:
                do_log(str(get_current_datetime())+" :: <WARNUNG>    : Netzwerk         : Ping nicht moeglich")
            sleep(1)
            get_ping = get_current_ping()
        incident_end = get_current_datetime()
        incident_duration = incident_end-incident_start
        do_log(str(get_current_datetime())+" :: <ENTWARNUNG> : Netzwerk         : Ping unter "+str(conf_network_warn_maxping)+" ms (Vorfalldauer: "+str(incident_duration)+")")
    else:
        do_log(str(get_current_datetime())+" :: <OK>         : Netzwerk         : Ping: "+str(get_ping)+" ms")


    sleep(2)
