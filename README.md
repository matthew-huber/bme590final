# bme590final

[![Build Status](https://travis-ci.org/matthew-huber/bme590final.svg?branch=master)](https://travis-ci.org/matthew-huber/bme590final)

SETUP: The Image processor can be run on your local machine by running the command, python image_processor_gui. This is the main file that acts as the interface through which the user can use the tool. The file image_processor_gui is supported/ needs the files image_processor, img_db, image_processor_server, and require modules to run. There are also several files that test the program to make sure everything is working as expected. 

HOW IT WORKS: The image processor starts with the graphical user interface. Here the user inputs their username or selects an existing username then hits enter to advance to the next page. 

Once the next tab is reached the user can open files on their computer to be processed. This done by clicking the open file button. When the button is clicked a file selector appears and has filters to limit the files that can be opened to only files with image extensions. 

Now that the file/ files are selcted the GUI displays the selected images in the display. The image that is selected first is display originally, however if there are multiple files then the user can click the prev and next buttons to cycle through the selected images. Once the user verifys that they selected the right images they use a drop menu to select one of four image processing options. These options include histogram equalization, contrast stretching, log compression, and reverse video. Lastly, now that all options and files are selcted the user can hit the process button to send the files and key information to the server for processing.

The server is contained in the file image_processor_server file and is currently being hosted on a duke virtual machine : 
vcm-7314.vm.duke.edu, port: 5000, using gunicorn to host a production server. When the files reach the server they are encoded in base64 so the first step to processing them is decoding them from base 64 and putting the images into numpy arrays so they can be processed. The images are then processed and all needed meta data from the images is harvested into data structures. The processed images and key data are then placed into a dictonary so the can be sent back as a json to the GUI. Also on the server, the key info like username, filename, and image metadata are saved into the database for this project. The primary id for the database objects is the imagename. In the server code the database is accessed multiple times in get requests to support features in the GUI with the latest information. 

Once the information from the server is sent back to the GUI, the dictonary with the information is unpacked. The most important piece of info from this dictonary is the processed image list. This contains all the processed images encoded in base64. The first step is to decoded these base64 processed images to numpy arrays so they can be displayed in pyqt. The first thing that happens is the processed image is displayed next to the orignal image in GUI. Then the download lights up, since, it can now be clicked. If multiple images were clicked than both the download and download all button lights up; since, both can now be used. In addition the download as a zip file option appears for multiple images and the original and processed image are in sync when the prev and next button are hit, to allow for easy image comparsion. The last button that can be activated on the main tab of the gui is the view histogram for this image button. Clicking this button lets the user see the pixel histograms for each channel in the image before and after processing. It serves as a check that the processing was done right.

The next tab is the manage image tab. This tab allows the user to see meta data for any image they have ever processed in the database. It also gives the option to remove an image they have processed from the database. 

EXTRA FEATURES: Username tab, zip together multiple files on download, manage image tabs were full processed image history can be viewed, server deployed with gunicorn so production level loads can handled by our server, and very nice looking and functional layout of the gui (scales). 
