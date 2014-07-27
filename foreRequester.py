# -*- coding: utf-8 -*-
'''
Author: Berlin
E-Mail: bolinsun@163.com
'''
import hmac, hashlib
import base64
import urllib, urllib2
import json
from datetime import datetime
import socket
import constant

def getWeatherInfo(index, area_dict, start, end, stime):
	weatherinfo_list = [];
	data_type = "forecast3d";
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
		weather_info = json_result['f'];
		
		forecast_time = weather_info['f0'];
		temp = datetime.strptime(forecast_time,'%Y%m%d%H%M%S');
		forecast_time = datetime.strftime(temp,'%Y-%m-%d %H:%M:%S');
		basicinfo = [];
		basicinfo.append(forecast_time);
		basicinfo.append(area_dict[area_id]);
		basicinfo.append(str(area_id));
		
		weatherinfo = [];
		weatherinfo.append((',').join(basicinfo[:]));
		
		weather_items = weather_info['f1'];
		for day in range(3):
			day_info = weather_items[day];
			
			dayweatherinfo = [];
			if temp.hour == 18 and day == 0:
				pass
			else:
				dayweatherinfo.append(constant.weather_code[day_info['fa']]);
				dayweatherinfo.append(constant.wind_direct_code[int(day_info['fe'])]);
				dayweatherinfo.append(constant.wind_power_code[int(day_info['fg'])]);
				dayweatherinfo.append(day_info['fc']);
				weatherinfo.append((',').join(dayweatherinfo[:]));
			
			nightweatherinfo = [];
			nightweatherinfo.append(constant.weather_code[day_info['fb']]);
			nightweatherinfo.append(constant.wind_direct_code[int(day_info['ff'])]);
			nightweatherinfo.append(constant.wind_power_code[int(day_info['fh'])]);
			nightweatherinfo.append(day_info['fd']);
			weatherinfo.append((',').join(nightweatherinfo[:]));
		
		weatherinfo_list.append(weatherinfo);
	
	filename = 'gn_360_' + stime + '.part.' + str(index);
	fp = open(filename, 'w');
	for weatherinfo in weatherinfo_list:
		info = ('#').join(weatherinfo[:]);
		fp.write(info.encode('utf8'));
		fp.write('\n');
		fp.flush();
		
	fp.close();