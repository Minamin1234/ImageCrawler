import os
import shutil
from icrawler.builtin import BingImageCrawler
from PIL import Image
import cv2
import numpy as np


#ディレクトリ内のファイルを指定した番号から通し番号を割り振ります
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


#指定したディレクトリ内のファイル数を返します
def CountFile(Dir):
  cnt = 0
  if not os.path.isdir(Dir):
    return 0
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      cnt += 1
  return cnt

#指定したディレクトリ内のファイルのみを移動させます
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

#ディレクトリ内の全てのファイルを削除します
def RemoveAllFiles(Dir):
  if not os.path.isdir(Dir):
    return
  for f in os.listdir(Dir):
    filepath = os.path.join(Dir,f)
    if os.path.isfile(filepath):
      os.remove(filepath)
      print(f"Removed : {filepath}")


#指定した数よりも超過したファイルを削除します。
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

#指定した２つの画像が一致するかどうかを返します
def IsEqualImage(dir,dir2):
  im1 = cv2.imread(dir)
  im2 = cv2.imread(dir2)
  return np.array_equal(im1,im2)

#指定した画像が画像リスト内の画像と一致するかどうかを返します
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

#ディレクトリ内に画像リスト内と一致する画像があれば削除します。
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

#指定した枚数の画像を収集します
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


dir = "" #画像を格納するディレクトリ
dir_temp = "" #一時的に画像を格納するディレクトリ
dir_filter = "" #除外する画像を格納したディレクトリ
#猫の画像約3000枚収集する
CollectImages(3000,"猫",dir,dir_temp,dir_filter)