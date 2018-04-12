from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from zapv2 import ZAPv2
from subprocess import Popen
import os
from time import sleep
import requests
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

zap = ZAPv2(proxies={'http': 'http://localhost:8090', 'https': 'http://localhost:8090'})

@dispatcher.add_method
def start_zap_scanner():
    try:
        cmd = '{0} -config api.disablekey=true -port {1}'.format(os.getenv("PATH_ZAP_SH", "/someplace/zap.sh"), os.getenv("ZAP_PORT", 8080))
        Popen(cmd.split(' '), stdout = open(os.devnull, 'w'))
        sleep(15)
        return "ZAP Started Successfully"
    except:
        return "Failed to start ZAP Scanner"

@dispatcher.add_method
def start_zap_spider(**kwargs):
    try:
        scan_id = zap.spider.scan(kwargs['baseUrl'])
        return {"spider_id": scan_id, "message": "Spider Successfully Started"}
    except:
        return "ERROR: Failed to start Scan"

@dispatcher.add_method
def get_spider_status(spider_id):
    return zap.spider.status(spider_id)

@dispatcher.add_method
def start_zap_active_scan(**kwargs):
    try:
        scan_id = zap.ascan.scan(kwargs['baseUrl'], scanpolicyname=kwargs['scan_policy'], inscopeonly=kwargs['in_scope_only'])
        return {"scan_id": scan_id, "message": "Scan Successfully Started"}
    except:
        return "ERROR: Failed to start Scan"

@dispatcher.add_method
def get_ascan_status(scan_id):
    return zap.ascan.status(scanid=scan_id)

@dispatcher.add_method
def write_json_report(**kwargs):
    url = 'http://localhost:{0}/JSON/exportreport/action/generate/'.format(os.getenv("ZAP_PORT", 8080))
    export_path = kwargs['fullpath']
    extension = kwargs['export_format']
    report_time = datetime.now().strftime("%I:%M%p on %B %d, %Y")
    source_info = '{0};{1};ZAP Team;{2};{3};v1;v1;{4}'.format(kwargs['report_title'], kwargs['report_author'], report_time, report_time,
                                                               kwargs['report_title'])
    alert_severity = 't;t;t;t'  # High;Medium;Low;Info
    alert_details = 't;t;t;t;t;t;t;t;t;t'  # CWEID;#WASCID;Description;Other Info;Solution;Reference;Request Header;Response Header;Request Body;Response Body
    data = {'absolutePath': export_path, 'fileExtension': extension, 'sourceDetails': source_info,
            'alertSeverity': alert_severity, 'alertDetails': alert_details}

    r = requests.post(url, data=data)
    if r.status_code == 200:
        return "Successfully written to target path: {0}".format(export_path)
    else:
        raise Exception("Unable to generate report")

@dispatcher.add_method
def kill_zap():
    zap.core.shutdown()
    return "zap has been shutdown"


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype="application/json")


if __name__ == "__main__":
    run_simple('localhost', int(os.getenv("JRPC_PORT", 4000)), application)