import os
from PIL import Image
from utils import read_dictionary

# 文件位置读取
folderPath = input("请输入图片位置:")
if folderPath == "":
    folderPath = "./images"
resultPath = input("请输入生成位置:")
if resultPath == "":
    resultPath = "./result"
if not os.path.exists(resultPath):
    os.makedirs(resultPath)
# 读取文件夹下的所有图片
images = []  # 图片
images = read_dictionary(folderPath)
imagesName = os.listdir(folderPath)
for i in range(len(imagesName)):
    imagesName[i] = os.path.split(imagesName[i])[1]
    imagesName[i] = os.path.splitext(imagesName[i])[0]
print("当前目录下一共有" + str(len(images)) + "张图片")
# 设置css sprite图片相关参数
print("css sprite相关参数:")
row = 0
column = 0
while row * column < len(images):
    column = input("矩阵长:")
    column = int(column)
    row = input("矩阵宽:")
    row = int(row)
zoom = input("图片缩放大小:")
if zoom == "":
    zoom = "1"
zoom = float(zoom)
# 个性化配置
ignoreStr = input("需要忽略的文件中的字符串:")

# 计算css sprite大小
totalSize = (images[0].size[0] * column, images[0].size[1] * row)
resultImg = Image.new("RGBA", (int(totalSize[0] * zoom), int(totalSize[1] * zoom)), (0, 0, 0, 0))
resultStyle = "@mixin resultImg {\n\tbackground-image: url(./result.png);\n\tbackground-repeat: no-repeat;"
# 获取图片高宽（每张图应该一致）
singleWidth = int(images[0].size[0] * zoom)
singleHeight = int(images[0].size[1] * zoom)
resultStyle += "\n\twidth: " + str(singleWidth) + "px;\n\theight: " + str(singleHeight) + "px;\n}\n"
# 生成css sprite
widthPos = 0
heightPos = 0
i = -1

for image in images:
    i = i + 1
    # 添加图片
    image = image.resize((int(image.size[0] * zoom), int(image.size[1] * zoom)))
    resultImg.paste(image, (widthPos, heightPos, widthPos + image.size[0], heightPos + image.size[1]))
    # 添加对应scss样式
    imagesName[i] = imagesName[i].replace(ignoreStr, "")
    # [x]改为_x，防止css样式问题
    imagesName[i] = imagesName[i].replace("[", "_")
    imagesName[i] = imagesName[i].replace("]", "")
    resultStyle += "." + imagesName[i] + " {"
    resultStyle += "\n\tbackground-position: " + str(widthPos * -1) + "px " + str(heightPos * -1) + "px;\n}\n"
    # 切换到下一张图片
    widthPos += image.size[0]
    if i % column == column - 1:
        heightPos += singleHeight
        widthPos = 0
resultImg.save(resultPath + "/result.png")  # 写入图片
# 写入样式
styleFile = open(resultPath + "/result.scss", "w")
styleFile.write(resultStyle)
styleFile.close()
