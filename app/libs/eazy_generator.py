import random
import string

def generate_random_string(length=6):
    # 定义字符集：大小写字母 + 数字
    characters = string.ascii_letters + string.digits
    
    # 使用random.choices从字符集中随机选择length个字符
    random_string = ''.join(random.choices(characters, k=length))
    
    return random_string