# Number Plate Detection on c610
## About the project

 - In this project, we are trying to detect and recognize the number plate using the qualcomm c610 camera. OpenCV library api’s are used for detecting the number plate region in the given or captured image and using the google tesseract-ocr python library, we are recognizing the number & digits on the detected region
 
## Dependencies
- Ubuntu System 18.04 or above
- Install Adb tool (Android debugging bridge) on host system
- Yocto build environment on host system
- Install python3.5 or above on the host system 


## Prerequisites
- Camera Environment configuration setup on the target device.
- Building the opencv library for target board
- Building the tesseract library for target board



### Camera Environment configuration setup on the target device.
 - To setup the camera environment configuration follow the below  document "Turbox-C610_Open_Kit_Software_User_Manual_LE1.0_v2.0.pdf" In given url 
“https://www.thundercomm.com/app_en/product/1593776185472315” and Refer section 2.10.1

### Install opencv library on board 
- To install opencv library on the target board the required meta recipe for opencv is already present in folder “poky/meta-openembedded/meta-oe/recipes-support/opencv/opencv_3.4.5.bb” file. We need to follow the below steps to build.

-  Get into the yocto working directory

 ```sh
        $ cd  <yocto working directory>
 ```
 
- Execute source command for environment setting 

 ```sh
        $ source poky/qti-conf/set_bb_env.sh
 ```
- The pop up menu will be open for available machines that select “qcs610-odk” and press ok. Then one more pop up window will be open for distribution selection in that we need to select “qti-distro-fullstack-perf”. Run the bitbake command for installing packages.

 ```sh
        $ bitbake opencv 
 ```


- Once the build is complete the shared library and include file will be available in “./tmp-glibc/sysroots-components/armv7ahf-neon/opencv/usr”
Push the opencv shared library to the target board 

 ```sh
        $ cd  ./tmp-glibc/sysroots-components/armv7ahf-neon/opencv/usr/
        $ adb push lib/  /data/cv2/
        $ adb push include/opencv/  /usr/include/
        $ adb push include/opencv2/  /usr/include/
 ```

**Note**: 
- For more reference refer to the “QCS610/QCS410 Linux Platform Development Kit Quick Start Guide document”.
- Also make sure install the all the dependency library from the yocto build to the system (ex: libgphoto2, libv4l-utils) 
- bb recipes of above  library are available inside meta-oe layer you can directly run bitbake command


### Building the tesseract library
 - To run the tesseract package on qcs610. you need to build the following packages on yocto build. meta recipes for these packages are available in the meta-recipe from source repository.
Required package are,
    - python3-pillow
    - tesseract
    - tesseract-lang
    - python3-pytesseract

- We can place/replace the python-pillow and pytesseract bb recipe in the given folder name /poky/meta-openembedded/meta-python/python/. similarly we can replace the tesseract folder in  /poky/meta-openembedded/meta-oe/recipes-graphics/. 

- Run the bitbake command for installing packages.
 ``` 
        $ bitbake <package-name> 
```
- Once the build is complete the library, shared library and include file will be available in “./tmp-glibc/sysroots-components/armv7ahf-neon/<package-name>/usr”
For c/c++ library, Push the  <package-name> shared library(.so files) to the target board 
```
        $ cd ./tmp-glibc/sysroots-components/armv7ahf-neon/<package-name>/usr/
        $ adb push lib/*.so  /data/tesseract/lib/
```
 - if the <package-name> contain any include file copy that into /usr/include/  directory
 adb push include/*  /usr/include/

- For python3 packages push the files inside in the library python3.5/site-packages directory to /data/tesseract/lib/  (bitbake file of python packages is start with ‘python3-’)
```
        $ adb push lib/python3.5/site-packages/*  /data/tesseract/lib/
```
- apart from above mentioned libraries, following dependent libraries will also be builded, you need to push these libararies and include files into the target board.  Dependency libraries are openjpeg, lcms, leptonica, tiff, lib-jpeg-turbo, python3-pyparsing, python3-cython, giflib.
- copy the tesseract binary file present in “./tmp-glic/work/armv7ahf-neon-oe-linux-gnueabi/tesseract/4.1.1-r0/image/usr/bin” folder
```
       $ adb push <yocto build directory>/tmp-glic/work/armv7ahf-neon-oe-linux-gnueabi/tesseract/4.1.1-r0/image/usr/bin/tesseract  /usr/bin/.
```
- **Note**: while building tesseract-lang package, it will create the tessdata folder, inside this contains trained data for all languages. For our implementation purpose, we use english. copy only that particular trained data file.
```
        $adb push share/tessdata/eng.traineddata      /data/tesseract/tessdata/.
```

### Steps to build and run the application: 
**Step-1** : Initialize the terget board with root access
```
        $ adb root
        $ adb remount
        $ adb shell mount -o remount,rw /
```
**Step-2** : Push the source file on the target:
Download the source repository
```
         $ git clone <source repository>    
         $ cd  <source repository>  
         $ adb push detection.py /data/tesseract/ 
         $ adb push images/  /data/tesseract/
```
**Step-3**:   Execute the python script in the target environment.
            To start the application, run the below commands on the qcs610 board, 
```
    $ adb shell
    /# 
```
Export the shared library path to the LD_LIBRARY_PATH
```
        /# export LD_LIBRARY_PATH= $LD_LIBRARY_PATH:/data/tesseract/lib/
        /# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/data/cv2/
        /# cd data/tesseract/
        /# export TESSDATA_PREFIX=/data/tesseract/tessdata/
```
**Step-4** : Execute the python code on the target board,
   
   - perform detection from input image use below command
```
       /# python3 detection.py --image images/KL05AB7000.jpg
```
   - perform detection from camera frame use below command
```
       /# python3 detection.py --camera True
```
  - recognize number plate will be displayed on the terminal.
