# lazyphoto2

A simple mannga viewer as a python web server. (Worked for python 3.5+)

It search the *.zip files in your mannga folder and make them readable on web browser though local network.

It may be useful if you just want to:

 * Read the files but don't want to unzip them.
 * Keep the files in portable or PC storage.
 * Read the files with other device in local network.

## Warning

The code has NO review on safty issue so use it on your own risk. Test it on backed-up files first. Don't expose the server to untrusted netwrok.

## Usage

Edit the path in server.py with text editor to your mannga folder containing the zip files 

    folderprefix = 'F:/myExt/fu/'
    
Start the server in commandline like this (There is a bat file sample for Windows):

    python server.py [port]

Test if you can read the mannga on your PC browser

    http://localhost:[port]

Now enjoy your mannga in bed with the web browser on your mobile device
    
    http://[your PC ip]:[port]  (For example: http://192.168.1.4:8080)
