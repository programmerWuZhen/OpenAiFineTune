from threading_request import threading_do_work
import pymysql

path="/v1/chat/completions"

#向chatgpt发送数据处理请求
#共times个线程，每个线程一个任务，每个任务让ai生成num条数据
def myrequest(user_content,times,num,operations):#(用户数据，提问次数，生成的问答数目)
    str_number=str(num)#生成的问答数目
    table_name=''
    if(operations==1):
        operation="请分析这些文字，帮我从中提取出"+str_number+"组语言为中文的问答，各组问答之间用换行符分隔，问题与答案分别用英文双引号引起来，问题与答案用英文逗号隔开，在问题前面加上{\"prompt\": 在答案前面增加\"completion\": 在答案结尾增加 } 后面是一个示例{\"prompt\":\"这里是换成问题\",\"compleion\":\"这里换成答案\"}请严格按照示例生成数据，并过滤掉答案为英文或未提及的问答"
        table_name='qatb'
    elif(operations==2):
        operation="在不改变原意的基础上，帮我换一种说法，生成意思相同的"+str_number+"组语言为中文的问答，各组问答之间用换行符分隔，问题与答案分别用英文双引号引起来，问题与答案用英文逗号隔开，在问题前面加上{\"prompt\": 在答案前面增加\"completion\": 在答案结尾增加 } 后面是一个示例{\"prompt\":\"这里是换成问题\",\"compleion\":\"这里换成答案\"}请严格按照示例生成数据，并过滤掉答案为未提及或英文的问答"
        table_name='transtb'
    else: return "error! operations should be 1 or 2,1 is create examples;2 is transform"
    #print("------opeation:",operation)
    prompt=user_content+operation
    print("------prompt:",prompt)
    threading_do_work(path,prompt,times,table_name)

#遍历数据库，从数据库中读取一条数据，将该数据根据换行符切分，得到一条问答，再发送
def generate_trans(i,transform_times,transform_quantity):
        conn=pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user="root",
            password="root1201",
            charset='utf8',
            db='testdb_art'
             )
        cursor=conn.cursor()
        sql='select answer from qatb'
        cursor.execute(sql)
        results=cursor.fetchall()
        
        for i in range(i,len(results),10):
            print(f"i is {i},len is {len(results)}")
            lists=results[i][0].split("\n")
            for item in lists:
                myrequest(item,transform_times,transform_quantity,2)
        conn.close()
        


#generate_trans(5,10)