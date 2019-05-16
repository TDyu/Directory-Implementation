#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import datetime
import sys
import re
from copy import deepcopy
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from exception import EmptyEnter, EnterNotDigit, EnterNotInRange
from utils import check_input_digit, remove_spaces, parse_json, write_json, quick_sort, pinyin_y_max, pinyin, sorted_dict_by_key_to_list

class Birthday(object):
	"""for Birthday"""
	def __init__(self, year, month, day):
		super(Birthday, self).__init__()
		# set year
		self.year = None
		self.__set_year(year)
		# set month
		self.month = None
		self.__set_month(month)
		# set day
		self.day = None
		self.__set_day(day)

	def __set_year(self, year):
		'''update year'''
		self.year = year

	def get_year(self):
		'''get year'''
		return self.year

	def __set_month(self, month):
		'''update month'''
		self.month = month

	def get_month(self):
		'''get month'''
		return self.month

	def __set_day(self, day):
		'''update day'''
		self.day = day

	def get_day(self):
		'''get day'''
		return self.day
	
	def get_birthday_str(self):
		if self.year != None:
			return self.year + '/' + self.month + '/' + self.day
		else:
			return self.month + '/' + self.day

	def calculate_age(self):
		'''calculate the age
		'''
		birthday_datetime = datetime.date(int(self.year), int(self.month), int(self.day))
		today_datetime = datetime.date.today()
		if (today_datetime.month > birthday_datetime.month):
			next_year = datetime.date(today_datetime.year + 1, birthday_datetime.month, birthday_datetime.day)
		elif (today_datetime.month < birthday_datetime.month):
			next_year = datetime.date(today_datetime.year, today_datetime.month + (birthday_datetime.month - today_datetime.month), birthday_datetime.day)
		elif (today_datetime.month == birthday_datetime.month):
			if (today_datetime.day > birthday_datetime.day):
				next_year = datetime.date(today_datetime.year + 1, birthday_datetime.month, birthday_datetime.day)
			elif (today_datetime.day < birthday_datetime.day):
				next_year = datetime.date(today_datetime.year, birthday_datetime.month, today_datetime.day + (birthday_datetime.day - today_datetime.day))
			elif (today_datetime.day == birthday_datetime.day):
				next_year = 0
		age = today_datetime.year - birthday_datetime.year
		return age

	def __str__(self):
		string = self.get_birthday_str()


class Address(object):
	"""for Address"""
	def __init__(self, region, county, district, detail):
		super(Address, self).__init__()
		self.region = None
		self.__set_region(region)
		self.county = None
		self.__set_county(county)
		self.district = None
		self.__set_district(district)
		self.detail = None
		self.__set_detail(detail)

	def __set_region(self, region):
		'''update region
		
		Arguments:
			region {string} -- region or country of address
		'''
		self.region = region

	def __set_county(self, county):
		'''update county
		
		Arguments:
			county {string} -- county of address
		'''
		self.county = county

	def __set_district(self, district):
		'''update district
		
		Arguments:
			district {string} -- district of address
		'''
		self.district = district

	def __set_detail(self, detail):
		'''update detail
		
		Arguments:
			detail {string} -- the address except of region, contry and district.
		'''
		self.detail = detail

	def get_county(self):
		if self.county != None and self.county != 'x':
			return self.county
		else:
			return None

	def get_address_str(self):
		string = ''
		if self.region != None:
			string += self.region + '/'
		if self.county != None:
			string += self.county + '/'
		if self.district != None:
			string += self.district + '/'
		if self.detail != None:
			string += self.detail
		return string

	def query_postal_code(self):
		'''find the corresponding postal code (format 3)
		'''
		pass


