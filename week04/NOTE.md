## 1. python 中导入文件的小技巧

```python
pwd = os.path.dirname(os.path.realpath(__file__))
book = os.path.join(pwd,'book_utf8.csv')
```



## 2. 导出excel表格编码选择

mac, linux, android 导出excel 使用 utf-8编码
windows 导出excel 使用 gbk 编码

## 3. series 和DataFrame 类型数据

series 的数据结构 可看作是Excel中的一列，是因为它来自numpy这种数据结构
DataFrame 的数据结构，就类似于Excel表格形式

