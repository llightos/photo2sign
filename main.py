import os

from PIL import Image, ImageOps


# 输入，输出和门限
def create_electronic_signature(image_path, output_path, thresholdIn):
    # 打开图片
    img = Image.open(image_path)

    # 转换为灰度图像
    img_gray = img.convert("L")

    # 使用阈值处理来二值化图像，阈值需要根据实际图片调整
    threshold = thresholdIn  # 阈值，需要根据实际图片调整
    img_binary = img_gray.point(lambda x: 0 if x < threshold else 255, '1')

    # 反转图像，使得签名为白色，背景为黑色
    img_binary = ImageOps.invert(img_binary)

    # 将二值化图像转换为RGBA模式
    img_binary = img_binary.convert("RGBA")

    # 加载图片数据
    datas = img_binary.getdata()

    # 创建一个新的图片数据列表
    new_data = []
    for item in datas:
        # 将黑色部分（背景）设置为透明
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append((0, 0, 0, 255))  # 将白色部分（签名）设置为黑色且不透明

    # 将新的图片数据写入图片
    img_binary.putdata(new_data)

    # 保存图片
    img_binary.save(output_path, "PNG")


def image_file():
    # 定义图片文件的扩展名（可以根据需要添加更多）
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

    # 获取当前目录
    current_directory = os.getcwd()

    # 列出当前目录下的所有文件
    files = os.listdir(current_directory)

    # 过滤出图片文件
    image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_extensions]

    return image_files


for image_file in image_file():
    input_name = image_file
    split_result = input_name.split(".")
    folder_name = split_result[0]

    if not os.path.exists(split_result[0]):
        os.mkdir(input_name.split(".")[0])

    # 使用函数
    for x in range(7):
        print("x", x)
        create_electronic_signature(input_name,
                                    "./{}/{}_{}.png".format(split_result[0], split_result[0], str(40 + x * 20)),
                                    40 + x * 20)
