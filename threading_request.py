import threading
import requests
import time 
import db_connection_pool
api_key = "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"
host = "http://chatgpt.lineadmob.fun"

#单次请求
#path:url后半部分 prompt：发送给ai的提示 i 第i次调用 count：成功的请求数目，table，要将数据插入到哪个数据表中
def request_prompt(path,prompt,i,count,table_name):
    print(f"第{i}个请求开始,开始时间为{time.strftime('%X')}")
    #向gpt发送请求
    try:
        response=requests.post(
            url=host+path,
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                'Connection': 'close'
                },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]  
                }
        )
        count[1]=count[1]+1
        data = response.json()
        chat_result = data["choices"][0]["message"]["content"]
        chat_result=chat_result.replace('\'',("\\'"))
        #尝试连接数据库
        try:
            conn = db_connection_pool.get_connection()
            cursor = conn.cursor()
            sql=f'insert into {table_name}(question,answer) values (\'{prompt}\',\'{chat_result}\')'
            cursor.execute(sql)
            conn.commit()
            print(f"插入数据成功")
        except Exception as e:
            print(f"插入数据失败：{e}")
        finally:
            cursor.close()
            db_connection_pool.return_connection(conn)
            print("响应时间为：",response.elapsed)
            print(f"completion of task {i} is :\n{chat_result}")
            #return chat_result
        print(f"第{i}个请求结束\n")
        response.close()
    except requests.exceptions.HTTPError as e:
        if  e.response.status_code == 502:
            print("---网络超时,3秒后重新请求：----")
            time.sleep(3)
            request_prompt(path,prompt,i,count,table_name)
        else:
            print(f"in except requests.exceptions.HTTPError as e:{e}")
            count[0]=count[0]+1
            print(f"{response.status_code}---{response.reason}------{response.content},聊天请求失败，5秒后重试") 
            time.sleep(5)
            #print("聊天请求失败")
    except ConnectionResetError as e:
        print(f'{e}\n将在5秒后重新请求')
        time.sleep(5)
        request_prompt(path,prompt,i,count,table_name)
    except Exception as e:
        print(f"annother error!{e}")
        count[0]=count[0]+1

#多线程工作
#path:url后半部分 prompt：发送给ai的提示 table_name:带插入的数据表名 times：线程数量
def threading_do_work(path,prompt,times,table_name):
    threads = []
    db_connection_pool.init_connection_pool(10,"testdb_art")
    count=[0,0]
    for i in range(times):
        t = threading.Thread(target=request_prompt, args=(path,prompt,i,count,table_name))
        threads.append(t)

    for i in range(len(threads)):
        threads[i].start()

    for i in range(len(threads)):
        threads[i].join()

    print(f"本轮请求共失败了{count[0]}个请求,共成功了{count[1]}条请求")
    db_connection_pool.close_connection_pool()


#test do work

'''
path="/v1/chat/completions"
prompt="在不改变原意的基础上，帮我换一种说法，生成意思相同的10组语言为中文的问答，各组问答之间用换行符分隔，问题与答案分别用英文双引号引起来，问题与答案用英文逗号隔开，在问题前面加上{\"prompt\": 在答案前面增加\"completion\": 在答案结尾增加 } 后面是一个示例{\"prompt\":\"这里是换成问题\",\"compleion\":\"这里换成答案\"}请严格按照示例生成数据，并过滤掉答案为未提及的问答"
table_name='transtb'
for i in range(2):
    threading_do_work(path,prompt,5,table_name)
'''