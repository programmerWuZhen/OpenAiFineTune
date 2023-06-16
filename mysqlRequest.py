import pymysql
import re
from myRequest import embedding_request

#查看数据所有库
"""
mycursor.execute("show databases")
result=mycursor.fetchall()
print(result)
"""
#创建一个数据表
"""
sql='create table qatb(id int not null auto_increment primary key,question text,answer text)'
#sql="drop table qatb"
cursor.execute(sql)
conn.commit()
"""

#插入一条数据
'''
question="this is a test"
answer="yes as an ai  i will accept this test and say hello"
table_name='qatb'
sql=f'insert into {table_name}(question,answer) values(\'{question}\',\'{answer}\')'
#sql='delete from qatb'
cursor.execute(sql)
conn.commit()
'''
"""
#数据查询

for i in range(0,200,10):
    question=results_question[i][0]
    question=question.replace("\"","\\\"")
    answer=results[i][0]
    answer=answer.replace("\"","\\\"")
    print(answer)
    line='{"prompt":"'+question+'###","completion":"'+repr(answer)+'"}'
    file_test.writelines(line+'\n')
file_test.close()
"""
#结果查看
'''
print(f"直接获取得到的结果为：{results}\n数量为:{len(results)}")
(('this is ansuer',), ('a2',)) 数量为:2
print(f"results 元组的第一个元素为：{results[0]}")
results 元组的第一个元素为：('this is ansuer',)
'''
#file_fine_tune_data=open('test_transformed_1.jsonl','w+',encoding='utf8')
#sql='select answer from qatb'

#file_fine_tune_data=open('generated_examples_1.jsonl','w+',encoding='utf8')
#sql='select answer from qatb'
def generate_text(sql='select answer from transtb',file_finetune_path="test_transformed_2.jsonl"):
    conn=pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root1201',
    charset='utf8',
    db='testdb_art'
    )
    file_fine_tune_data=open(file_finetune_path,"w+",encoding="utf8")
    cursor = conn.cursor()
    cursor.execute(sql)
    results=cursor.fetchall()
    for result in results:
        lists=result[0].split('\n')
        #print(f"---当前为第{i}个result---")
        for item in lists:
            if(item!=''):
                item=item.strip()
                item=item.rstrip(',')
                pattern = re.compile('}.*?{')
                item=re.sub(pattern,'}\n{',item)
                item=item+'\n'
                file_fine_tune_data.write(item)
    file_fine_tune_data.close()
    cursor.close()
    conn.close() 
    return file_finetune_path

"""
sql='select answer from transtb'
file_finetune_path="test_transformed_2.jsonl"
generate_text(sql,file_finetune_path)
"""
def  test():
    file=open('generated_examples_2.jsonl','r',encoding="utf8")
    file_data=file.readlines()
    patten=re.compile('(?<=prompt":").*?(?=###)')
    patten2=re.compile('(?<=completion":").*?(?=END"})')
    conn=pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root1201',
            charset='utf8',
            db='embeddingdb'
            )
    cursor=conn.cursor()
    for line in file_data:
        if line!="":
            ob1=re.search(patten,line)
            ob2=re.search(patten2,line)
            if ob1:
                prompt=ob1.group()               
                if ob2:
                    completion=ob2.group()
                    embedding=embedding_request(prompt)
                    sql=f"insert into qatb(question,answer,embedding) values(\"{prompt}\",\"{completion}\",{embedding})"
                    print(sql)
                    cursor.execute(sql)
                    conn.commit()
    cursor.close()
    conn.close()
    file.close()
    
test()
    