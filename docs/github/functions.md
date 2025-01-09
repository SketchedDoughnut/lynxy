# Functions
- [Main Github page](https://github.com/SketchedDoughnut/lynxy)
- [Home](/README.md)

***

Here you can find information about the variety of functions that Lynxy offers.

The functions that are immediately available are the ones picked that are meant for public use. These are the only ones that this page will be covering. The rest of the functions can be found if, after making your Lynxy instance, you go into the `_comm` class instance.
    
    inst = Lynxy()
    inst._comm

Within `_comm`, there are instances of the parser and encryption classes.

    inst._comm.parser # for parser
    inst._comm.sec # for encryption

It is advised to not mess with the things here unless you know what you are doing. Thanks!

***

# Classes
**Lynxy: Class**: Makes your Lynxy class instance, allowing you to use your client. This is essential for setup. 

***

# functions
**get_host: Function**: Gets host information of host machine.

**get_actual_target: Function**: Gets the actual target information, which depending on variables during connecting can have a different port than the initial one used for connecting.

**config_heartbeat: Function**: Sets the heartbeat settings for maintaining a connection even if the client is not sending any data.

**set_connection: Function**: Sets how Lynxy will manage the connection closing when it occurs, regardless of if it is an intendec closure or not.

**connect: Function**: Connects to the target machine. Also automatically runs the recv function unless specified otherwise. Uses RSA assymetrical encryption keys to exchange a 128-bit AES encryption key which is used for main data encryption.

**close: Function**: Closes the connection to the target machine.

**send: Function**: Sends data of any size to the target machine, encrypted with the 128-bit AES encryption key.

**recv: Function**: Starts the background thread for recieving data.

***

# Decorators
**event: Decorator**: Used as a decorator to set up functions to be triggered when events happen. Needs to be called on as a decorator function in order to configure what event you are subscribing to.