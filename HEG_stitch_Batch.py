# -*- coding: utf-8 -*-
"""
调用HEG相关工具批量完成MODIS数据拼接工作。
"""
import glob
import os
import re
# 设置HEG相关环境变量，简单来说就是把data，TOOLKIT_MTD,bin的路径告诉系统，方便cmd执行，别问我为什么，用户手册上写的
os.environ['MRTDATADIR'] = r'D:\HEG\HEGtools\HEG_Win\data'
os.environ['PGSHOME'] = r'D:\HEG\HEGtools\HEG_Win\TOOLKIT_MTD'
os.environ['MRTBINDIR'] = r'D:\HEG\HEGtools\HEG_Win\bin'
# 设置HEG的bin路径
hegpath = r'D:\HEG\HEGtools\HEG_Win\bin'
# 指定处理模块的可执行程序文件subset_stitch_grid，
hegdo = os.path.join(hegpath, 'subset_stitch_grid.exe')


# 指定输入数据的路径
inpath = os.getcwd()

# inpath = inpath.replace('\\', '/')
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        # print
        # path + ' 创建成功'
        return True

    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


mkdir(inpath+'\\prm\\')
mkdir(inpath+'\\result\\')
# 指定输出数据的路径
# os.mkdir(os.getcwd()+'\\result\\')
outpath = os.getcwd()+'\\result\\'
# outpath = outpath.replace('\\', '/')

allhdffiles=glob.glob(inpath+'\*.hdf')
allhdffiles.sort()
# 获取当前文件夹下的所有hdf文件
prmpath = inpath+"\\prm_gridstitch" #参考文件路径
fr = open(prmpath, 'r+')
prm = fr.read()

NUMBER_INPUTFILES = re.findall("NUMBER_INPUTFILES = (.*)", prm)[0]  # 拼接文件数目
##################读取参考文件参数#########
FIELD_NAME = re.findall("FIELD_NAME = (.*)", prm)[0]
OBJECT_NAME = re.findall("OBJECT_NAME = (.*)", prm)[0]
BAND_NUMBER = re.findall("BAND_NUMBER = (.*)", prm)[0]
SPATIAL_SUBSET_UL_CORNER = re.findall("SPATIAL_SUBSET_UL_CORNER = (.*)", prm)[0]
SPATIAL_SUBSET_LR_CORNER = re.findall("SPATIAL_SUBSET_LR_CORNER = (.*)", prm)[0]
OUTPUT_OBJECT_NAME = re.findall("OUTPUT_OBJECT_NAME = (.*)", prm)[0]
OUTGRID_X_PIXELSIZE = re.findall("OUTGRID_X_PIXELSIZE = (.*)", prm)[0]
OUTGRID_Y_PIXELSIZE = re.findall("OUTGRID_Y_PIXELSIZE = (.*)", prm)[0]
RESAMPLING_TYPE = re.findall("RESAMPLING_TYPE = (.*)", prm)[0]
OUTPUT_PROJECTION_TYPE = re.findall("OUTPUT_PROJECTION_TYPE = (.*)", prm)[0]
ELLIPSOID_CODE = re.findall("ELLIPSOID_CODE = (.*)", prm)[0]
OUTPUT_PROJECTION_PARAMETERS = re.findall("OUTPUT_PROJECTION_PARAMETERS = (.*)", prm)[0]
OUTPUT_FILENAME = re.findall("OUTPUT_FILENAME = (.*)", prm)[0]
SAVE_STITCHED_FILE = re.findall("SAVE_STITCHED_FILE = (.*)", prm)[0]
# OUTPUT_STITCHED_FILENAME = re.findall("ELLIPSOID_CODE = (.*)", prm)[0]
OUTPUT_TYPE = re.findall("OUTPUT_TYPE = (.*)", prm)[0]
#############################
n = int(NUMBER_INPUTFILES)

fr.close()

# 输入文件
hdf_group=[allhdffiles[i:i+n] for i in range(0,len(allhdffiles),n)]
inputfile='|'.join(hdf_group[0])
# print(inputfile)
#######################创建参数文件

i = 0
while i < len(hdf_group):
    # 变量prm暂存过会儿需要写进txt的文本
    inputfile = '|'.join(hdf_group[i])
    # print(hdf_group[i])
    outputfile = outpath + '.'.join(os.path.basename(hdf_group[i][0]).split('.')[0:2])+'.'+FIELD_NAME.strip('|')+'.tif'
    print(outputfile)

    prm = [

        'NUM_RUNS = 1\n',

        'BEGIN\n',

        'NUMBER_INPUTFILES = ' + NUMBER_INPUTFILES + '\n',  # 提前根据命名规则看一下你需要把多少个文件合在一起，这里就写几

        'INPUT_FILENAMES = ' + inputfile + '\n',  # 这里是路径

        'OBJECT_NAME = ' + OBJECT_NAME + '\n',

        'FIELD_NAME = ' + FIELD_NAME + '\n',

        'BAND_NUMBER = ' + BAND_NUMBER + '\n',

        'SPATIAL_SUBSET_UL_CORNER = ' + SPATIAL_SUBSET_UL_CORNER + '\n',

        'SPATIAL_SUBSET_LR_CORNER = ' + SPATIAL_SUBSET_LR_CORNER + '\n',

        'OUTPUT_OBJECT_NAME = ' + OUTPUT_OBJECT_NAME + '\n',

        'OUTGRID_X_PIXELSIZE = ' + OUTGRID_X_PIXELSIZE + '\n',

        'OUTGRID_Y_PIXELSIZE = ' + OUTGRID_Y_PIXELSIZE + '\n',

        'RESAMPLING_TYPE = '+RESAMPLING_TYPE+'\n',

        'OUTPUT_PROJECTION_TYPE = '+OUTPUT_PROJECTION_TYPE+'\n',

        'ELLIPSOID_CODE = '+ELLIPSOID_CODE+'\n',

        'OUTPUT_PROJECTION_PARAMETERS = '+OUTPUT_PROJECTION_PARAMETERS+'\n',

        'OUTPUT_FILENAME = ' + outputfile+'\n',

        # 输出文件名，路径+名字+后缀名，你可以随意命名

        'SAVE_STITCHED_FILE = '+SAVE_STITCHED_FILE+'\n',

        # 'OUTPUT_STITCHED_FILENAME = '+outpath+'/'+allhdffiles[i]+'_stitched.hdf\n',


        'OUTPUT_TYPE = '+OUTPUT_TYPE+'\n',

        'END\n',

    ]

    prmfilename = inpath+"\\prm\\"+'.'.join(os.path.basename(hdf_group[i][0]).split('.')[0:2])+'.'+FIELD_NAME.strip('|')+'_prm'

    # 这里一定要注意，设定换行符为‘\n’,否则由于在windows系统下默认换行符为‘\r\n’,则无法运行成功

    fo = open(prmfilename, 'w', newline='\n')

    fo.writelines(prm)

    fo.close()

    i+=1

# 写入参数文件

prmlist=glob.glob(inpath+"\\prm\\"+'*_prm')
# 执行拼接工具
for x in range(len(prmlist)):
    prmfile=prmlist[x]
    resamplefiles = '{0} -P {1}'.format(hegdo, prmfile)
    os.system(resamplefiles)
