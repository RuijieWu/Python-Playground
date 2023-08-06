'''
classify files
'''
import os
import shutil

DIRPATH = ""
if __name__ == "__main__":
    os.makedirs(DIRPATH+"Pictures")
    os.makedirs(DIRPATH+"Videos")
    os.makedirs(DIRPATH+"Documents")
    os.makedirs(DIRPATH+"Audio")
    for f in os.listdir(DIRPATH) :
        if not os.path.isdir(DIRPATH+f) :
            if os.path.splitext(DIRPATH+f)[1] in [
                ".txt",
                ".bak",
                ".docx",
                ".xlsx",
                ".doc",
                ".pptx"
                ] :
                shutil.move(DIRPATH+f, DIRPATH+"Documents"+f)
                print(f"{f} had been moved to {DIRPATH}"+"Documents" )

            if os.path.splitext(DIRPATH+f)[1] in [
                ".mp3",
                ".wav"
            ]:
                shutil.move(DIRPATH+f, DIRPATH+"Audio"+f)
                print(f"{f} had been moved to {DIRPATH}"+"Audio" )

            if os.path.splitext(DIRPATH+f)[1] in [
                ".mp4",
                ".mov",
            ]:
                shutil.move(DIRPATH+f, DIRPATH+"Videos"+f)
                print(f"{f} had been moved to {DIRPATH}"+"Videos")

            if os.path.splitext(DIRPATH+f)[1] in [
                ".png",
                ".jpg",
                ".bmp",
                ".webp",
                ".jpeg"
            ]:
                shutil.move(DIRPATH+f, DIRPATH+"Pictures"+f)    
                print(f"{f} had been moved to {DIRPATH}"+"Pictures" )
