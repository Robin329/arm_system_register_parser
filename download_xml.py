# * Copyright (C) 2023 robin

import os
import requests
import tarfile
from tqdm import tqdm
from threading import Thread

# 定义要下载的文件URL
urls = ["https://developer.arm.com/-/media/developer/products/architecture/armv9-a-architecture/2023-09/SysReg_xml_A_profile-2023-09.tar.gz",
        "https://developer.arm.com/-/media/developer/products/architecture/armv9-a-architecture/2023-09/ISA_A64_xml_A_profile-2023-09.tar.gz",
        "https://developer.arm.com/-/media/developer/products/architecture/armv9-a-architecture/2023-09/ISA_AArch32_xml_A_profile-2023-09.tar.gz"]

# 定义要保存文件的本地路径
download_dir = "./dl/"
local_file = os.path.join(download_dir, "SysReg_xml_A_profile.tar.gz")
extract_dir = "./sys_reg_xml/"

# 创建下载目录和解压目录（如果不存在）
os.makedirs(download_dir, exist_ok=True)
os.makedirs(extract_dir, exist_ok=True)

# 下载和解压文件的函数
def download_and_extract(url):
    local_file = os.path.join(download_dir, os.path.basename(url))

    # 发送HTTP GET请求并下载文件，同时显示下载进度
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB

        # 使用 tqdm 创建下载进度条
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

        with open(local_file, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)

        progress_bar.close()  # 关闭进度条
        print(f"File {os.path.basename(url)} Successfully download to {local_file}")

        # 解压文件到指定目录
        with tarfile.open(local_file, 'r:gz') as tar:
            tar.extractall(path=extract_dir)
        print(f"File {os.path.basename(url)} Successfully extracted to {extract_dir}")

        # 可选：删除下载的压缩文件
        os.remove(local_file)
        print(f"Downloaded zip file deleted")
    else:
        print(
            f"Downlaod file {os.path.basename(url)} error, HTTP state code: {response.status_code}")


# 创建并启动线程来处理每个URL
threads = []
for url in urls:
    thread = Thread(target=download_and_extract, args=(url,))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print("Download and decompression of all files completed")
