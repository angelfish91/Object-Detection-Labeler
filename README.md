# Position Labeler
In field of object detection, we need firstly build dataset.
This tool would help you to label the ROI of pictures into VOC format.
Hope you enjoy it.


## Dependency

***python2.7***

***python-opencv***

`http://jingyan.baidu.com/article/f25ef2545714ab482c1b8201.html`

***pandas\numpy***

`pip install pandas`

`pip install numpy`

## Usage：

On terminal, just type:

`python xpos2.py`

HOT KEY

**R**    

refresh the picture and relabel it

**ESC**   

back to last picture and relabel it

**SPACE** 

label it

**C**    

jump to next picture

**Q**    

quit this program & save config.cfg which uesd to configurate the unfished work

when trying to config xPos, keep tmp.pkl & config.cfg at current working path

## Usage Example:

`python xpos2.py --img-path=D:\imgs --nclass=1`

`python xpos2.py --img-path=D:\imgs --nclass=1 --config=1`
