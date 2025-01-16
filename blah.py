import sys
sys.path.insert(0, './src/')
from familylink import FamilyLink

child = FamilyLink()
time_limits = child.get_time_limits()
applied_time_limits = time_limits['appliedTimeLimits']
current_limit = None
devices = []

for limit in applied_time_limits:
    print(limit)
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

first_device  = devices[0]
print(first_device)
