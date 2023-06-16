#准备数据
import threading_generate
import threading
file_name="user_document_1.txt"
#1.打开用户文件并根据###分段
file_user_document=open(file_name,"r+",encoding="utf-8")
user_document=file_user_document.read()
file_user_document.close()
user_document_sections=user_document.split("###")
section=user_document_sections[0]    
#2.对每个分段进行处理并将数据存储到数据库
def prepare_data(examples_quantity,examples_times,transform_quantity,transform_times):
    for section in user_document_sections:
        #根据该分段的内容，开启examples_times条线程，每个线程发送一个请求，生成examples_quantity条问答
        t1 = threading.Thread(target=threading_generate.myrequest,args=(section,examples_times,examples_quantity,1))
        t1.start()
        t1.join()
    threads = []
    for i in range(10):     
        t = threading.Thread(target=threading_generate.generate_trans,args=(i,transform_times,transform_quantity))
        threads.append(t)
    for i in range(len(threads)):
        threads[i].start()
        print(f"thread{i} in prepare start!")
    for i in range(len(threads)):
        threads[i].join()
        print(f"thread{i} in prepare end!")
   


"""
count=1
for section in user_document_sections:
    print("这是第%d个section:"%(count) ,section)
    count=count+1
"""
#prepare_data(10,10,5,4)