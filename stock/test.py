import zipfile

try:
    zipfile.ZipFile("E:\GITHUB\stock\stock\data\sz_lrb_002093_2006_2017.zip", "r")
    print('文件正常')
except:
    print("文件已损坏")

# 打印zip文件中的文件列表
#for filename in z.namelist():
#    print('File:', filename)
