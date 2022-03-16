# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/15/12:53 下午

import csv
import os
import json


class CargoDataSource:

	def __init__(self):

		self.covert_data = list()
		self.uniq = dict()
		self.err_msg = list()
		self.data = list()

	# deal with dimensions unit and val
	def deal_dimemsions(self, dimensions, unit):
		cm_find = dimensions.find("cm")
		mm_find = dimensions.find("mm")
		if cm_find == -1 and mm_find == -1:
			return -1, ""
		if cm_find != -1:
			print("dimensions[0: cm_find]:",dimensions[0: cm_find])
			dimensions_val = dimensions[0: cm_find]
			if unit != "" and unit != "cm":
				return -1, ""
			else:
				return dimensions_val, "cm"
		if mm_find != -1:
			dimensions_val = dimensions[0: mm_find]
			if unit != "" and unit != "mm":
				return -1, ""
			else:
				return dimensions_val, "mm"

	# load data to list:self.data
	def load(self, file_path):
		'''
		:param file_path:
		:return: load cvs data to self.data,and return
		'''
		self.file_path = file_path
		with open(self.file_path) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				self.data.append(row)
			return self.data

	# valid a file
	def data_valid(self):
		'''
		:return: cargo_data file data is valid
		'''
		if not self.data:
			self.err_msg.append("this file is empty，please check")
			return False
		if not self.valid_head(self.data[0]):
			self.err_msg.append("form head is error，please check")
			return False

		for row in self.data:
			self.valid_index(row)
			self.valid_weight(row)
			self.valid_dimension(row)
			self.destination_valid(row)
		return False if self.err_msg else True

	# if file type is not csv，then file type error
	def file_type_valid(self):
		if os.path.splitext(self.file_path)[-1][1:] != 'csv':
			self.err_msg.append("file's type must be csv")
			return False
		return True

	# form_head验证，some field should exist，such as index/weight/dimensions
	def valid_head(self, row):
		not_exist_fields = []
		if 'index' not in row:
			not_exist_fields.append('index')
		if 'weight' not in row:
			not_exist_fields.append('weight')
		if 'dimensions' not in row:
			not_exist_fields.append('dimensions')
		if not_exist_fields:
			self.err_msg.append('field not exits:'+'、'.join(not_exist_fields))
		return False if not_exist_fields else True

	# field:index valid
	def valid_index(self, row):
		index = row.get("index", None)
		if index is None:
			row["err_msg"] = "index is None"
			self.err_msg.append(row)
			return False
		index_t = self.uniq.get(index, None)
		if index_t is None:
			self.uniq[index] = 1
		else:
			row["err_msg"] = "index is not unique"
			self.err_msg.append(row)
			return False
		return True

	# field:weight valid
	def valid_weight(self, row):
		weight = row.get("weight", None)
		weight = str(weight)
		if weight is None:
			row["err_msg"] = "weight is None"
			self.err_msg.append(row)
			return False
		find_index = weight.find("kg")
		if find_index == -1:
			c_weight = weight
		else:
			c_weight = weight[0: find_index]
		if not c_weight.isdigit():
			row["err_msg"] = "weight format error,format likes 20kg"
			self.err_msg.append(row)
			return False
		if int(c_weight) <= 10:
			row["err_msg"] = "weight is <= 10"
			self.err_msg.append(row)
			return False
		return True

	def valid_dimension(self, row):
		# row = {'weight': '15kg', 'dimensions': '5*10cm*cm', 'destination': 'Tian Jin', 'index': 3, 'result': False}
		dimensions = row.get("dimensions", None)
		dimensions = str(dimensions)
		if dimensions is None:
			row["err_msg"] = "dimensions is None"
			self.err_msg.append(row)
			return False
		dimensions_list = dimensions.split("*")
		if len(dimensions_list) != 3:
			row["err_msg"] = "dimensions's format is error."
			self.err_msg.append(row)
			return False
		return self.deal_dimensions_list(dimensions_list,row)

	def deal_dimensions_list(self, dimensions_list, row):
		unit = ""
		for dimensions in dimensions_list:
			ret, ret_unit = self.deal_dimemsions(dimensions, unit)
			if ret == -1:
				row["err_msg"] = "dimensions unit is wrong."
				self.err_msg.append(row)
				return False
			elif not ret.isdigit():
				row["err_msg"] = "dimensions value is not digit,and it must bigger than 0"
				self.err_msg.append(row)
				return False
			elif int(ret) <= 0:
				row["err_msg"] = "dimensions value is wrong,it must bigger than 0"
				self.err_msg.append(row)
				return False
			unit = ret_unit
		return True

	def destination_valid(self,row):
		destination = row['destination']
		return True

	# the row data is correct
	def row_valid(self,row):
		if self.valid_index(row) and self.valid_weight(row) and self.valid_dimension(row) and self.destination_valid(row):
			return True
		return False

	def get_dimension_val(self,dimensions):
		d = dimensions.split("*")
		length = d[0][0:-2]
		width = d[1][0:-2]
		height = d[2][0:-2]
		unit = d[2][-2:]
		return length,width,height,unit

	# convert valid data to list
	def convert_valid_data(self):
		for row in self.data:
			tmp = {}
			if self.row_valid(row):
				tmp['index'] = row['index']
				tmp['destination'] = row['destination']
				tmp['weight'] = row['weight']
				dimensions = self.get_dimension_val(row['dimensions'])
				tmp['length'] = dimensions[0]
				tmp['width'] = dimensions[1]
				tmp['height'] = dimensions[2]
				tmp['unit'] = dimensions[3]
				self.covert_data.append(tmp)

	def export(self, output_file_path= '../data/validated-cargo.json'):
		"""
		:param output_file_path: write data to output_file_path
		:return: None
		"""
		self.convert_valid_data()
		str_data = json.dumps(self.covert_data)
		with open(output_file_path, "w") as f:
			json.dump(str_data, f)

	@staticmethod
	def data_to_tuple(dict_list):
		"""
		convert dict_list to tuple_list
		:return:tuple_list:[((('weight', 20), ('length', 1), ('width', 2), ('height', 3), ('dim_unit', 'cm'), ('destination', 'SZ'), ('index', 1)), 0)]
		"""
		tuple_data = []
		for i in range(len(dict_list)):
			tmp = (tuple(zip(dict_list[i].keys(), dict_list[i].values())),i)
			tuple_data.append(tmp)
		print(tuple_data)
		return tuple_data

	@staticmethod
	def diff_cargo(cargo_data1,cargo_data2):
		"""
		:param cargo_data1: CargoDataSource's instance
		:param cargo_data2: CargoDataSource's instance
		:return: list data in cargo_data1.data and not in cargo_data2.data
		"""

		# convert dict_list to tuple_list with index
		data1 = CargoDataSource.data_to_tuple(cargo_data1.data)
		data2 = CargoDataSource.data_to_tuple(cargo_data2.data)

		diff_list = set(data1)-set(data2)
		diffs = []
		# get tuple_list with no index
		for d in diff_list:
			diffs.append(d[0])
		diff_list = list(map(dict,diffs))
		return diff_list

if __name__ == '__main__':
	cargo_data_source = CargoDataSource()
	cargo_data_source.load('../data/cargo.csv')
	cargo_data_source.export('../data/cargo-json.json')
	cargo1 = CargoDataSource()
	cargo1.data = [
    {"weight": 20, "length": 1, "width": 2, "height": 3,
     "dim_unit": "cm", "destination": "SZ", "index": 1},

    {"weight": 10, "length": 4, "width": 2, "height": 1,
     "dim_unit": "cm", "destination": "SZ", "index": 2},
		{"weight": 20, "length": 1, "width": 2, "height": 3,
		 "dim_unit": "cm", "destination": "SZ", "index": 1},
    ]
	cargo2 = CargoDataSource()
	cargo2.data = [
    {"weight": 20, "length": 1, "width": 2, "height": 3,
     "dim_unit": "cm", "destination": "SZ", "index": 1},

    {"weight": 15, "length": 8, "width": 4, "height": 2,
     "dim_unit": "mm", "destination": "HZ", "index": 2}
    ]
	CargoDataSource.diff_cargo(cargo1,cargo2)



