# coding:utf-8
import os
from lib.core.option import *

# 功能：本程序旨在为安全应急响应人员对Linux主机排查时提供便利，实现主机侧安全Checklist的自动化，用于快速主机安全点排查。


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    # 导入platform库判断平台，分平台导入库
    main(path)