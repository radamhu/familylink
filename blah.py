import sys
sys.path.insert(0, './src/')
from pprint import pprint

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
        client.set_time_limits(child['id'],
                               child['first_device']['id'],
                               child['first_device']['limit']['id'],
                               child['first_device']['limit']['minutes'] + 5)
    for child in children:
        get_children_time_limits(child)
    pprint(children)

def get_children_time_limits(child):
    time_limits = client.get_time_limits(child['id'])
    applied_time_limits = time_limits['appliedTimeLimits']
    devices = []
    for limit in applied_time_limits:
        device = {}
        device['limit'] = {}
        device['down_time'] = {}
        device['limit']['id'] = limit['currentUsageLimitEntry']['id']
        device['limit']['minutes'] = limit['currentUsageLimitEntry']['usageQuotaMins']
        device['limit']['state'] = limit['currentUsageLimitEntry']['state']
        device['down_time']['id'] = limit['todayWindowLimitEntry']['id']
        device['down_time']['state'] = limit['todayWindowLimitEntry']['state']
        device['down_time']['start_at'] = {'hour': limit['todayWindowLimitEntry']['startsAt']['hour'], 'minute': limit['todayWindowLimitEntry']['startsAt']['minute']}
        device['down_time']['ends_at'] = {'hour': limit['todayWindowLimitEntry']['endsAt']['hour'], 'minute': limit['todayWindowLimitEntry']['endsAt']['minute']}
        device['remaining_time'] = limit['currentUsageRemainingMins']
        device['spent_time'] = device['limit']['minutes'] - device['remaining_time']
        device['id'] = limit['deviceId']
        devices.append(device)
    child['first_device'] = devices[0]

if __name__ == "__main__":
    main()