class ContactPerson(object):
	"""single contact person information in a directory"""
	def __init__(self, processed_input_dict):
		'''init the fields

		Arguments:
			processed_input_dict {dict} -- the dict items include of
				time {datetime/string}[0..1] -- key
				name {string}[0..1] -- It cannot be null.
				alias {string}[0,1] -- Another name can be null.
				birthday {Birthday}[0..1] -- Birthday can be null.
				home_phones {string}[0..*] -- It can be null.
				mobile_phones {string}[0..*] -- It can be null.
				company_phones {string}[0..*] -- It can be null.
				address {Address}[0..1] -- Mailing address can be null.
				emails {string}[0..*] -- Emails can be null.
				line_ids {string}[0..*] -- LINE IDs can be null.
				facebook_ids {string}[0..*] -- Facebook IDs can be null.
				note {string}[0..1] -- Note can be null.
		'''
		super(ContactPerson, self).__init__()
		self.time = None
		self.set_time(processed_input_dict['time'])
		# set name
		self.name = None
		self.set_name(processed_input_dict['name'])
		# set alias
		self.alias = None
		self.set_alias(processed_input_dict['alias'])
		# set birthday and constellation
		self.birthday = None
		self.constellation = None
		self.set_birthday(processed_input_dict['birthday'])
		# set home phones list
		# new home phones list at first
		self.home_phones = []
		self.set_home_phones(processed_input_dict['home_phones'])
		# set mobile phones list
		# new mobile phones list at first
		self.mobile_phones = []
		self.set_mobile_phones(processed_input_dict['mobile_phones'])
		# set company phones list
		# new company phones list at first
		self.company_phones = []
		self.set_company_phones(processed_input_dict['company_phones'])
		# set address
		self.address = None
		self.set_address(processed_input_dict['address'])
		# set emails list
		# new emails list at first
		self.emails = []
		self.set_emails(processed_input_dict['emails'])
		# set line_ids list
		# new line_ids list at first
		self.line_ids = []
		self.set_line_ids(processed_input_dict['line_ids'])
		# set facebook_ids list
		# new facebook_ids list at first
		self.facebook_ids = []
		self.set_facebook_ids(processed_input_dict['facebook_ids'])
		# set note
		self.note = ''
		self.set_note(processed_input_dict['note'])

	def set_time(self, time):
		if isinstance(time, str):
			time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
			self.time = time
		else:
			self.time = time

	def set_name(self, name):
		'''update name

		Arguments:
			name {string} -- It cannot be null.
		'''
		self.name = name

	def set_alias(self, alias):
		'''update alias

		Arguments:
			alias {string} -- another name can be null.
		'''
		self.alias = alias

	def set_birthday(self, birthday):
		'''update birthday and constellation
		Arguments:
			birthday {Birthday} -- birthday can be null.
		'''
		self.birthday = birthday
		# set constellation
		if birthday != None:
			self.__set_constellation()

	def __set_constellation(self):
		'''update constellation'''
		constellation_tuple = ('魔羯座', '水瓶座', '雙魚座', '白羊座', '金牛座', '雙子座', '巨蟹座', '獅子座', '處女座', '天秤座', '天蠍座', '射手座')
		date_tuple = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22), (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
		constellation = constellation_tuple[len(list(filter(lambda y : y <= (int(self.birthday.get_month()), int(self.birthday.get_day())), date_tuple))) % 12]
		self.constellation = constellation

	def set_home_phones(self, home_phones):
		'''update home_phones list
		
		Arguments:
			home_phones {list} -- It can be null.
		'''
		if len(home_phones) > 0:
			for home_phone in home_phones:
				self.home_phones.append(home_phone)

	def set_mobile_phones(self, mobile_phones):
		'''update mobile_phones list
		
		Arguments:
			mobile_phones {list} -- It can be null.
		'''
		if len(mobile_phones) > 0:
			for mobile_phone in mobile_phones:
				self.mobile_phones.append(mobile_phone)

	def set_company_phones(self, company_phones):
		'''update company_phones list
		
		Arguments:
			company_phones {list} -- It can be null.
		'''
		if len(company_phones) > 0:
			for company_phone in company_phones:
				self.company_phones.append(company_phone)

	def set_address(self, address):
		'''update address

		Arguments:
			address {Address} -- Address can be null.
		'''
		self.address = address

	def set_emails(self, emails):
		'''update emails list
		
		Arguments:
			emails {list} -- It can be null.
		'''
		if len(emails) > 0:
			for email in emails:
				self.emails.append(email)

	def set_line_ids(self, line_ids):
		'''update line_ids list
		
		Arguments:
			line_ids {list} -- It can be null.
		'''
		if len(line_ids) > 0:
			for line_id in line_ids:
				self.line_ids.append(line_id)

	def set_facebook_ids(self, facebook_ids):
		'''update facebook_ids list
		
		Arguments:
			facebook_ids {list} -- It can be null.
		'''
		if len(facebook_ids) > 0:
			for facebook_id in facebook_ids:
				self.facebook_ids.append(facebook_id)

	def set_note(self, note):
		'''update note
		
		Arguments:
			note {string} -- note can be null.
		'''
		self.note = note

	def get_time_str(self):
		return datetime.datetime.strftime(self.time, '%Y-%m-%d %H:%M:%S.%f')

	def get_time_datetime(self):
		return deepcopy(self.time)

	def get_name(self):
		return self.name

	def get_alias(self):
		if self.alias == '' or self.alias == None:
			return ''
		else:
			return self.alias

	def get_birthday(self):
		return deepcopy(self.birthday)

	def get_birthday_str(self):
		if self.birthday == None:
			return ''
		else:
			return self.birthday.get_birthday_str()

	def get_constellation(self):
		if self.birthday == None:
			return ''
		else:
			return self.constellation

	def get_home_phones(self):
		return self.home_phones

	def get_home_phones_str(self):
		if len(self.home_phones) == 0:
			return ''
		elif len(self.home_phones) == 1:
			return self.home_phones[0]
		else:
			string = '\n'
			for phone in self.home_phones:
				if self.home_phones.index(phone) == len(self.home_phones) - 1:
					string += phone
				else:
					string += phone + '\n'
			return string

	def get_mobile_phones(self):
		return self.mobile_phones

	def get_mobile_phones_str(self):
		if len(self.mobile_phones) == 0:
			return ''
		elif len(self.mobile_phones) == 1:
			return self.mobile_phones[0]
		else:
			string = '\n'
			for phone in self.mobile_phones:
				if self.mobile_phones.index(phone) == len(self.mobile_phones) - 1:
					string += phone
				else:
					string += phone + '\n'
			return string

	def get_company_phones(self):
		return self.company_phones

	def get_company_phones_str(self):
		if len(self.company_phones) == 0:
			return ''
		elif len(self.company_phones) == 1:
			return self.company_phones[0]
		else:
			string = '\n'
			for phone in self.company_phones:
				if self.company_phones.index(phone) == len(self.company_phones) - 1:
					string += phone
				else:
					string += phone + '\n'
			return string

	def get_phones(self):
		return self.get_home_phones() + self.get_mobile_phones() + self.get_company_phones()

	def get_phones_str(self):
		string = self.get_multivalue_list_str('home') + ', ' + self.get_multivalue_list_str('mobile') + ', ' + self.get_multivalue_list_str('company')
		string = remove_spaces(string)
		return string

	def get_address(self):
		if self.address == None:
			return ''
		else:
			return deepcopy(self.address)

	def get_address_str(self):
		if self.address == None:
			return ''
		else:
			return self.address.get_address_str()

	def get_emails(self):
		return self.emails

	def get_emails_str(self):
		if len(self.emails) == 0:
			return ''
		elif len(self.emails) == 1:
			return self.emails[0]
		else:
			string = '\n'
			for email in self.emails:
				if self.emails.index(email) == len(self.emails) - 1:
					string += email
				else:
					string += email + '\n'
			return string

	def get_line_ids(self):
		return self.line_ids

	def get_line_ids_str(self):
		if len(self.line_ids) == 0:
			return ''
		elif len(self.line_ids) == 1:
			return self.line_ids[0]
		else:
			string = '\n'
			for line_id in self.line_ids:
				if self.line_ids.index(line_id) == len(self.line_ids) - 1:
					string += line_id
				else:
					string += line_id + '\n'
			return string

	def get_facebook_ids(self):
		return self.facebook_ids

	def get_facebook_ids_str(self):
		if len(self.facebook_ids) == 0:
			return ''
		elif len(self.facebook_ids) == 1:
			return self.facebook_ids[0]
		else:
			string = '\n'
			for facebook_id in self.facebook_ids:
				if self.facebook_ids.index(facebook_id) == len(self.facebook_ids) - 1:
					string += facebook_id
				else:
					string += facebook_id + '\n'
			return string

	def get_note(self):
		return self.note

	def get_age(self):
		if self.birthday != None:
			return self.birthday.calculate_age()
		else:
			return None

	def get_multivalue_list_str(self, type):
		string = ''
		if type == 'home':
			if len(self.home_phones) == 0:
				return ''
			elif len(self.home_phones) == 1:
				return self.home_phones[0]
			else:
				for phone in self.home_phones:
					if self.home_phones.index(phone) == len(self.home_phones) - 1:
						string += phone
					else:
						string += phone + ','
		elif type == 'mobile':
			if len(self.mobile_phones) == 0:
				return ''
			elif len(self.mobile_phones) == 1:
				return self.mobile_phones[0]
			else:
				for phone in self.mobile_phones:
					if self.mobile_phones.index(phone) == len(self.mobile_phones) - 1:
						string += phone
					else:
						string += phone + ','
		elif type == 'company':
			if len(self.company_phones) == 0:
				return ''
			elif len(self.company_phones) == 1:
				return self.company_phones[0]
			else:
				for phone in self.company_phones:
					if self.company_phones.index(phone) == len(self.company_phones) - 1:
						string += phone
					else:
						string += phone + ','
		elif type == 'email':
			if len(self.emails) == 0:
				return ''
			elif len(self.emails) == 1:
				return self.emails[0]
			else:
				for email in self.emails:
					if self.emails.index(email) == len(self.emails) - 1:
						string += email
					else:
						string += email + ','
				return string
		elif type == 'facebook_id':
			if len(self.facebook_ids) == 0:
				return ''
			elif len(self.facebook_ids) == 1:
				return self.facebook_ids[0]
			else:
				for facebook_id in self.facebook_ids:
					if self.facebook_ids.index(facebook_id) == len(self.facebook_ids) - 1:
						string += facebook_id
					else:
						string += facebook_id + ','
		elif type == 'line_id':
			if len(self.line_ids) == 0:
				return ''
			elif len(self.line_ids) == 1:
				return self.line_ids[0]
			else:
				for line_id in self.line_ids:
					if self.line_ids.index(line_id) == len(self.line_ids) - 1:
						string += line_id
					else:
						string += line_id + ','
		return string

	def __str__(self):
		string = '姓名: ' + self.get_name() + '\n'
		string += '暱稱: ' + self.get_alias() + '\n'
		string += '生日: ' + self.get_birthday_str() + '\n'
		string += '星座: ' + self.get_constellation() + '\n'
		string += '家用電話: ' + self.get_home_phones_str() + '\n'
		string += '手機: ' + self.get_mobile_phones_str() + '\n'
		string += '公司電話: ' + self.get_company_phones_str() + '\n'
		string += '通訊地址: ' + self.get_address_str() + '\n'
		string += 'Email: ' + self.get_emails_str() + '\n'
		string += 'Line ID: ' + self.get_line_ids_str() + '\n'
		string += 'Facebook ID: ' + self.get_facebook_ids_str() + '\n'
		string += '備註: ' + self.get_note() + '\n'
		return string


def contact_compare_by_time(x, y):
	x_datetime = x.get_time_datetime()
	y_datetime = y.get_time_datetime()
	if x_datetime <= y_datetime:
		return True
	else:
		return False

def contact_compare_by_name(x, y):
	x_name = x.get_name()
	y_name = y.get_name()
	if pinyin_y_max(x_name, y_name):
		return True
	else:
		return False

def _sort_by_time(x):
	return x.get_time_datetime()

def _sort_by_name_pinyin(x):
	return pinyin(x.get_name())


class Directory(object):
	"""for Directory"""
	def __init__(self):
		super(Directory, self).__init__()
		# get the contacts data
		self.data_path = os.path.abspath("./").replace('\\', '/') + '/data/contacts.json'
		# new  contact people dict for store
		self.contacts_dict = {}
		# new  contact people list
		self.contacts_list = []
		# new groups dict
		self.groups_dict = {}
		self.__open()

	def __open(self):
		data = parse_json(self.data_path)
		self.contacts_dict = data['contacts']
		self.__build_contact()
		self.groups_dict = data['groups']

	def __build_contact(self):
		if len(self.contacts_dict) != 0:
			for key, value in self.contacts_dict.items():
				# parse
				contact_input = {}
				contact_input['time'] = key
				contact_input['name'] = value['name']
				contact_input['alias'] = value['alias']
				contact_input['birthday'] =  self.__deal_with_birthday(value['birthday'])
				contact_input['home_phones'] = value['home_phones']
				contact_input['mobile_phones'] = value['mobile_phones']
				contact_input['company_phones'] = value['company_phones']
				contact_input['address'] = self.__deal_with_address(value['address'])
				contact_input['emails'] = value['emails']
				contact_input['line_ids'] = value['line_ids']
				contact_input['facebook_ids'] = value['facebook_ids']
				contact_input['note'] = value['note']
				# new contact
				contact = ContactPerson(contact_input)
				self.contacts_list.append(contact)

	def __store_data(self):
		data = {}
		data['contacts'] = self.contacts_dict
		data['groups'] = self.groups_dict
		write_json(self.data_path, data)
	
	def __start_menu(self):
		# flag for that the input need to retry or no
		need_retry = True
		while need_retry:
			print('通訊錄 - 主選單')
			print('1. 聯絡人列表') # bug: 超過3個不能執行快速排序, 選擇年份出不來沒有的狀況, 次單無法停留
			print('2. 搜尋聯絡人')
			print('3. 新增聯絡人')
			print('4. 刪除聯絡人')
			print('5. 分組聯絡人')
			print('6. 修改聯絡資訊')
			print('7. 關閉通訊錄')
			select = input('請輸入預執行的功能代號: ')
			select = remove_spaces(select)
			need_clear = True
			try:
				# check the enter
				check_input_digit(1, 7, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				select = int(select)
				os.system('cls')

				# need to check the data has contact person or no at first 
				# except selected option = 3, 7
				has_contact = True
				if select != 3 and select != 7:
					if len(self.contacts_list) == 0:
						print('===> 目前無聯絡人!\n')
						need_clear = False
						has_contact = False
					else:
						pass
				elif select == 3:
					# pass check, then do not need to retry
					need_clear = False
					self.__insert_contact()
				else:
					# pass check, then do not need to retry
					need_retry = False
					# = exit
					self.__store_data()

				if has_contact and select != 3 and select != 7:
					# pass check, then do not need to retry
					need_retry = False
					# excute the selected option method
					if select == 1:
						need_retry = self.__contacts_show_list()
					elif select == 2:
						need_retry = self.__query()
					elif select == 4:
						need_retry = self.__delete_contact()
					elif select == 5:
						need_retry = self.__group_contact()
					elif select == 6:
						need_retry = self.__modify_contact_info()
			finally:
				if not need_retry:
					print('===關閉通訊錄===')
					sys.exit(0)
				else:
					if need_clear:
						os.system('cls')

	def __contacts_show_list(self):
		# flag for backing main menu or no
		back_main_menu, select = self.__contacts_show_method_menu()
		if back_main_menu:
			return True
		else:
			return False

	def __contacts_show_method_menu(self):
		# flag for that the input need to retry or no
		need_retry = True
		while need_retry:
			print('通訊錄 - 聯絡人列表呈現方式選單')
			print('1. 依加入時間全排序顯示(舊 -> 新)')
			print('2. 依加入時間全排序顯示(新 -> 舊)')
			print('3. 依姓名字首拼音順序全排序顯示(A -> Z)')
			print('4. 依姓名字首拼音倒序全排序顯示(Z -> A)')
			print('5. 依分組顯示')
			print('6. 依生日顯示')
			print('7. 依年齡顯示')
			print('8. 依星座顯示')
			print('9. 依縣市分類顯示')
			print('10. 回主選單')
			print('11. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			try:
				# check the enter
				check_input_digit(1, 11, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					print('===> 聯絡人列表:')
					back = 'pre'
					self.__contacts_show_all_sort(contact_compare_by_time)
					# self.__contacts_show_all_sort(_sort_by_time)
				elif select == 2:
					print('===> 聯絡人列表:')
					back = 'pre'
					self.__contacts_show_all_sort(contact_compare_by_time, reverse=True)
					# self.__contacts_show_all_sort(_sort_by_time, reverse=True)
				elif select == 3:
					print('===> 聯絡人列表:')
					back = 'pre'
					self.__contacts_show_all_sort(contact_compare_by_name)
					# self.__contacts_show_all_sort(_sort_by_name_pinyin)
				elif select == 4:
					print('===> 聯絡人列表:')
					back = 'pre'
					self.__contacts_show_all_sort(contact_compare_by_name, reverse=True)
					# self.__contacts_show_all_sort(_sort_by_name_pinyin, reverse=True)
				elif select == 5:
					back = 'pre'
					self.__contacts_show_group()
				elif select == 6:
					back = self.__contacts_show_birthday()
				elif select == 7:
					back = self.__contacts_show_age()
				elif select == 8:
					back = self.__contacts_show_constellation()
				elif select == 9:
					back = self.__contacts_show_county()
				elif select == 10:
					back = 'main'
				elif select == 11:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					if back == 'pre':
						need_retry = True
					elif back == 'main':
						return True, select
					else:
						return False, select

	def __contacts_show_all_sort(self, compare_func, reverse=False):
		contacts = []
		for contact in self.contacts_list:
			contacts.append(contact)
		contacts = quick_sort(contacts, compare_func)
		# contacts.sort(key=compare_func, reverse=reverse)
		if reverse:
			contacts.reverse()
		i = 1
		for contact in contacts:
			print(str(i) + '.')
			print(contact)
			i += 1

	def __contacts_show_group(self):
		# show menu and get back where
		back, select = self.__contacts_show_group_menu()
		if back:
			return back
		else:
			pass

	def __contacts_show_group_menu(self):
		# flag for that the input need to retry or no
		need_retry = True
		while need_retry:
			print('通訊錄 - 聯絡人列表 - 分組呈現方式選單')
			print('1. 全組別分類顯示')
			print('2. 選擇組別顯示')
			print('3. 回上一層')
			print('4. 回主選單')
			print('5. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			try:
				# check the enter
				check_input_digit(1, 5, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				# pass check, then do not need to retry
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					self.__contacts_show_group_all()
				elif select == 2:
					back = 'pre'
					self.__contacts_show_group_option()
				elif select == 3:
					back = 'pre'
				elif select == 4:
					back = 'main'
				elif select == 5:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					return back, select

	def __group_list(self):
		groups_list = []
		if len(self.groups_dict) == 0:
			groups_no = []
			for contact in self.contacts_list:
				groups_no.append(contact)
			groups_list.append(('未分組', groups_no))
		else:
			has_group_contacts = []
			for key, contacts_time_str_list in self.groups_dict.items():
				for contact_time_str in contacts_time_str_list:
					for contact in self.contacts_list:
						if contact_time_str == contact.get_time_str():
							has_group_contacts.append(contact)
							break
				groups_list.append((key, has_group_contacts))

			no_group_contacts = []
			for contact in self.contacts_list:
				if contact not in has_group_contacts:
					no_group_contacts.append(contact)
			groups_list.append(('未分組', no_group_contacts))
		return groups_list

	def __contacts_show_group_all(self):
		groups_list = self.__group_list()

		i = 1
		for key, contacts in groups_list:
			print('組別 【' + key + '】')
			for contact in contacts:
				print(str(i) + '.')
				print(contact)
				i += 1
		
		return groups_list

	def __groups_option_list(self, groups_name):
		groups_option_list = []
		if len(self.groups_dict) != 0:
			groups_names = []
			for name in self.groups_dict.keys():
				groups_names.append(name)
			if name in groups_names:
				for contact in self.groups_dict[group_name]:
					groups_option_list.append(contact)
		return groups_option_list

	def __contacts_show_group_option(self):
		groups_option_list = []
		if len(self.groups_dict) == 0:
			print('===> 目前尚未有組別!\n')
		else:
			groups_names = []
			print('目前有的組別名:\n')
			for name in self.groups_dict.keys():
				print('【' + name + '】')
				groups_names.append(name)
			group_name = input('請輸入要選擇的組別名: ')
			if group_name not in groups_names:
				print('===> 目前無名為 【' + group_name + '】 的組別')
			else:
				groups_option_list = self.__groups_option_list(group_name)
				print('組別 【' + group_name + '】')
				if len(groups_option_list) == 0:
					print('【無】')
				else:
					i = 1
					for contact in groups_option_list:
						print(str(i) + '.')
						print(contact)
						i += 1

		return groups_option_list
	
	def __contacts_show_birthday(self):
		# show menu and get back where
		back, select = self.__contacts_show_birthday_menu()
		if back:
			return back
		else:
			pass

	def __contacts_show_birthday_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 聯絡人列表 - 生日呈現方式選單')
			print('1. 依年份順序分類全排序顯示')
			print('2. 依年份倒序分類全排序顯示')
			print('3. 選擇年份顯示')
			print('4. 依月份順序分類全排序顯示')
			print('5. 依月份倒序分類全排序顯示')
			print('6. 選擇月份顯示')
			print('7. 依日期(=按年齡)順序全排序顯示')
			print('8. 依日期(=按年齡)倒序全排序顯示')
			print('9. 回上一層')
			print('10. 回主選單')
			print('11. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			try:
				# check the enter
				check_input_digit(1, 11, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				# pass check, then do not need to retry
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					self.__contacts_show_birthday_by_year()
				elif select == 2:
					back = 'pre'
					self.__contacts_show_birthday_by_year(reverse=True)
				elif select == 3:
					back = 'pre'
					self.__contacts_show_birthday_choose_year()
				elif select == 4:
					back = 'pre'
					self.__contacts_show_birthday_by_month()
				elif select == 5:
					back = 'pre'
					self.__contacts_show_birthday_by_month(reverse=True)
				elif select == 6:
					back = 'pre'
					self.__contacts_show_birthday_choose_month()
				elif select == 7:
					back = 'pre'
					self.__contacts_show_by_age()
				elif select == 8:
					back = 'pre'
					self.__contacts_show_by_age(reverse=True)
				elif select == 9:
					back = 'pre'
				elif select == 10:
					back = 'main'
				elif select == 11:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					return back, select

	def __contacts_dict(self, type, key=None):
		contacts_has_dict = {}
		contacts_none_list = []
		for contact in self.contacts_list:
			if type == 'birthday':
				if contact.get_birthday() != None:
					if key == 'year':
						if contact.get_birthday().get_year() != None:
							if contact.get_birthday().get_year() not in contacts_has_dict.keys():
								contacts_has_dict[contact.get_birthday().get_year()] = []
							contacts_has_dict[contact.get_birthday().get_year()].append(contact)
						else:
							contacts_none_list.append(contact)
					elif key == 'month':
						if contact.get_birthday().get_month() != None:
							if contact.get_birthday().get_month() not in contacts_has_dict.keys():
								contacts_has_dict[contact.get_birthday().get_month()] = []
							contacts_has_dict[contact.get_birthday().get_month()].append(contact)
						else:
							contacts_none_list.append(contact)
				else:
					contacts_none_list.append(contact)
			elif type == 'constellation':
				if contact.get_constellation() != None:
					if contact.get_constellation() not in contacts_has_dict.keys():
						contacts_has_dict[contact.get_constellation()] = []
					contacts_has_dict[contact.get_constellation()].append(contact)
				else:
					contacts_none_list.append(contact)
			elif type == 'county':
				if contact.get_address() != None:
					if contact.get_address().get_county() != None:
						if contact.get_address().get_county() not in contacts_has_dict.keys():
							contacts_has_dict[contact.get_address().get_county()] = []
						contacts_has_dict[contact.get_address().get_county()].append(contact)
					else:
						contacts_none_list.append(contact)
				else:
					contacts_none_list.append(contact)
		return contacts_has_dict, contacts_none_list

	def __contacts_show_birthday_by_year(self, reverse=False):
		contacts_has_dict, contacts_none_list = self.__contacts_dict('birthday', 'year')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict, reverse=reverse)
		total_list = contacts_has_dict_sorted_list
		total_list += ('無', contacts_none_list)
		i = 1
		for key, contacts in total_list:
			print(str(key) + ' 年:')
			for contact in contacts:
				print(str(i) + '.')
				print(contact)
				i += 1

	def __contacts_show_birthday_choose_year(self):
		year = input('請輸入欲查找的年份(西元): ')
		year = remove_spaces(year)
		contacts_has_dict, contacts_none_list = self.__contacts_dict('birthday', 'year')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict)
		no = True
		has_list = []
		for key, contacts in contacts_has_dict_sorted_list:
			if year == key:
				no = False
				print('===> 生日年份為 ' + year + ' 的聯絡人有: ')
				i = 1
				for contact in contacts:
					print(str(i) + '.')
					print(contact)
					has_list.append(contact)
					i += 1
				break
			if not no:
				break
		if no:
			print('===> 目前沒有生日年份為 ' + year + ' 的聯絡人!\n')
		return has_list

	def __contacts_show_birthday_by_month(self, reverse=False):
		contacts_has_dict, contacts_none_list = self.__contacts_dict('birthday', 'month')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict, reverse=reverse)
		total_list = contacts_has_dict_sorted_list
		total_list += ('無', contacts_none_list)
		i = 1
		for key, contacts in total_list:
			print(str(key) + ' 月:')
			for contact in contacts:
				print(str(i) + '.')
				print(contact)
				i += 1

	def __contacts_show_birthday_choose_month(self):
		month = input('請輸入欲查找的月份(2位數字格式): ')
		month = remove_spaces(month)
		contacts_has_dict, contacts_none_list = self.__contacts_dict('birthday', 'month')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict)
		no = True
		has_list = []
		for key, contacts in contacts_has_dict_sorted_list:
			if month == key:
				no = False
				print('===> 生日月份為 ' + month + ' 的聯絡人有: ')
				i = 1
				for contact in contacts:
					print(str(i) + '.')
					print(contact)
					has_list.append(contact)
					i += 1
				break
			if not no:
				break
		if no:
			print('===> 目前沒有生日月份為 ' + month + ' 的聯絡人!\n')
		return has_list

	def __contacts_show_age(self):
		# show menu and get back where
		back, select = self.__contacts_show_age_menu()
		if back:
			return back
		else:
			pass

	def __contacts_show_age_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 聯絡人列表 - 年齡呈現方式選單')
			print('1. 年齡順序分類全排序顯示')
			print('2. 年齡倒序分類全排序顯示')
			print('3. 選擇年齡顯示')
			print('4. 回上一層')
			print('5. 回主選單')
			print('6. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			try:
				# check the enter
				check_input_digit(1, 6, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				# pass check, then do not need to retry
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					self.__contacts_show_by_age()
				elif select == 2:
					back = 'pre'
					self.__contacts_show_by_age(reverse=True)
				elif select == 3:
					back = 'pre'
					self.__contacts_show_choose_age()
				elif select == 4:
					back = 'pre'
				elif select == 5:
					back = 'main'
				elif select == 6:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					return back, select

	def __contacts_age_dict_sorted_to_list(self, reverse=False):
		birthday_has = []
		birthday_none = []
		for contact in self.contacts_list:
			if contact.get_birthday().get_year() != None:
				birthday_has.append(contact)
			else:
				birthday_none.append(contact)
		age_dict = {}
		for contact in birthday_has:
			age = str(contact.get_age())
			if age not in age_dict.keys():
				age_dict[age] = []
			age_dict[age].append(contact)

		age_dict_sorted_to_list = sorted_dict_by_key_to_list(age_dict, reverse=reverse)
		total_list = age_dict_sorted_to_list
		total_list += ('無', birthday_none)
		return total_list

	def __contacts_show_by_age(self, reverse=False):
		total_list = self.__contacts_age_dict_sorted_to_list(reverse=reverse)
		i = 1
		for key, contacts in total_list:
			print(str(key) + ' 歲:')
			for contact in contacts:
				print(str(i) + '.')
				print(contact)
				i += 1

	def __contacts_show_choose_age(self):
		age = input('請輸入欲查找的年齡: ')
		age = remove_spaces(age)
		total_list = self.__contacts_age_dict_sorted_to_list()
		no = True
		has_list = []
		for key, contacts in total_list:
			if age == key:
				no = False
				print('===> 年齡為 ' + age + ' 的聯絡人有: ')
				i = 1
				for contact in contacts:
					print(str(i) + '.')
					print(contact)
					has_list.append(contact)
					i += 1
				break
			if not no:
				break
		if no:
			print('===> 目前沒有年齡為 ' + age + ' 的聯絡人!\n')
		return has_list

	def __contacts_show_constellation(self):
		# show menu and get back where
		back, select = self.__contacts_show_constellation_menu()
		if back:
			return back
		else:
			pass

	def __contacts_show_constellation_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 聯絡人列表 - 星座呈現方式選單')
			print('1. 星座分類全排序顯示')
			print('2. 選擇星座顯示')
			print('3. 回上一層')
			print('4. 回主選單')
			print('5. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			try:
				# check the enter
				check_input_digit(1, 5, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				# pass check, then do not need to retry
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					self.__contacts_show_by_constellation()
				elif select == 2:
					back = 'pre'
					self.__contacts_show_choose_constellation()
				elif select == 3:
					back = 'pre'
				elif select == 4:
					back = 'main'
				elif select == 5:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					return back, select

	def __contacts_show_by_constellation(self):
		contacts_has_dict, contacts_none_list = self.__contacts_dict('constellation')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict)
		total_list = contacts_has_dict_sorted_list
		total_list += ('無', contacts_none_list)
		i = 1
		for key, contacts in total_list:
			print(str(key) + ':')
			for contact in contacts:
				print(str(i) + '.')
				print(contact)
				i += 1

	def __contacts_show_choose_constellation(self):
		constellation = input('請輸入欲查找的星座(格式(繁中輸入): xx座):\nex: 魔羯座, 水瓶座, 雙魚座, 白羊座, 金牛座, 雙子座, 巨蟹座, 獅子座, 處女座, 天秤座, 天蠍座, 射手座\n')
		constellation = remove_spaces(constellation)
		contacts_has_dict, contacts_none_list = self.__contacts_dict('constellation')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict)
		no = True
		has_list = []
		for key, contacts in contacts_has_dict_sorted_list:
			if constellation == key:
				no = False
				print('===> 星座為 ' + constellation + ' 的聯絡人有:\n ')
				i = 1
				for contact in contacts:
					print(str(i) + '.')
					print(contact)
					has_list.append(contact)
					i += 1
				break
			if not no:
				break
		if no:
			print('===> 目前沒有星座為 ' + constellation + ' 的聯絡人!\n')
		return has_list

	def __contacts_show_county(self):
		# show menu and get back where
		back, select = self.__contacts_show_county_menu()
		if back:
			return back
		else:
			pass

	def __contacts_show_county_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 聯絡人列表 - 縣市呈現方式選單')
			print('1. 縣市分類全排序顯示')
			print('2. 選擇縣市顯示')
			print('3. 回上一層')
			print('4. 回主選單')
			print('5. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			try:
				# check the enter
				check_input_digit(1, 5, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				# pass check, then do not need to retry
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					self.__contacts_show_by_county()
				elif select == 2:
					back = 'pre'
					self.__contacts_show_choose_county()
				elif select == 3:
					back = 'pre'
				elif select == 4:
					back = 'main'
				elif select == 5:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					return back, select

	def __contacts_show_by_county(self):
		contacts_has_dict, contacts_none_list = self.__contacts_dict('county')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict)
		total_list = contacts_has_dict_sorted_list
		total_list += ('無', contacts_none_list)
		i = 1
		for key, contacts in total_list:
			print(str(key) + ':')
			for contact in contacts:
				print(str(i) + '.')
				print(contact)
				i += 1

	def __contacts_show_choose_county(self):
		county = input('請輸入欲查找的縣市(繁中輸入全稱): ')
		county = remove_spaces(county)
		contacts_has_dict, contacts_none_list = self.__contacts_dict('county')
		contacts_has_dict_sorted_list = sorted_dict_by_key_to_list(contacts_has_dict)
		no = True
		has_list = []
		for key, contacts in contacts_has_dict_sorted_list:
			if county == key:
				no = False
				print('===> 縣市為 ' + county + ' 的聯絡人有:\n ')
				i = 1
				for contact in contacts:
					print(str(i) + '.')
					print(contact)
					has_list.append(contact)
					i += 1
				break
			if not no:
				break
		if no:
			print('===> 目前沒有縣市為 ' + county + ' 的聯絡人!\n')
		return has_list

	def __query(self):
		# flag for backing main menu or no
		back_main_menu, select = self.__query_menu()
		if back_main_menu:
			return True
		else:
			return False

	def __query_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 搜尋聯絡人 - 搜尋方式選單')
			print('(PS. 除了以下的搜尋方法, 在列表功能中有更多篩選方法, 請多加善用)')
			print('1. 依名稱(姓名/暱稱)(為部分符合搜尋)')
			print('2. 依電話(為部分符合搜尋)')
			print('3. 依生日年份(為完全符合搜尋)')
			print('4. 依生日月份(為完全符合搜尋)')
			print('5. 依星座(為完全符合搜尋)')
			print('6. 依年齡(為完全符合搜尋)')
			print('7. 依縣市(為完全符合搜尋)')
			print('8. 回主選單')
			print('9. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			subject_list = []
			try:
				# check the enter
				check_input_digit(1, 9, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					subject_list = self.__query_name()
				elif select == 2:
					back = 'pre'
					subject_list = self.__query_phone()
				elif select == 3:
					back = 'pre'
					subject_list = self.__contacts_show_birthday_choose_year()
				elif select == 4:
					back = 'pre'
					subject_list = self.__contacts_show_birthday_choose_month()
				elif select == 5:
					back = 'pre'
					subject_list = self.__contacts_show_choose_constellation()
				elif select == 6:
					back = 'pre'
					subject_list = self.__contacts_show_choose_age()
				elif select == 7:
					back = 'pre'
					subject_list = self.__contacts_show_choose_county()
				elif select == 8:
					back = 'main'
				elif select == 9:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					if back == 'pre':
						need_retry = True
					elif back == 'main':
						return True, select
					else:
						return False, select

	def __query_name(self):
		name = input('請輸入要搜尋的名稱: ')
		query_list = []
		has = False
		for contact in self.contacts_list:
			if name in contact.get_name():
				query_list.append(contact)
				has = True
			if contact.get_alias() != None and name in contact.get_alias():
				query_list.append(contact)
				has = True
		if has:
			print('===> 姓名或暱稱含有 "' + name + '" 的聯絡人:')
			i = 1
			for contact in query_list:
				print(str(i) + '.')
				print(contact)
				i += 1
		else:
			print('===> 目前沒有姓名或暱稱含有 "' + name + '" 的聯絡人!')
		return query_list

	def __query_phone(self):
		phone = input('請輸入要搜尋的電話: ')
		query_list = []
		has = False
		for contact in self.contacts_list:
			if phone in contact.get_phones_str():
				query_list.append(contact)
				has = True
		if has:
			print('===> 擁有電話號碼 "' + phone + '" 的聯絡人:')
			i = 1
			for contact in query_list:
				print(str(i) + '.')
				print(contact)
				i += 1
		else:
			print('===> 目前沒有擁有電話號碼 "' + phone + '" 的聯絡人!')
		return query_list

	def __insert_contact(self):
		# input at first
		input_dict = self.__insert_base_input()
		# then process the input to format or type ContactPerson need
		processed_input_dict = self.__insert_input_process(input_dict)
		# build the ContactPerson at last
		new_contact = self.__insert_build(processed_input_dict)
		if new_contact:
			os.system('cls')
			print('===> 新聯絡人:\n')
			print(new_contact)
			print('===> 新增成功!\n')
		else:
			pass

	def __insert_build(self, processed_input_dict):
		new_contact = ContactPerson(processed_input_dict)
		self.contacts_list.append(new_contact)

		new_contact_dict = {}
		new_contact_dict['name'] = new_contact.get_name()
		new_contact_dict['alias'] = new_contact.get_alias()
		new_contact_dict['birthday'] = new_contact.get_birthday_str()
		new_contact_dict['constellation'] = new_contact.get_constellation()
		new_contact_dict['home_phones'] = new_contact.get_home_phones()
		new_contact_dict['mobile_phones'] = new_contact.get_mobile_phones()
		new_contact_dict['company_phones'] = new_contact.get_company_phones()
		new_contact_dict['address'] = new_contact.get_address_str()
		new_contact_dict['emails'] = new_contact.get_emails()
		new_contact_dict['line_ids'] = new_contact.get_line_ids()
		new_contact_dict['facebook_ids'] = new_contact.get_facebook_ids()
		new_contact_dict['note'] = new_contact.get_note()
		self.contacts_dict[new_contact.get_time_str()] = new_contact_dict
		self.__store_data()
		return new_contact

	def __insert_base_input(self):
		'''for user input
		just the name is necessary item
		
		Returns:
			dict -- unprocessed user input
		'''
		input_dict = {}

		# the name is necessary items
		# so, if user did not input the name or input all empty, 
		# then user need to input again
		no_name = True
		while no_name:
			print('通訊錄 - 新增聯絡人 (以下資料均將自動移除空格, 不合乎格式者視同為填)')
			input_dict['name'] = input('請輸入聯絡人 名稱 (必填): \n')
			input_dict['name'] = remove_spaces(input_dict['name'])
			if not input_dict['name']:
				os.system('cls')
				print('===> 聯絡人名稱不得為空!\n')
			else:
				no_name = False

		# other item is optional
		input_dict['alias'] = input('\n請輸入聯絡人 暱稱 (選填):\n')
		input_dict['birthday'] = input('\n請輸入聯絡人 生日 (選填)\n(格式(以下兩種挑一種): 年/月/日: xxxx/xx/xx or 月/日: xx/xx)\n(不合常理的日期將視為無效):\n')
		input_dict['home_phones'] = input('\n請輸入聯絡人 家用電話 (選填) (若多組則請以逗號分開):\n')
		input_dict['mobile_phones'] = input('\n請輸入聯絡人 手機 (選填) (若多組則請以逗號分開):\n')
		input_dict['company_phones'] = input('\n請輸入聯絡人 公司電話 (選填) (若多組則請以逗號分開):\n')
		input_dict['address'] = input('\n請輸入聯絡人 地址 (選填)\n(格式: 國家地區/縣市/鄉區鎮/其他) (若有不填的欄位請輸入"x", 全不填則留空):\n')
		input_dict['emails'] = input('\n請輸入聯絡人 email (選填) (若多組則請以逗號分開):\n')
		input_dict['line_ids'] = input('\n請輸入聯絡人 Line ID (選填) (若多組則請以逗號分開):\n')
		input_dict['facebook_ids'] = input('\n請輸入聯絡人 Facebook ID (選填) (若多組則請以逗號分開):\n')
		input_dict['note'] = input('\n請輸入備註 (選填) (200字為限, 超過將自動裁掉):\n')

		return input_dict

	def __insert_input_process(self, input_dict):
		'''process the user input string to be ContactPerson needed format or type
		
		Arguments:
			input_dict {dict} -- unprocessed input string dict
		
		Returns:
			dict -- processed input dict
		'''
		unprocessed_input_dict = {}
		# time part
		unprocessed_input_dict['time'] = datetime.datetime.now()
		# name part
		unprocessed_input_dict['name'] = input_dict['name']
		unprocessed_input_dict['alias'] = remove_spaces(input_dict['alias'])
		# birthday part
		unprocessed_input_dict['birthday'] = self.__deal_with_birthday(input_dict['birthday'])
		# phone part
		remove_rule_phone = '\D'
		unprocessed_input_dict['home_phones'] = self.__deal_with_multivalue_input_str(input_dict['home_phones'], remove_rule_phone)
		unprocessed_input_dict['mobile_phones'] = self.__deal_with_multivalue_input_str(input_dict['mobile_phones'], remove_rule_phone)
		unprocessed_input_dict['company_phones'] = self.__deal_with_multivalue_input_str(input_dict['company_phones'], remove_rule_phone)
		# address part
		unprocessed_input_dict['address'] = self.__deal_with_address(input_dict['address'])
		# other communication part
		remove_rule_string_value = '[’!"#$%&\'()*+,-/:;<=>?[\\]^`{|}~]+'
		unprocessed_input_dict['emails'] = self.__deal_with_multivalue_input_str(input_dict['emails'], remove_rule_string_value)
		remove_rule_string_value = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~]+'
		unprocessed_input_dict['line_ids'] = self.__deal_with_multivalue_input_str(input_dict['line_ids'], remove_rule_string_value)
		unprocessed_input_dict['facebook_ids'] = self.__deal_with_multivalue_input_str(input_dict['facebook_ids'], remove_rule_string_value)
		# note part
		unprocessed_input_dict['note'] = self.__deal_with_note(input_dict['note'])

		return unprocessed_input_dict

	def __deal_with_birthday(self, birthday):
		processed_birthday = None
		birthday = remove_spaces(birthday)
		if not birthday:
			pass
		else:
			birthday = birthday.replace('／', '/')
			splited_birthday = birthday.split('/')
			if len(splited_birthday) == 2:
				month = re.sub('\D', '', splited_birthday[0])
				if not month:
					pass
				else:
					month_int = int(month)
					if month_int > 12 or month_int < 1:
						pass
					else:
						day = re.sub('\D', '', splited_birthday[1])
						if not day:
							pass
						else:
							day_int = int(day)
							if month_int == 2:
								if day_int > 29 or day_int < 1:
									pass
								else:
									processed_birthday = Birthday(None, month, day)
							else:
								big_months = [1, 3, 5, 7, 8, 10, 12]
								if month_int in big_months:
									if day_int > 31 or day_int < 1:
										pass
									else:
										processed_birthday = Birthday(None, month, day)
								else:
									if day_int > 30 or day_int < 1:
										pass
									else:
										processed_birthday = Birthday(None, month, day)
			elif len(splited_birthday) == 3:
				year = re.sub('\D', '', splited_birthday[0])
				if not year:
					pass
				else:
					year_int = int(year)
					current_year = datetime.date.today().year
					if year_int > current_year:
						pass
					else:
						month = re.sub('\D', '', splited_birthday[1])
						if not month:
							pass
						else:
							month_int = int(month)
							if month_int < 1 or month_int > 12:
								pass
							else:
								day = re.sub('\D', '', splited_birthday[2])
								if not day:
									pass
								else:
									day_int = int(day)
									big_months = [1, 3, 5, 7, 8, 10, 12]
									is_leap_year = False
									if year_int % 4 == 0:
										if year_int % 100 == 0:
											if year_int % 400 == 0:
												is_leap_year = True
										else:
											is_leap_year = True
									if is_leap_year:
										if month_int == 2:
											if day_int > 29 or day_int < 1:
												pass
											else:
												processed_birthday = Birthday(year, month, day)
										else:
											
											if month_int in big_months:
												if day_int > 31 or day_int < 1:
													pass
												else:
													processed_birthday = Birthday(year, month, day)
											else:
												if day_int > 30 or day_int < 1:
													pass
												else:
													processed_birthday = Birthday(year, month, day)
									else:
										if month_int == 2:
											if day_int > 28 or day_int < 1:
												pass
											else:
												processed_birthday = Birthday(year, month, day)
										else:
											
											if month_int in big_months:
												if day_int > 31 or day_int < 1:
													pass
												else:
													processed_birthday = Birthday(year, month, day)
											else:
												if day_int > 30 or day_int < 1:
													pass
												else:
													processed_birthday = Birthday(year, month, day)

		return processed_birthday

	def __deal_with_address(self, address):
		processed_address = None
		address = remove_spaces(address)
		if not address:
			pass
		else:
			address = address.replace('／', '/')
			splited_address = address.split('/')
			if len(splited_address) != 4:
				pass
			else:
				processed = []
				for string in splited_address:
					if string == 'x':
						processed.append(None)
					else:
						processed.append(string)
				processed_address = Address(processed[0], processed[1], processed[2], processed[3])

		return processed_address

	def __deal_with_multivalue_input_str(self, values, rule):
		# if the length of values is 0, then the values list is empty.
		# or, replace '，' by ',' and split values with ','
		# remove all not rule character from each value string,
		# and then add to values_list
		values_list = []
		if not values:
			pass
		else:
			removed_value = remove_spaces(values)
			values = values.replace('，', ',')
			splited_values = values.split(',')
			for value in splited_values:
				if not value:
					pass
				else:
					value = re.sub(rule, '', value)
					values_list.append(value)
		return values_list

	def __deal_with_note(self, note):
		# if length of not > 200, then capture from 0 to 199
		if not note:
			note = ''
		else:
			if len(note) > 200:
				note = note[:199]
		return note

	def __delete_contact(self):
		# flag for backing main menu or no
		back_main_menu, select = self.__delete_menu()
		if back_main_menu:
			return True
		else:
			return False

	def __delete_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 刪除聯絡人')
			print('請先選擇一種搜查方法, 再選擇其搜尋結果的編號做刪除')
			print('1. 依名稱(姓名/暱稱)(為部分符合搜尋)')
			print('2. 依電話(為部分符合搜尋)')
			print('3. 依生日年份(為完全符合搜尋)')
			print('4. 依生日月份(為完全符合搜尋)')
			print('5. 依星座(為完全符合搜尋)')
			print('6. 依年齡(為完全符合搜尋)')
			print('7. 依縣市(為完全符合搜尋)')
			print('8. 回主選單')
			print('9. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			subject_list = []
			try:
				# check the enter
				check_input_digit(1, 9, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					subject_list = self.__query_name()
				elif select == 2:
					back = 'pre'
					subject_list = self.__query_phone()
				elif select == 3:
					back = 'pre'
					subject_list = self.__contacts_show_birthday_choose_year()
				elif select == 4:
					back = 'pre'
					subject_list = self.__contacts_show_birthday_choose_month()
				elif select == 5:
					back = 'pre'
					subject_list = self.__contacts_show_choose_constellation()
				elif select == 6:
					back = 'pre'
					subject_list = self.__contacts_show_choose_age()
				elif select == 7:
					back = 'pre'
					subject_list = self.__contacts_show_choose_county()
				elif select == 8:
					back = 'main'
				elif select == 9:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					if back == 'pre':
						if len(subject_list) != 0:
							if self.__delete_someone(subject_list):
								return True, select
						need_retry = True
					elif back == 'main':
						return True, select
					else:
						return False, select

	def __delete_someone(self, subject_list):
		need_retry = True
		while need_retry:
			select = input('請選擇以上搜尋結果之欲刪除聯絡人的編號(輸入0為回主選單): ')
			select = remove_spaces(select)
			try:
				# check the enter
				check_input_digit(0, len(subject_list), select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				
				need_retry = False
				if select == '0':
					return True
				else:
					index = int(select) - 1
					self.contacts_list.remove(subject_list[index])
					del self.contacts_dict[subject_list[index].get_time_str()]
					self.__store_data()
					print('===> 已刪除聯絡人:')
					print(subject_list[index])
					return False

	def __group_contact(self):
		# flag for backing main menu or no
		back_main_menu, select = self.__group_menu()
		if back_main_menu:
			return True
		else:
			return False

	def __group_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 分組聯絡人')
			print('1. 依分組列出目前聯絡人')
			print('2. 選擇組別列出聯絡人')
			print('3. 添加聯絡人到組別')
			print('4. 將聯絡人移出組別')
			print('5. 新增分組')
			print('6. 刪除分組')
			print('7. 回主選單')
			print('8. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			try:
				# check the enter
				check_input_digit(1, 8, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					self.__contacts_show_group_all()
				elif select == 2:
					back = 'pre'
					self.__contacts_show_group_option()
				elif select == 3:
					back = 'pre'
					self.__group_add_member()
				elif select == 4:
					back = 'pre'
					self.__group_remove_member()
				elif select == 5:
					back = 'pre'
					self.__group_add()
				elif select == 6:
					back = 'pre'
					self.__group_delete()
				elif select == 7:
					back = 'main'
				elif select == 8:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					if back == 'pre':
						need_retry = True
					elif back == 'main':
						return True, select
					else:
						return False, select

	def __group_add_member(self):
		if len(self.groups_dict) == 0:
			print('===> 目前尚未有組別!\n')
			return
		else:
			print('===> 目前組別情況:')
			groups_list = self.__contacts_show_group_all()
			groups_names = []
			for name in self.groups_dict.keys():
				groups_names.append(name)
			group_name = input('請輸入要添加成員的組別名: ')
			if group_name not in groups_names:
				print('===> 目前無名為 【' + group_name + '】 的組別')
				return
			else:
				print('===> 目前聯絡人:')
				i = 1
				for contact in self.contacts_list:
					print(str(i) + '.')
					print(contact)
					i += 1
				need_retry = True
				while need_retry:
					select = input('請輸入要加入此組別的聯絡人(根據以上序號)(輸入0為放棄添加): ')
					try:
						# check the enter
						check_input_digit(0, len(self.contacts_list), select)
					except EmptyEnter as e:
						print(e.message)
					except EnterNotDigit as e:
						print(e.message)
					except EnterNotInRange as e:
						print(e.message)
					else:
						need_retry = False
						if select == '0':
							return
						else:
							index = int(select) - 1
							subject_contact = self.contacts_list[index]
							self.groups_dict[group_name].append(subject_contact.get_time_str())
							self.__store_data()
							print('===> 添加成功!\n')
							return

	def __group_remove_member(self):
		if len(self.groups_dict) == 0:
			print('===> 目前尚未有組別!\n')
			return
		else:
			print('===> 目前組別情況:')
			groups_list = self.__contacts_show_group_all()
			groups_names = []
			for name in self.groups_dict.keys():
				groups_names.append(name)
			group_name = input('請輸入要移除成員的組別名: ')
			if group_name not in groups_names:
				print('===> 目前無名為 【' + group_name + '】 的組別')
				return
			else:
				print('===> 此組別目前聯絡人:')
				groups_option_list = self.__groups_option_list(group_name)
				if len(groups_option_list) == 0:
					print('【無】')
				else:
					i = 1
					for contact in groups_option_list:
						print(str(i) + '.')
						print(contact)
						i += 1
				need_retry = True
				while need_retry:
					select = input('請輸入要移出此組別的聯絡人(根據以上序號)(輸入0為放棄移除): ')
					try:
						# check the enter
						check_input_digit(0, len(groups_option_list), select)
					except EmptyEnter as e:
						print(e.message)
					except EnterNotDigit as e:
						print(e.message)
					except EnterNotInRange as e:
						print(e.message)
					else:
						need_retry = False
						if select == '0':
							return
						else:
							index = int(select) - 1
							subject_contact = groups_option_list[index]
							self.groups_dict[group_name].remove(subject_contact.get_time_str())
							self.__store_data()
							print('===> 移除成功!\n')
							return

	def __group_add(self):
		name = input('請輸入要加入的組別名: ')
		if name in self.groups_dict.keys():
			print('===> 此組別名已經存在!\n')
			return
		else:
			self.groups_dict[name] = []
			self.__store_data()
			print('===> 新增組別 【' + name + '】 成功!\n')

	def __group_delete(self):
		name = input('請輸入要刪除的組別名: ')
		if name in self.groups_dict.keys():
			del self.groups_dict[name]
			self.__store_data()
			print('===> 刪除組別 【' + name + '】 成功!n')
			return
		else:
			print('===> 此組別名未存在!\n')
			return

	def __modify_contact_info(self):
		# flag for backing main menu or no
		back_main_menu, select = self.__modify_menu()
		if back_main_menu:
			return True
		else:
			return False

	def __modify_menu(self):
		need_retry = True
		while need_retry:
			print('通訊錄 - 修改聯絡人資訊')
			print('請先選擇一種搜查方法, 再選擇其搜尋結果的編號做修改')
			print('1. 依名稱(姓名/暱稱)(為部分符合搜尋)')
			print('2. 依電話(為部分符合搜尋)')
			print('3. 依生日年份(為完全符合搜尋)')
			print('4. 依生日月份(為完全符合搜尋)')
			print('5. 依星座(為完全符合搜尋)')
			print('6. 依年齡(為完全符合搜尋)')
			print('7. 依縣市(為完全符合搜尋)')
			print('8. 回主選單')
			print('9. 關閉通訊錄')
			select = input('請選擇選項: ')
			select = remove_spaces(select)
			# back where
			back = None
			subject_list = []
			try:
				# check the enter
				check_input_digit(1, 9, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				need_retry = False
				select = int(select)
				os.system('cls')
				# excute the selected option method
				if select == 1:
					back = 'pre'
					subject_list = self.__query_name()
				elif select == 2:
					back = 'pre'
					subject_list = self.__query_phone()
				elif select == 3:
					back = 'pre'
					subject_list = self.__contacts_show_birthday_choose_year()
				elif select == 4:
					back = 'pre'
					subject_list = self.__contacts_show_birthday_choose_month()
				elif select == 5:
					back = 'pre'
					subject_list = self.__contacts_show_choose_constellation()
				elif select == 6:
					back = 'pre'
					subject_list = self.__contacts_show_choose_age()
				elif select == 7:
					back = 'pre'
					subject_list = self.__contacts_show_choose_county()
				elif select == 8:
					back = 'main'
				elif select == 9:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					if back == 'pre':
						if len(subject_list) != 0:
							os.system('cls')
							if self.__modify_someone(subject_list):
								return True, select
						need_retry = True
					elif back == 'main':
						return True, select
					else:
						return False, select

	def __modify_someone(self, subject_list):
		need_retry = True
		while need_retry:
			select = input('請選擇以上搜尋結果之欲修改聯絡人的編號(輸入0為回主選單): ')
			select = remove_spaces(select)
			try:
				# check the enter
				check_input_digit(0, len(subject_list), select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				need_retry = False
				if select == '0':
					return True
				else:
					index = int(select) - 1
					subject_contact = subject_list[index]
					if self.__modify_something(subject_contact):
						return True
					else:
						return False

	def __modify_something(self, subject_contact):
		need_retry = True
		while need_retry:
			print('1. 姓名')
			print('2. 暱稱')
			print('3. 生日(星座與年齡會隨之更改)')
			print('4. 家用電話')
			print('5. 手機')
			print('6. 公司電話')
			print('7. 通訊地址')
			print('8. Email')
			print('9. Line ID')
			print('10. Facebook ID')
			print('11. 備註')
			print('12. 回主選單')
			select = input('請選擇要修改的資訊: ')
			select = remove_spaces(select)
			try:
				# check the enter
				check_input_digit(1, 12, select)
			except EmptyEnter as e:
				print(e.message)
			except EnterNotDigit as e:
				print(e.message)
			except EnterNotInRange as e:
				print(e.message)
			else:
				select = int(select)
				need_retry = False
				os.system('cls')
				if select == 1:
					no_name = True
					name = None
					while no_name:
						name = input('請輸入聯絡人 名稱 (必填): \n')
						name = remove_spaces(name)
						if not name:
							os.system('cls')
							print('===> 聯絡人名稱不得為空!\n')
						else:
							no_name = False
					subject_contact.set_name(name)
					ori_name = self.contacts_dict[subject_contact.get_time_str()]['name']
					self.contacts_dict[subject_contact.get_time_str()]['name'] = name
					os.system('cls')
					print('===> 聯絡人姓名 "' + ori_name + '" 已改為 "' + name + '"\n')
				elif select == 2:
					alias = None
					alias = input('請輸入聯絡人 暱稱 (選填): \n')
					alias = remove_spaces(alias)
					subject_contact.set_alias(alias)
					ori_alias = self.contacts_dict[subject_contact.get_time_str()]['alias']
					self.contacts_dict[subject_contact.get_time_str()]['alias'] = alias
					os.system('cls')
					print('===> 聯絡人暱稱 "' + ori_alias + '" 已改為 "' + alias + '"\n')
				elif select == 3:
					birthday = None
					birthday = input('\n請輸入聯絡人 生日 (選填)\n(格式(以下兩種挑一種): 年/月/日: xxxx/xx/xx or 月/日: xx/xx)\n(不合常理的日期將視為無效):\n')
					birthday = self.__deal_with_birthday(birthday)
					subject_contact.set_birthday(birthday)
					ori_birthday = self.contacts_dict[subject_contact.get_time_str()]['birthday']
					self.contacts_dict[subject_contact.get_time_str()]['birthday'] = subject_contact.get_birthday_str()
					self.contacts_dict[subject_contact.get_time_str()]['constellation'] = subject_contact.get_constellation()
					os.system('cls')
					print('===> 聯絡人生日 "' + ori_birthday + '" 已改為 "' + subject_contact.get_birthday_str() + '"\n')
				elif select == 4:
					home_phones = None
					home_phones = input('\n請輸入聯絡人 家用電話 (選填) (若多組則請以逗號分開):\n')
					remove_rule_phone = '\D'
					home_phones = self.__deal_with_multivalue_input_str(home_phones, remove_rule_phone)
					subject_contact.set_home_phones(home_phones)
					ori_home_phones = self.contacts_dict[subject_contact.get_time_str()]['home_phones']
					self.contacts_dict[subject_contact.get_time_str()]['home_phones'] = subject_contact.get_home_phones()
					os.system('cls')
					print('===> 聯絡人家用電話\n"' + ori_home_phones + '"\n\n已改為\n\n"' + subject_contact.get_multivalue_list_str('home') + '"\n')
				elif select == 5:
					mobile_phones = None
					mobile_phones = input('\n請輸入聯絡人 手機 (選填) (若多組則請以逗號分開):\n')
					remove_rule_phone = '\D'
					mobile_phones = self.__deal_with_multivalue_input_str(mobile_phones, remove_rule_phone)
					subject_contact.set_mobile_phones(mobile_phones)
					ori_mobile_phones = self.contacts_dict[subject_contact.get_time_str()]['mobile_phones']
					self.contacts_dict[subject_contact.get_time_str()]['mobile_phones'] = subject_contact.get_mobile_phones()
					os.system('cls')
					print('===> 聯絡人手機\n"' + ori_mobile_phones + '"\n\n已改為\n\n"' + subject_contact.get_multivalue_list_str('mobile') + '"\n')
				elif select == 6:
					company_phones = None
					company_phones = input('\n請輸入聯絡人 公司電話 (選填) (若多組則請以逗號分開):\n')
					remove_rule_phone = '\D'
					company_phones = self.__deal_with_multivalue_input_str(company_phones, remove_rule_phone)
					subject_contact.set_company_phones(company_phones)
					ori_company_phones = self.contacts_dict[subject_contact.get_time_str()]['company_phones']
					self.contacts_dict[subject_contact.get_time_str()]['company_phones'] = subject_contact.get_company_phones()
					os.system('cls')
					print('===> 聯絡人公司電話\n"' + ori_company_phones + '"\n\n已改為\n\n"' + subject_contact.get_multivalue_list_str('company') + '"\n')
				elif select == 7:
					address = None
					address = input('\n請輸入聯絡人 地址 (選填)\n(格式: 國家地區/縣市/鄉區鎮/其他) (若有不填的欄位請輸入"x"):\n')
					address = self.__deal_with_address(address)
					subject_contact.set_address(address)
					ori_address = self.contacts_dict[subject_contact.get_time_str()]['address']
					self.contacts_dict[subject_contact.get_time_str()]['address'] = subject_contact.get_address_str()
					os.system('cls')
					print('===> 聯絡人地址\n"' + ori_address + '"\n\n已改為\n\n"' + subject_contact.get_address_str() + '"\n')
				elif select == 8:
					emails = None
					emails = input('\n請輸入聯絡人 Email (選填) (若多組則請以逗號分開):\n')
					removremove_rule_string_value = '[’!"#$%&\'()*+,-/:;<=>?[\\]^`{|}~]+'
					emails = self.__deal_with_multivalue_input_str(emails, removremove_rule_string_value)
					subject_contact.set_emails(emails)
					ori_emails = self.contacts_dict[subject_contact.get_time_str()]['emails']
					self.contacts_dict[subject_contact.get_time_str()]['emails'] = subject_contact.get_emails()
					os.system('cls')
					print('===> 聯絡人Email\n"' + ori_emails + '"\n\n已改為\n\n"' + subject_contact.get_multivalue_list_str('email') + '"\n')
				elif select == 9:
					line_ids = None
					line_ids = input('\n請輸入聯絡人 Line ID (選填) (若多組則請以逗號分開):\n')
					remove_rule_string_value = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~]+'
					line_ids = self.__deal_with_multivalue_input_str(line_ids, removremove_rule_string_value)
					subject_contact.set_line_ids(line_ids)
					ori_line_ids = self.contacts_dict[subject_contact.get_time_str()]['line_ids']
					self.contacts_dict[subject_contact.get_time_str()]['line_ids'] = subject_contact.get_line_ids()
					os.system('cls')
					print('===> 聯絡人Line ID\n"' + ori_line_ids + '"\n\n已改為\n\n"' + subject_contact.get_multivalue_list_str('line_id') + '"\n')
				elif select == 10:
					facebook_ids = None
					facebook_ids = input('\n請輸入聯絡人 Facebook ID (選填) (若多組則請以逗號分開):\n')
					remove_rule_string_value = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~]+'
					facebook_ids = self.__deal_with_multivalue_input_str(facebook_ids, removremove_rule_string_value)
					subject_contact.set_facebook_ids(facebook_ids)
					ori_facebook_ids = self.contacts_dict[subject_contact.get_time_str()]['facebook_ids']
					self.contacts_dict[subject_contact.get_time_str()]['facebook_ids'] = subject_contact.get_facebook_ids()
					os.system('cls')
					print('===> 聯絡人Facebook ID\n"' + ori_facebook_ids + '"\n\n已改為\n\n"' + subject_contact.get_multivalue_list_str('facebook_id') + '"\n')
				elif select == 11:
					note = None
					note = input('\n請輸入備註 (選填) (200字為限, 超過將自動裁掉):\n')
					note = self.__deal_with_note(note)
					subject_contact.set_note(note)
					ori_note = self.contacts_dict[subject_contact.get_time_str()]['note']
					self.contacts_dict[subject_contact.get_time_str()]['note'] = note
					os.system('cls')
					print('===> 聯絡人備註\n"' + ori_note + '"\n\n已改為\n\n"' + note + '"\n')
				elif select == 12:
					pass
			finally:
				if need_retry:
					os.system('cls')
				else:
					self.__store_data()
					return True

	def __call__(self):
		self.__start_menu()

# if __name__ == '__main__':
