import requests
import time

api_key = "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"
host = "http://chatgpt.lineadmob.fun"
url_file_path="/v1/files"
url_finetune_path="/v1/fine-tunes"

# 设置聊天请求的参数
def requestByPrompt_json(url_path,json):
    url=host+url_path
    # 发送聊天请求
    print(f"task started at {time.strftime('%X')}")
    result=requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
            },
        json=json,
    )
    print(f"task end at {time.strftime('%X')}")
    # 处理聊天响应
    if result.status_code == 200:
        data = result.json()
        print(f"{data},聊天请求成功") 
        print("响应时间为：",result.elapsed)
        #print(f"completion of task  is :\n{chat_result}")
        return data
    else:
        print(f"{result.json()},聊天请求失败") 
        time.sleep(5)
        return ""
#test api


#chat模型
def chat_request(prompt,model="gpt-3.5-turbo"):
    path="/v1/chat/completions"
    json={
        "model": model,
        "messages":[
        #{"role": "user","content":"我是alex"},
        #{"role": "user","content":"我是一名python程序员"},
        {"role": "user", "content": prompt}]  
    }
    data=requestByPrompt_json(path,json)
    chat_result = data["choices"][0]["message"]["content"]
    return chat_result


#completion模型
def completion_request(prompt,model):
    path="/v1/completions"
    json={
        "model":model,
        "prompt":prompt,
        "max_tokens":100,
        "temperature":0.4,
        "stop":"***"
        }
    data=requestByPrompt_json(path,json)
    print("返回的数据为",data['choices'][0]['text'])

#embedding 模型
def embedding_request(prompt):
    path="/v1/embeddings"
    json={
        "input":prompt,
        "model":"text-embedding-ada-002"
    }
    data_json=requestByPrompt_json(path,json)
    result=data_json['data'][0]['embedding']
    print(f"lenth : {len(result)}\n type:{type(result)}\ncompletion of embedding request is :\n{result}")
    sp=','
    embedding_str=sp.join(str(x)for x in result)
    #print(f'list to string\n{embedding_str}')
    print(embedding_str)
    return embedding_str


#upload file
def upload_file(file_path):
    url=host+url_file_path
    headers= {
            "Authorization": f"Bearer {api_key}"
            }
    data={"purpose":"fine-tune"}
    file=open(file_path, 'rb')
    files = {"file": ('generated_examples_1', file, 'application/json')}
    response=requests.post(url,headers=headers,files=files,data=data)
    content=response.json()
    file_id=content["id"]
    print(f"file_id:{file_id}\ncontent:{content}")
    return file_id


#fine_tune


def finetune(json):
    url=url_finetune_path
    json=json
    requestByPrompt_json(url,json)


#retrieve fine_tune
def retrieve_finetune(finetune_id):
    finetune_id=finetune_id
    url_status_job=host+url_finetune_path+finetune_id
    response=requests.get(
        url_status_job,
        headers={
            "Authorization": f"Bearer {api_key}"
        }
        )
    print(response.json())


#test api
#1 test chat model 
#chat_request("openai微调所使用的基础模型能做什么")

#2 test completion 
prompt="西夏经历了几代帝王###"
model="ada:ft-personal:format-2023-06-14-04-10-48"
#completion_request(prompt,model)

# 3 test embedding 
embedding_request("this is a test ")


#3 test upload file
file_path="E:/Work/VSCode/Python/OpenAi/FineTuning/test_transformed_2.jsonl"
#file_id=upload_file(file_path)

# test fine tune
file_id="file-WQn7wRZuEzSnsHVfleeNB0iK"
json={
    "training_file": file_id,
    "model":"ada",
    'n_epochs': 4,
    "batch_size":150,
    "learning_rate_multiplier":0.1,
    'suffix':"_transformed_2"
}
#finetune(json)


# test retrieve
#retrieve_finetune("/ft-eWxGRV9M4ffvGOqQrn2DUr3w")