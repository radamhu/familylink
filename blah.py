import sys
sys.path.insert(0, './src/')
from pprint import pprint
import math
from familylink import FamilyLink
import logging.config


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
client = FamilyLink(browser="txt")

def main():
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
    pprint(children)
    for child in children:
        for device in child['devices']:
            client.enable_time_limits_device(child['id'], device['id'], device['limit']['id'], device['limit']['minutes'])
            # client.turn_on_downtime_device(child['id'],
            #                                 device['id'],
            #                                 device['down_time']['starts_at']['hour'],
            #                                 device['down_time']['starts_at']['minute'],
            #                                 device['down_time']['ends_at']['hour'],
            #                                 device['down_time']['ends_at']['minute'],
            #                                 device['down_time']['id'])
    for child in children:
        get_children_time_limits(child)
    pprint(children)

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

        device['id'] = limit['deviceId']
        devices.append(device)
        child['devices'] = devices

if __name__ == "__main__":
    main()
