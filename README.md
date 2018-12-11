# BME 590 Final Project: Image Processor

## DEMO VIDEO
The following link will take you to a video demoing the functional features of our image processor.
[![Image processor demo video](http://img.youtube.com/vi/M5GgaO1uSFc/0.jpg)](https://www.youtube.com/watch?v=M5GgaO1uSFc& "Image Processor Demo")
[![Build Status](https://travis-ci.org/matthew-huber/bme590final.svg?branch=master)](https://travis-ci.org/matthew-huber/bme590final)

## SETUP
The Image processor can be run on your local machine by running the command `python image_processor_gui`. This is the main file that acts as the interface through which the user can use the tool. The file `image_processor_gui` is supported by/needs the files `image_processor`, `img_db`, `image_processor_server`, and the included modules to run. There are several files in this repository that test the program to make sure everything is working as expected, but are not required for the basic operation of the image processor. 
To use this project, you can simply clone the repository, install the requirements specified in requirements.txt in a virtual environment, and simply run `python image_processor_gui.py` from the command line.
## HOW IT WORKS
The image processor starts with the graphical user interface on the **Specify User** tab. Here the user inputs their username or selects an existing username then hits enter to advance to the **Process Image** tab. 

In the **Process Image** tab the user can open files on their computer to be processed. This done by clicking the open file button. When the button is clicked a file selector appears which has filters to limit the files that can be opened to only files with image extensions. 

Now that the file(s) are selcted the GUI displays the selected images in the display. The image that is selected first is displayed originally, however if there are multiple files then the user can click the prev and next buttons to cycle through all of the uploaded images. Once the user has verified that the correct images are selected, a dropdown menu can be used to select one of four image processing options. These options include histogram equalization (default option), contrast stretching, log compression, and reverse video. With the processing option and the files selected, the process button can be triggered to send the files and key information to the server for processing.

The server is contained in the file `image_processor_server` and is currently being hosted on a duke virtual machine : 
vcm-7314.vm.duke.edu, port: 5000, using gunicorn to host a production server. When the files reach the server they are encoded in base64. Therefore, the first image processing step is to decode each image from base 64 and place the data in numpy arrays for further processing. The selected processing algorithm is applied to the image, and all the needed metadata from the images are harvested into data structures. The processed images and key data are then placed into a dictionary so the can be sent back as a json to the GUI. The key metadata information, such as the username, file, and processing characteristics, are saved into the database for this project. The primary id for the database objects is the image filename with the username appended. In the server code the database is accessed multiple times through GET requests initiated by the GUI to provide up-to-date information on the images in the database.

Once the information from the server is sent back to the GUI, the dictionary with the information is unpacked. The most important piece of info from this dictionary is the processed image list. This contains all the processed images encoded in base64. The first step is to decode these base64 processed images to numpy arrays so they can be displayed by the GUI. In the GUI, the processed images are displayed next to the original images. With processed images available, it becomes possible to download and save images. If multiple images were processed, both the download and download all buttons are enabled. In addition, the option to download images as a zip file appears for multiple images. Clicking the prev and next buttons still jumps through the images, allowing for easy comparision between the original and process image. The last button that can be activated on the main tab of the gui is the view histogram button, which sends the GUI to the otherwise disabled **Color Intensity** tab. In this tab, the user can see the pixel histograms for each channel in the image before and after processing. It serves as a check that the processing was done correctly.

The **Manage Images** tab allows the user to see metadata for any image they have ever processed in the database. It also gives the option to remove an image they have processed from the database. 

## EXTRA FEATURES
* Username tab: allows user to specify username or select from previous users
* Ability to download multiple files (both zipped and unzipped)
* Manage image tabs were full processed image history can be viewed or erased
* Server deployed with gunicorn so production level loads can handled by our server
* Enabling and disabling of buttons and features on the GUI to guide the user in correct usage
* Aesthetically pleasing and functional layout of the gui which scales buttons and images with resizing of the window. 
