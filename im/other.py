import time
import string
import random
import secrets
from PIL import Image,ImageDraw,ImageFont


SECRET_KEY = "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(20))


# 返回消息模板
def message(code_num,message):
    result = {"status":code_num,"result":message}
    return result
# 获取当前时间
def get_datetime():
    my_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    return my_date_time

# 得到RGB随机颜色
def get_random_color():
    return random.randint(120,200),random.randint(120,200),random.randint(120,200)

# 得到随机字符
def get_random_code():
    chars = string.ascii_letters+string.digits
    return "".join([chars[random.randint(0,len(chars)-1)],chars[random.randint(0,len(chars)-1)],chars[random.randint(0,len(chars)-1)],chars[random.randint(0,len(chars)-1)]])

# 将随机字符画到图里，并画干扰点，干扰线
def create_image(width=120,height=50,length=4):
    code = get_random_code()
    img = Image.new('RGB',(width,height),(250,250,250))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("static/font/fzstk.ttf",size=40)
    # 画验证文本
    for i in range(4):
        rand_len = random.randint(-3, 3)
        draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),text=code[i], fill=get_random_color(), font=font)
    # 画干扰线
    for i in range(3):
        draw.line((random.randint(0,width),random.randint(0,height),random.randint(0,width),random.randint(0,height)),fill=get_random_color())
    # 画干扰点
    for i in range(16):
        draw.point((random.randint(0,width),random.randint(0,height)),fill=get_random_color())
    
    return img,code


if __name__ == "__main__":
    # pass
    rel = get_random_code()
    print(rel)
