# how_to_conneсt_to_gcp

Ubuntu is supposed to be used.
To connect to the cloud you need to add your own variable with the value to the environment of variables:
**"export GOOGLE_APPLICATION_CREDENTIALS="/current/folder/with/token.json"**
in our case we use the created test token:
**"export GOOGLE_APPLICATION_CREDENTIALS="/home/kot/Desktop/CloudToken.json"**
Accordingly, we put the token file at the desired address.

Commands are presented below:

1. Opening the command shell file:
   *sudo nano .bashrc*

2. Using the command shell file:
   sourse ~/.bashrc

Now just run the script, after which it will automatically load data from the GCS segment.

P.S. The script loads files in the place where it is located.