import sys
sys.path.insert(0, './src/')
from pprint import pprint
import math
from familylink import FamilyLink
import logging.config



from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
# LOGGING_CONFIG = {
#     "version": 1,
#     "handlers": {
#         "default": {
#             "class": "logging.StreamHandler",
#             "formatter": "http",
#             "stream": "ext://sys.stderr"
#         }
#     },
#     "formatters": {
#         "http": {
#             "format": "%(levelname)s [%(asctime)s] %(name)s - %(message)s",
#             "datefmt": "%Y-%m-%d %H:%M:%S",
#         }
#     },
#     'loggers': {
#         'httpx': {
#             'handlers': ['default'],
#             'level': 'DEBUG',
#         },
#         'httpcore': {
#             'handlers': ['default'],
#             'level': 'DEBUG',
#         },
#     }
# }

# logging.config.dictConfig(LOGGING_CONFIG)
#
client = FamilyLink(browser="txt")
hostName = "localhost"
serverPort = 8080
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path)
        if path.path != '/api':
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Dave is not here man</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>Look deeper.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        query = urllib.parse.parse_qs(path.query)
        self.eval_request(query)

    def eval_request(self, query):
        if not 'command' in query:
            self.send_response(400)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            return
        if 'get_members' in query['command']:
            json_data = get_members()
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        elif 'lock' in query['command'] and 'user_id' in query:
            user_id = query['user_id'][0]
            children = get_members()
            for child in children:
                if child['id'] != user_id:
                    continue
                for device in child['devices']:
                    client.lock_device(child['id'], device['id'])
            children = get_members()
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        elif 'unlock' in query['command'] and 'user_id' in query:
            user_id = query['user_id'][0]
            children = get_members()
            for child in children:
                if child['id'] != user_id:
                    continue
                for device in child['devices']:
                    client.unlock_device(child['id'], device['id'])
            children = get_members()
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        elif 'enable_downtime' in query['command'] and 'user_id' in query:
            user_id = query['user_id'][0]
            children = get_members()
            for child in children:
                if child['id'] != user_id:
                    continue
                for device in child['devices']:
                    client.enable_downtime_device(child['id'], device['id'], device['down_time']['starts_at']['hour'], device['down_time']['starts_at']['minute'], device['down_time']['ends_at']['hour'], device['down_time']['ends_at']['minute'], device['down_time']['id'])
            children = get_members()
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        elif 'disable_downtime' in query['command'] and 'user_id' in query:
            user_id = query['user_id'][0]
            children = get_members()
            for child in children:
                if child['id'] != user_id:
                    continue
                for device in child['devices']:
                    client.disable_downtime_device(child['id'], device['id'], device['down_time']['starts_at']['hour'], device['down_time']['starts_at']['minute'], device['down_time']['ends_at']['hour'], device['down_time']['ends_at']['minute'], device['down_time']['id'])
            children = get_members()
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        elif 'enable_limits' in query['command'] and 'user_id' in query:
            user_id = query['user_id'][0]
            children = get_members()
            for child in children:
                if child['id'] != user_id:
                    continue
                for device in child['devices']:
                    client.enable_time_limits_device(child['id'], device['id'], device['limit']['id'], device['limit']['minutes'])
            children = get_members()
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        elif 'disable_limits' in query['command'] and 'user_id' in query:
            user_id = query['user_id'][0]
            children = get_members()
            for child in children:
                if child['id'] != user_id:
                    continue
                for device in child['devices']:
                    client.disable_time_limits_device(child['id'], device['id'], device['limit']['id'], device['limit']['minutes'])
            children = get_members()
            json_data = children
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        elif 'update_time' in query['command'] and 'user_id' in query and 'amount' in query:
            user_id = query['user_id'][0]
            amount = int(query['amount'][0])
            children = get_members()
            for child in children:
                if child['id'] != user_id:
                    continue
                for device in child['devices']:
                    client.set_time_limits_device(child['id'], device['id'], device['limit']['id'], amount + device['limit']['minutes'])
            children = get_members()
            json_data = children
            self.send_response(200)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()
            json_to_pass = json.dumps(json_data)
            self.wfile.write(json_to_pass.encode('utf-8'))
        else:
            self.send_response(500)
            self.send_header(keyword='Content-type', value='application/json')
            self.end_headers()

def get_members():
    children = []
    members = client.get_members()
    for member in members.members:
        if member.role == 'child':
            child = {}
            child['id'] = member.user_id
            child['name'] = member.profile.display_name
            child['image'] = member.profile.profile_image_url
            children.append(child)
    for child in children:
        get_children_time_limits(child)
    return children

def main():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

def get_children_time_limits(child):
    time_limits = client.get_time_limits(child['id'])
    applied_time_limits = time_limits['appliedTimeLimits']
    pprint(applied_time_limits)
    devices = []
    for limit in applied_time_limits:
        device = {}

        device['limit'] = {}
        key = 'currentUsageLimitEntry'
        if 'inactiveCurrentUsageLimitEntry' in limit:
            key = 'inactiveCurrentUsageLimitEntry'
            device['limit']['id'] = limit[key]['id']
            device['limit']['minutes'] = limit[key]['usageQuotaMins']
            device['limit']['state'] = limit[key]['state']
            device['remaining_time'] = 0
            device['spent_time'] = math.ceil(int(limit['currentUsageUsedMillis'])/60000)
        else:
            device['limit']['id'] = limit[key]['id']
            device['limit']['minutes'] = limit[key]['usageQuotaMins']
            device['limit']['state'] = limit[key]['state']
            device['remaining_time'] = limit['currentUsageRemainingMins']
            device['spent_time'] = device['limit']['minutes'] - device['remaining_time']

        device['down_time'] = {}
        key ='todayWindowLimitEntry'
        if 'inactiveTodayWindowLimitEntry' in limit:
            key = 'inactiveTodayWindowLimitEntry'
        device['down_time']['id'] = limit[key]['id']
        device['down_time']['state'] = limit[key]['state']
        device['down_time']['starts_at'] = {'hour': limit[key]['startsAt']['hour'], 'minute': limit[key]['startsAt']['minute']}
        device['down_time']['ends_at'] = {'hour': limit[key]['endsAt']['hour'], 'minute': limit[key]['endsAt']['minute']}
        device['is_locked'] = limit['isLocked']
        device['id'] = limit['deviceId']
        devices.append(device)
    child['devices'] = devices

if __name__ == "__main__":
    main()
