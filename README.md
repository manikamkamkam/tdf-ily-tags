This application is built to simulate the security processes in user data handling procedures. 

The user can register themselves into the system with the register function, then they can start adding their data into the system. If they have registered themselves into the system, they can access the login feature to go into the system to edit and read their data. 

This system DOES NOT allow the users to delete their data from the system. 

To start the application, create a virtual environment (referring to this as venv from now on) to run your python scripts with: 

**WINDOWS**: *venv\Scripts\activate*
**MACOS/LINUX**: *source venv/bin/activate*

While you are in the venv, install the required modules: 
*pip install cryptography* or *pip3 install cryptography*
We will use the cryptography module because it has the required hashing and encrypting tools we need for this application. 

Check that you have installed the cryptography module by typing in:
*pip show cryptography*
This is a step I would not skip as some devices may have the python installed in weird places -> if this is you, use pip3/python3 commands for the download and running of the application. This worked for me as I'm runnning Monterey so you will need to run it on your own to see what works.

After you have verified the module installation, run the application to register your first user:
*python script.py --register* or *python3 script.py --register*

Once you have registered your user, your user will be logged into the system. You can now use the menu functions to navigate.
Option 1: Enter data
Option 2: View data
Option 3: Edit data
Option 4: Logout

There are input checking measures in place to ensure valid inputs.

While in register mode, your user WILL NOT be able to use the 2nd option without first entering their data by using Option 1/3. Once you have entered the data, you may use Option 2.

You can log in to the system by running: 
*python script.py --register* or *python3 script.py --register*
After you have logged in, you still have the same menu options. You are also able to view the data that you have filled in while you were in register mode. 

The data will be encrypted and stored in a JSON file for ease of access and security. Other than that, the user will be logged out of the system after a minute of inactivity. 

If you want to see a live demo, I have linked a YouTube video covering this on my channel.

Have a great day!
