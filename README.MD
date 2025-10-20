# Clark-Milone Telescope New Dashboard

The new informational web dashboard for the Clark-Milone Telescope at the Rothney Astrophysical Observatory.

## Features

- Displays status of the telescope and dome, such as its position and current state (open, moving, etc.)
- Displays current and historical wind direction via a compass rose
- Displays Temperature, Humidity and Pressure line graphs
- Reads from SQM device to display brightness of sky

## Installation

To install this software for development, 
    
1. **Clone the project**
    ```bash
    git clone https://github.com/AdaVoden/cmt_dashboard.git
    ```
2. Move into the project folder
    ```bash
    cd FOLDER_NAME
    ```
3. Install poetry 
    ```bash
    pip install poetry
    ```
4. Install the project 
    ```bash
    poetry install
    ``` 
5. Start the development webserver 
    ```bash
    poetry run pserve development.ini --reload
    ```
    
At this point, the website will run. It requires test data to run from the CMT weather module as a text file.

Simply copy the current "wx.log" from `/usr/local/telescope/comm` on Talon and set the file's location in the `development.ini` file.

## Deployment

This website is currently only in use on `talon.rao.phas.ucalgary.ca`, or "new-talon" as it's known. It is installed to `/var/www/documents/cmt`.

If you wish to update it, make your changes, clone the directory from github and then use the command

```bash
sudo cp -RT /var/www/documents/cmt/ CLONED_FOLDER
```

This will move all the files into the directory, at which point you will need to run to have the changes reflected in the software:

```bash
sudo apachectl restart
```

## License

MIT

## 

