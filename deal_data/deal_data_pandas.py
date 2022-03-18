# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/17/5:45 下午
import shlex

import pandas as pd


class CargoDataSource(object):
    '''
    deal data with pandas
    '''

    def __init__(self):
        self.df = None

    def load(self,file_path='./cargo.csv'):
        self.df = pd.read_csv(file_path)

    def deal_data(self):
        self.rm_empty()
        self.rm_na()
        self.rm_duplicates_index()
        self.deal_weight()
        self.deal_dimensions()

    def rm_empty(self):
        self.df.dropna(inplace=True)

    def rm_na(self):
        self.df.dropna(subset=['index','weight','dimensions'],inplace=True)

    def rm_duplicates_index(self):
        self.df.drop_duplicates(subset=['index'], keep='first', inplace=True)

    def deal_weight(self):
        for x in self.df.index:
            weight = self.df.loc[x, "weight"]
            find_index = weight.find("kg")
            if find_index == -1:
                c_weight = weight
            else:
                c_weight = weight[0: find_index]
            if not c_weight.isdigit():
                self.df.drop(x, inplace=True)
                continue
            if int(c_weight) <= 10:
                self.df.drop(x, inplace=True)

    def deal_dimensions(self):
        print(self.df)
        for x in self.df.index:
            dimensions = self.df.loc[x, "dimensions"]
            dimensions_list = dimensions.split("*")
            # if not use * to seperate data，then remove
            if len(dimensions_list) != 3:
                self.df.drop(x, inplace=True)
                continue
            # if unit is difference or dimensions val <= 0,，to remove
            if not self.deal_dimensions_list(dimensions_list):
                self.df.drop(x, inplace=True)

    def deal_dimensions_list(self, dimensions_list):
        unit = ""
        for dimensions in dimensions_list:
            ret, ret_unit = self.dimemsions_units_vals(dimensions, unit)
            # unit is difference
            if ret == -1:
                return False
            # dimension val
            elif not ret.isdigit():
                return False
            elif int(ret) <= 0:
                return False
            unit = ret_unit
        return True

    # deal with dimensions unit and val
    def dimemsions_units_vals(self, dimensions, unit):
        cm_find = dimensions.find("cm")
        mm_find = dimensions.find("mm")
        if cm_find == -1 and mm_find == -1:
            return -1, ""
        if cm_find != -1:
            print("dimensions[0: cm_find]:", dimensions[0: cm_find])
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

    def data_convert(self):
        self.df['length'] = self.df['dimensions'].apply(lambda x: x.split('*')[0][0:-2])
        self.df['width'] = self.df['dimensions'].apply(lambda x: x.split('*')[1][0:-2])
        self.df['height'] = self.df['dimensions'].apply(lambda x: x.split('*')[2][0:-2])
        self.df['unit'] = self.df['dimensions'].apply(lambda x: x.split('*')[2][-2:])

    def write_csv(self,out_put_file='./cargo_valid.csv'):
        self.df.to_csv(out_put_file)

    def export(self, output_file_path='./validated-cargo.json'):
        """
        :param output_file_path: write data to output_file_path
        :return: None
        """
        self.df.to_json(output_file_path)


if __name__ == '__main__':
    data = CargoDataSource()
    data.load('./cargo.csv')
    data.deal_data()
    data.data_convert()
    data.write_csv()
    data.export()
