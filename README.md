in client folder:

npm install

npm run build

npm run **serve**



in server folder:

python3 -m venv env 

pip3 install -r requirements.txt 

source env/bin/activate 
(每次重新打开可能需要这个命令)

python3 app.py      



Demo Readme: 

the demo is consist of the front-end(vue) and back-end(flask), the front-back end communication is realized by the asio library. 



Loose Configured Readme
for contour_detection.py

1. preprocessing:
   1. Binary image is created by opencv::cvtColor and opencv::threshold functions
   2. Contour is found by the opencv::findcontours function
   3. contour selection is finished by area thresholding.
   
2. Blur removal and contour extraction:
   1. Gaussian blur is done to remove the blue on the edge of the contour.
   2. the combination of dilation and erosion is done before extraction by the opencv::dilate and opencv::erode
   3. skeleton extraction and distance(width) measurement is done by the morphology::medial_axis function

3. Width Infomation Collection
   1. skeleton point and corresponding distance is assigned to each contour by opencv::pointPolygonTest
   2. average and variance is calculated by numpy.

