# Development

To install this software for development, 
    
    1. Clone the project to your desired folder with `git clone git@github.com:RothneyAO/telescope_website.git FOLDER_NAME`
    2. Move into the project folder with `cd FOLDER_NAME`
    3. Install poetry with `pip install poetry`
    4. Install the project with `poetry install` 
    5. Start the development webserver with `poetry run pserve development.ini --reload`
    
At this point, the website will stand up and will try to run. It requires test data to run from the CMT weather module as a text file.

Simply copy the current "wx.log" from `/usr/local/telescope/comm` on Talon and set the file's location in the `development.ini` file.
