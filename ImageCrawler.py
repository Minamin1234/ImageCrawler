import os
import shutil
from icrawler.builtin import BingImageCrawler
from PIL import Image
import cv2
import numpy as np


#�f�B���N�g�����̃t�@�C�����w�肵���ԍ�����ʂ��ԍ�������U��܂�
def AssignNumber(Dir,begin=1,pre=""):
  i = begin
  if not os.path.isdir(Dir):
    return
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      name = f"{pre}{i:0=6}.jpg"
      newfilepath = os.path.join(Dir,name)
      os.rename(filepath,newfilepath)
      print(newfilepath)
      i += 1
  return i


#�w�肵���f�B���N�g�����̃t�@�C������Ԃ��܂�
def CountFile(Dir):
  cnt = 0
  if not os.path.isdir(Dir):
    return 0
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      cnt += 1
  return cnt

#�w�肵���f�B���N�g�����̃t�@�C���݂̂��ړ������܂�
def MoveAllFiles(Dir,to):
  if not os.path.isdir(Dir):
    return
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      try:
        shutil.move(filepath,to)
        print("Moved: " + filepath)
      except shutil.Error:
        print("Error: Exisist file.")
        print("File" + filepath)
        continue

#�f�B���N�g�����̑S�Ẵt�@�C�����폜���܂�
def RemoveAllFiles(Dir):
  if not os.path.isdir(Dir):
    return
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      os.remove(filepath)
      print(f"Removed : {filepath}")


#�w�肵�����������߂����t�@�C�����폜���܂��B
def CutFile(Dir,count):
  if CountFile(Dir) <= count:
    return
  cnt = 0
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      if cnt >= count:
        os.remove(filepath)
        print("Removed: " + filepath)
      cnt += 1
  AssignNumber(Dir,pre="_")    
  AssignNumber(Dir)

#�w�肵���Q�̉摜����v���邩�ǂ�����Ԃ��܂�
def IsEqualImage(dir,dir2):
  im1 = cv2.imread(dir)
  im2 = cv2.imread(dir2)
  return np.array_equal(im1,im2)

#�w�肵���摜���摜���X�g���̉摜�ƈ�v���邩�ǂ�����Ԃ��܂�
def IsEqualInList(dir,imglist):
  im = cv2.imread(dir)
  for f in imglist:
    if IsEqualImage(dir,f):
      return True
  return False

def GetFiles(Dir):
  files = []
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      files.append(filepath)
  return files

#�f�B���N�g�����ɉ摜���X�g���ƈ�v����摜������΍폜���܂��B
def RemoveImage(Dir,imglist):
  if not os.path.isdir(Dir):
    return
  print("Start Checking..")
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if IsEqualInList(filepath,imglist):
      os.remove(filepath)
      print("Removed: " + filepath)
  print("Finished checking.")

#�w�肵�������̉摜�����W���܂�
def CollectImages(count,keyw,dir,dir_temp,dir_filter,removefiles=False):
  num = 1000
  if removefiles:
    RemoveAllFiles(dir)
  if count < 1000:
    num = count
  while True:
    if CountFile(dir) < count:
      #RemoveAllFiles(Temp_cat)
      crawler = BingImageCrawler(storage={"root_dir": dir_temp})
      crawler.crawl(keyword=keyw,max_num=num)
      AssignNumber(dir_temp,pre="_")
      MoveAllFiles(dir_temp,dir)
      AssignNumber(dir,pre="__")
      AssignNumber(dir)
      print(f"Dir: {CountFile(dir)}")

    if CountFile(dir) >= count:
      print("Finished.")
      break
  CutFile(dir,count)
  filter = GetFiles(dir_filter)
  RemoveImage(dir,filter)
  AssignNumber(dir,pre="_")
  AssignNumber(dir)
  print("Finished Collect.")


dir = "" #�摜���i�[����f�B���N�g��
dir_temp = "" #�ꎞ�I�ɉ摜���i�[����f�B���N�g��
dir_filter = "" #���O����摜���i�[�����f�B���N�g��
#�L�̉摜��3000�����W����
CollectImages(3000,"�L",dir,dir_temp,dir_filter)