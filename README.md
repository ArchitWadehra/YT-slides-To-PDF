# YouTube slides To PDF generator

Python code to convert ppt slides in YouTube videos to PDF format. 

1) Downloads the video using pytube. 

2) Converts the video into images every 5 seconds(150 frames).

3) Then uses Image Hashing to check if we saved duplicate images and delete images with similar hash. Image hashes tell whether two images look nearly identical. This is different from cryptographic hashing algorithms (like MD5, SHA-1) where tiny changes in the image give completely different hashes. In image fingerprinting, we actually want our similar inputs to have similar output hashes as well.

4) finally converts the image to pdf using img2pdf.
