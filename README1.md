#关于任务2：
##工程：ApiAutoExam项目下的deal_data目录下，运行cargo_data_source.py,对应测试用例运行：test_deal_data.py

```
class CargoDataSource:

	def load(self, input_file_path):
		'''
		:param file_path:
		:return: load cvs data to self.data,and return
		'''

	def export(self, output_file_path):
		"""
		:param output_file_path: write data to output_file_path
		:return: None
		"""

    # valid a file
	def data_valid(self):
		'''
		:return: cargo_data file data is valid
		'''

    @staticmethod
	def diff_cargo(cargo_data1,cargo_data2):
		"""
		:param cargo_data1: CargoDataSource's instance
		:param cargo_data2: CargoDataSource's instance
		:return: list data in cargo_data1.data and not in cargo_data2.data
		"""
```

##method:
###1、load：
```
CargoDataSource().load('./cargo.csv)
```

###2、export
export csv file's valid data to json file
```
cargo_data_source = CargoDataSource()
cargo_data_source.load('../data/cargo.csv')
cargo_data_source.export('../data/cargo-json.json')
```

###3、data_valid ->return boold
```
cargo_data_source = CargoDataSource()
cargo_data_source.load('../data/cargo.csv')
cargo_data_source.data_valid()
```

### 4、diff_cargo -> return diff_list
```
cargo_data_source = CargoDataSource()
data1 = cargo_data_source.load('../data/cargo.csv')
cargo_data_source = CargoDataSource()
data2 = cargo_data_source.load('../data/cargo.csv')
CargoDataSource.diff_cargo(data1,data2)
```

##testcases:
###1、文件类型验证：such as：txt、xls、csc、ppt、empty file
###2、表头验证
* Index字段不存在，其他字段正常
* Weight字段不存在，其他字段正常
* Dimens字段不存在，其他字段正常
* destination不存在，可以通过
* 别的字段存在，通过
###3、字段index验证
* index是否存在
* Index是否唯一验证
* 特殊字符，-1、0、maxint、
###4、weight验证
* 重量包含单位且>10kg验证通过
* 不包含单位
* 重量单位错误
* 重量<=10
* 重量为空
* 重量格式错误，eg：kg20，验证不通过
* 没有重量值
* 重量值验证：10、0、maxint
###5、Dimensions验证
* 尺寸单位和值正确
* 尺寸缺少单位
* 尺寸单位错误
* 尺寸单位混用
* 尺寸缺少*
* 尺寸值<0
###6、Destination验证
* 正常的一个地址，eg：shenzhen
* 一个详细的正常地址：eg：广东省、深圳市。。。
* 空
* 纯数字
