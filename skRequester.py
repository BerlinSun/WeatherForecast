# -*- coding: utf-8 -*-
import hmac, hashlib
import base64
import urllib, urllib2
import json
from datetime import datetime
import socket
import constant, areaParser

def getWeatherInfo(area_dict, start, end, stime):
	weatherinfo_list = [];
	data_type = "observe";
	for area_id in area_dict.keys()[start:end]:
		public_key = constant.fixed_url + "?areaid=" + str(area_id) + "&type=" + data_type + "&date=" + stime + "&appid=" + constant.app_id;
		h = hmac.new(constant.private_key, public_key, hashlib.sha1);
		digest_key = h.digest();
		base64_key = base64.b64encode(digest_key);

		encode_key = urllib.quote_plus(base64_key);
		request_url = constant.fixed_url + "?areaid=" + str(area_id) + "&type=" + data_type + "&date=" + stime + "&appid=" + constant.app_id[:6] + "&key=" + encode_key;

		try:
			response = urllib2.urlopen(request_url, timeout = 10);
		except Exception, e:
			print 'Failed to get the weather info of %s.' % area_dict[area_id];
			if isinstance(e, urllib2.HTTPError):
				print 'Http error: {0}'.format(e.code);
			elif isinstance(e, urllib2.URLError) and isinstance(e.reason, socket.timeout):
				print 'Url error: socket timeout {0}'.format(e.__str__());
			else:
				print 'Misc error: ' + e.__str__();
			continue;

		json_result = json.load(response);
		# print json.dumps(json_result, ensure_ascii=False, indent = 4);

		currtime = datetime.strptime(stime, '%Y%m%d%H%M%S');
		caltime = datetime.strftime(currtime, '%Y-%m-%d');
		weektime = currtime.weekday();
		skinfo = json_result['l'];
		timeinfo = skinfo['l7'];
		temp = datetime.strptime(timeinfo,'%H:%M');
		timeinfo = datetime.strftime(temp, '%H:%M:%S');
		tempinfo = skinfo['l1'];
		huminfo = skinfo['l2'];
		windpowerinfo = constant.wind_power_code[int(skinfo['l3'])];
		winddirectinfo = constant.wind_direct_code[int(skinfo['l4'])];

		print caltime, constant.weeks[weektime], timeinfo, area_dict[area_id], area_id, tempinfo, huminfo, windpowerinfo, winddirectinfo;

if __name__ == '__main__':
	now = datetime.now().strftime('%Y%m%d%H%M%S');
	area_dict = areaParser.getAreaDict();
	getWeatherInfo(area_dict, 0, 1, now);
