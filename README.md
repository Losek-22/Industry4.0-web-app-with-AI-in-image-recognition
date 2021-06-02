# Industry4.0-web-app-with-AI-in-image-recognition
## The project has been stopped

Developed as a startup idea in cooperation with promoter at Warsaw University of Technology.

Main technologies used:
Python Django
IBM Cloud API
SQLite

The site uses user accounts, and requires a login:

![image](https://user-images.githubusercontent.com/55858107/120470273-a3cae200-c3a3-11eb-9d2b-5d22343e60ca.png)

The main functionality was designed to allow users and administrators with following permissions:

Administrators:

1) Ability to train a Visual Recognition DL algorithm by uploading the files through the site, which then would be uploaded to IBM Watson and fed to a model. The main idea was to allow a person create good DL algorithms without the extensive knowledge required to do so. The idea was to allow higher management in industrial plants to create tools for untrained employees to enable them to solve simple issues which required taking a look at an object (such as manufacturing imprefection). The site is designed to classify an image taken with a phone, detect what's wrong and offer possible solutions to try before taking an engineer's time.

![image](https://user-images.githubusercontent.com/55858107/120470901-6024a800-c3a4-11eb-8de8-43bdc87dd252.png)

![image](https://user-images.githubusercontent.com/55858107/120469812-23a47c80-c3a3-11eb-8701-f1404dd2a98d.png)

![image](https://user-images.githubusercontent.com/55858107/120469962-4a62b300-c3a3-11eb-89e6-1c199a8e095d.png)

![image](https://user-images.githubusercontent.com/55858107/120470699-2489de00-c3a4-11eb-87b3-4e223d5fed08.png)

2) Ability to add .pdf files for easy access for technicians (such as machinery documentation needed during maintenance or unplanned manufacturing breaks). (not yet finished)

3) Ability to create forms which automatically connect to an SQLite database which allow user to remotely collect readings from machinery, without the need to write them down on a piece of paper and retyping them into a computer at the desk. (partially finished)

![image](https://user-images.githubusercontent.com/55858107/120469714-02dc2700-c3a3-11eb-91cc-a04d7e78c903.png)

4) Much more planned, but we never got to that point.

Users:

1) Using the Visual Recognition algorithms created by administrators to perform basic tasks which they were not taught to do by a human being. The idea is to output a solution to a problem which is recognised on a picture. In the picture below you can see a list of available classifiers (example given is "chair assembly", which would tell the worker clues on how to install each element given its picture). The idea down the line was to eliminate the need to choose a classifier alltogether, and instead use an IBM Cloud functionality designed for it, but we never got to that point. As seen on the picture, the classifier name is greyed out and has an appendix "BEING_TRAINED", which means IBM Watson marked the state of this classifier as such.

![image](https://user-images.githubusercontent.com/55858107/120470406-c52bce00-c3a3-11eb-8a9c-67add2ef1c56.png)

2) Using .pdf library. (not yet finished)
3) Measurement data input to an SQLite database.
4) More planned

Summing up, the startup was rejected because it was not in ready-to-use state. It waits for a day to be picked up again when I'm done with university.
