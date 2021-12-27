# Day 7 - This is quite meta

We found this picture that seemed to contain the flag, but it seems like it has been cropped, are you able to help us retrieve the flag?

## Write-Up
For this challenge we are given an image and a hint about "meta"... metadata?

Let's download the image and look at the metadata with `exiftool` and also compare output from another test image.

Challenge Image:
```
$ exiftool 07-challenge.jpg              
ExifTool Version Number         : 12.36
File Name                       : 07-challenge.jpg
Directory                       : .
File Size                       : 9.0 KiB
File Modification Date/Time     : 2021:12:07 01:05:41+01:00
File Access Date/Time           : 2021:12:07 01:06:28+01:00
File Inode Change Date/Time     : 2021:12:07 01:05:46+01:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Comment                         : CREATOR: gd-jpeg v1.0 (using IJG JPEG v80), quality = 75.
Exif Byte Order                 : Big-endian (Motorola, MM)
X Resolution                    : 96
Y Resolution                    : 96
Resolution Unit                 : inches
Y Cb Cr Positioning             : Centered
Thumbnail Offset                : 199
Thumbnail Length                : 2265
Image Width                     : 798
Image Height                    : 69
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 1
Image Size                      : 798x69
Megapixels                      : 0.055
Thumbnail Image                 : (Binary data 2265 bytes, use -b option to extract)
```

Test Image:
```
$ exiftool test.jpg        
ExifTool Version Number         : 12.36
File Name                       : test.jpg
Directory                       : .
File Size                       : 21 KiB
File Modification Date/Time     : 2021:12:20 00:58:08+01:00
File Access Date/Time           : 2021:12:20 00:58:08+01:00
File Inode Change Date/Time     : 2021:12:20 00:58:08+01:00
File Permissions                : -rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 96
Y Resolution                    : 96
Image Width                     : 481
Image Height                    : 324
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 481x324
Megapixels                      : 0.156
```
There is no message in the metadata from the Challenge image, but we see that, compared to the test image, there is a Thumbnail Image inside our Challenge image.

From the metadata we know the offset and length of the Thumbnail image. We can try extract the Thumbnail. `dd` utility which is in my "MultiTool-Toolbox" can be used. But also `Exiftool` has this ability I found out.. clearly I have not played enough with `Exiftool`.

```
1$ exiftool 07-challenge.jpgexiftool -b -ThumbnailImage 07-challenge.jpg > 07-challenge-thumbnail.jpg

2$ dd if=07-challenge.jpg of=dd-thumbnail.jpg bs=1 skip=199 count=2265
```

We can now open these images and see what this reveals...

```
1$ xdg-open 07-challenge-thumbnail.jpg

2$ xdg-open dd-thumbnail.jpg
```

![](./day07/dd-thumbnail.jpg)

## The Flag
RSXC{Sometimes_metadata_hides_stuff}