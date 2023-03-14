import os
import shutil

dirpath = "./Python_Develop/"
os.makedirs(dirpath+"Pictures")
os.makedirs(dirpath+"Videos")
os.makedirs(dirpath+"Documents")
os.makedirs(dirpath+"Audio")
for f in os.listdir(dirpath) :
    if not os.path.isdir(dirpath+f) :
        if os.path.splitext(dirpath+f)[1] in [
            ".txt",
            ".bak",
            ".docx",
            ".xlsx",
            ".doc",
            ".pptx"
            ] :
            shutil.move(dirpath+f, dirpath+"Documents"+f)
            print(f"{f} had been moved to {dirpath}"+"Documents" )
            
        if os.path.splitext(dirpath+f)[1] in [
            ".mp3",
            ".wav"
        ]:
            shutil.move(dirpath+f, dirpath+"Audio"+f)
            print(f"{f} had been moved to {dirpath}"+"Audio" )
            
        if os.path.splitext(dirpath+f)[1] in [
            ".mp4",
            ".mov",
        ]:
            shutil.move(dirpath+f, dirpath+"Videos"+f)
            print(f"{f} had been moved to {dirpath}"+"Videos")
            
        if os.path.splitext(dirpath+f)[1] in [
            ".png",
            ".jpg",
            ".bmp",
            ".webp",
            ".jpeg"
        ]:
            shutil.move(dirpath+f, dirpath+"Pictures"+f)    
            print(f"{f} had been moved to {dirpath}"+"Pictures" )
        
    