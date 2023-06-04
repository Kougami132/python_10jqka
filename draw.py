from database import DataBase
import matplotlib.pyplot as plt
from time import strftime, localtime




if __name__ == '__main__':
    db = DataBase()
    data = db.get(21)
    # for i in data:
    #     print(i)

    # 解决中文乱码问题
    plt.rcParams['font.family'] = ['sans-serif']
    plt.rcParams['font.sans-serif'] = ['SimHei']

    #准备绘制数据
    x = []
    y = []
    for i in data:
        x.append(strftime('%H:%M', localtime(i[4])))
        y.append(i[3])
    # "g" 表示红色，marksize用来设置'D'菱形的大小
    plt.plot(x, y, "g", marker='D', markersize=5, label="股票走向")
    #绘制坐标轴标签
    plt.xlabel("爬取时间")
    plt.ylabel("股票现价")
    plt.title(f'{strftime("%Y-%m-%d", localtime(data[0][4]))} {data[0][2]} 股票现价走向')
    #显示图例
    plt.legend(loc="lower right")
    #调用 text()在图像上绘制注释文本
    #x1、y1表示文本所处坐标位置，ha参数控制水平对齐方式, va控制垂直对齐方式，str(y1)表示要绘制的文本
    for x1, y1 in zip(x, y):
        plt.text(x1, y1, str(y1), ha='center', va='bottom', fontsize=10)
    #保存图片
    plt.savefig("test.jpg")
    plt.show()