import os
import shutil
import numpy
from pytube import YouTube
import cv2 as cv
import img2pdf
from PIL import Image
import imagehash

link = input('Enter link: ')

# Remove previous video
try:
    os.remove(r'D:/Python/pdf/video.mp4')
except:
    pass

# Download video
youtube = YouTube(link)
my_video = youtube.streams.filter(fps = 30, res = "480p").first()
out_file = my_video.download(r'D:/Python/pdf')
os.rename(out_file, r'D:/Python/pdf/video.mp4')

# Remove previous images
import os, shutil
folder = r'D:/Python/pdf/images'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Convert Video to Images (Every 150th frame i.e. 5 seconds)
path = r'D:/Python/pdf/images'
vidcap = cv.VideoCapture(r'D:/Python/pdf/video.mp4')

vidcap.set(cv.CAP_PROP_POS_AVI_RATIO,1)
frames = vidcap.get(cv.CAP_PROP_FRAME_COUNT)
frames_len = len(str(int(frames)))
vidcap.set(cv.CAP_PROP_POS_AVI_RATIO,0)

success,image = vidcap.read()
count = 0
while success:
    if count%150 == 0:
        add_zeros = frames_len - len(str(count))
        zeros_str = '0'*add_zeros
        name = "frame{}.jpg".format(zeros_str + str(count))
        crop_img = image[40:450, 0:640]
        cv.imwrite(os.path.join(path , name), crop_img)
    else:
        pass
    success,image = vidcap.read()
    count += 1

# Hashing images to find duplicates
files = sorted(os.listdir(r'D:/Python/pdf/images'))
count = 0
hash_list = []

for file in files:
    if file == files[0]:
        count += 1
        continue
        
    hash1_file = files[count - 1]
    hash1_address = "{}{}{}".format('D:\\Python\\pdf\\images', '\\', hash1_file)
    hash2_file = files[count]
    hash2_address = "{}{}{}".format('D:\\Python\\pdf\\images', '\\', hash2_file)
    
    hash1 = imagehash.average_hash(Image.open(hash1_address))
    hash2 = imagehash.average_hash(Image.open(hash2_address))
    
    if((hash1 - hash2) <= 1):
        hash_list.append(0)    
    else:
        hash_list.append(hash1 - hash2)
    
    count += 1

# Hash difference of images(non-zero are originals)
count = 1
for term in hash_list:
    print('{} : {}'.format(files[count], term))
    count += 1

# Saving non-zero pages
print('Page {} : {} saved!'.format(1, files[0]))
page_count = 2
count = 1
for term in hash_list:
    if term == 0:
        file_name = files[count]
        file_address = "{}{}{}".format('D:\\Python\\pdf\\images', '\\', file_name)
        os.remove(file_address)
    else:
        print('Page {} : {} saved!'.format(page_count, files[count]))
        page_count += 1
    count += 1

# Convert Images to PDF
dirname = r'D:/Python/pdf/images'
imgs = []
for fname in os.listdir(dirname):
    if not fname.endswith(".jpg"):
        continue
    path = os.path.join(dirname, fname)
    if os.path.isdir(path):
        continue
    imgs.append(path)
with open("final.pdf","wb") as f:
    f.write(img2pdf.convert(imgs))

shutil.move(os.path.join(r'C:/Users/archi/Python Code/pdf', 'final.pdf'), os.path.join(r'D:/Python/pdf', 'final.pdf'))
