from prepareData import *
from mysqlRequest import generate_text
from myRequest import *
# 1. prepare data

#参数：单次请求生成的问答数 请求次数 单次请求生成的同义转换数 请求次数
# 1.0 生成的结果将存至数据库
prepare_data(10,10,5,4)

# 1.1 将数据库中的数据按指定格式存至文件中
file_path=generate_text()


# 2 upload file
file_id=upload_file(file_path)

# 3 fine tune
json={
    "training_file": file_id,
    "model":"ada",
    'n_epochs': 4,
    "batch_size":100,
    "learning_rate_multiplier":0.01,
    'suffix':"_transformed_2"
}
finetune(json)