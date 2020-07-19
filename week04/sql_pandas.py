# 1. SELECT * FROM data;
import pandas as pd
data = {'id':[x for x in range(1,7)], 'Name':['张三','李四','王五','赵六','翠花', '二丫'], 'Sex': ['男','男','男','男','女','女'], 'age':[23, 26, 24, 19, 18, 15]}
df = pd.DataFrame(data)
print(df)

import pymysql
sql  =  'SELECT *  FROM data'
conn = pymysql.connect('ip','name','pass','dbname','charset=utf8')
df = pd.read_sql(sql,conn)

# 2. SELECT * FROM data LIMIT 10;
print(df.head(10))

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
print(df['id'])

# 4. SELECT COUNT(id) FROM data;
print(df.shape[0])

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
print( df[(df['id'] < 1000) & (df['age'] > 30)])

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
df1 = df1.groupby('id')
count_order_id = df1.drop_duplicates(subset=order_id,inplace=False).shape[0]
df1['id', 'count_order_id']

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(table1, table2, on='id', how='inner')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
df4 = pd.concat([table1, table2])
print(df4)

# 9. DELETE FROM table1 WHERE id=10;
df.drop(df[df.id == 10].index, inplace=True)

# 10. ALTER TABLE table1 DROP COLUMN xis
df.drop('age',axis=1, inplace=True)