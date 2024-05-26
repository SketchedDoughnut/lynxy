# Server setup
To set up the server module, you first need to import it. <br>
`import lynxy_server` <br>
Next, there is some customization you can do. However, if you want to just start the server, skip to "Starting your server"











<!-- Instructions on how to configure the server -->
***
**Configuring your server** <br>
The server has a couple of parameters that can be overriden. These are: 
- the ports it attempts to connect to
- the IP it tries to run on 
- whether the program prints or not


**Overriding ports** <br>
The server has a default list of ports it will try to connect to. These ports are:
1.  11111 
2.  12111 
3.  11211 
4.  11121 
5.  11112 
6.  22111 
7.  12211 
8.  11221 
9.  11122 
10. 22222 

It cycles through these ports so that if one is not available, it can still launch itself. You can override these ports by running the function below, and passing in a list with one or more ports (in integer form). There is no limit for how many ports you can pass into it. In this example, we use three random ports: <br>
`lynxy_server.override_ports([12345, 67890, 17390])` <br>
**NOTE**: YOU MUST HAVE PORTS ON THE CLIENT AND THE SERVER THAT ARE THE SAME, SO THAT THEY CAN FIND EACH OTHER


**Overriding IP** <br>
The server uses the ipv4 IP of the device it is running on. It is advised to not change this. However, if you want to override the IP, you can use the following function, inputting a string. <br>
`lynxy_server.override_ip("123.456.789.0")`


**Overriding prints** <br>
If you don't want any console message to be printed, use the following command: <br>
`lynxy_server.disable_print()` <br>
If you want to enable printing, use the following command: <br>
`lynxy_server.enable_print()`











<!-- Instructions on how to start the server -->
# Starting the server
To start your server, you have a couple of options. Here is the rundown: <br>
- `lynxy_server.start_server()`
  - This option will not block your code, as it will run the server in a seperate thread. This allows for use of functions such as `lynxy_server.get_data()`, and more.
  - If you disable print and then call on this function, absolutely nothing will be printed. You can get the IP the server is on, the port the server is on, and the session token from `lynxy_server.get_data()`. Alternatively, `lynxy_server.start_server()` returns a tuple containing all of these (in respective order) which you can also use to get data from. Clients will need the IP address to connect to the server, and if you want to remotely control the server then you will also need the session token. Usage of this token is elaborated on more in the client setup page.
  - **PLEASE NOTE**: If you use this function, and there is no code continuing after it, the file will finish. This means that the server will get terminated. To prevent this, please include some sort of loop system AFTER calling the function that keeps the file in which you called on this function active, as to not close the server.
- `lynxy_server.no_thread_start_server()`
  - This option will block your code, as it is directly running the server. This does not allow for any code to run after this function is called, until the server goes offline. The server will only go offline if it crashes, or if someone remotely shuts it down by authorizing their user, and then commanding the server to shut down. This is explained more in the client setup page, and the shutdown feature is explained below.
 
# Server response key
The server has a variety of numbers it will return as responses to actions. Codes from 0 to 99 are status codes. Codes from 100 to 199 is regarding invalid messages from the clients. Codes from 200 to 299 are regarding system settings, set by an authorized client. These include being denied if you do not have the right permissions.
The key is below. 
- 0
  - the operation was successful
- 1
  - the server failed to do an operation
- 2
  - the client requested to end the communication channel with the server
- 3
  - the message the the client sent to the server is not connected to any command, and so it did nothing
- 100
  - the client requested data associated with a username that does not exist
- 101
  - the user tried to authorize themself, but had an invalid auth token
- 102
  - the user has not been authorized, and can not do what they just tried to
- 200
  - the server has been commanded to deny every client that connects to it

# Other functions
- `lynxy_server.get_data()` -> This function will only work if you are using the threaded start function, and will return the following data in a dictionary:
  - server info
    - if the server is alive or not (bool)
    - the ip the server is on (string)
    - the port the server is on (int)
  - client info (dict)
    - example username (str)
      - (example ip, example port) (tuple)
- `lynxy_server.freeze_server()` -> will freeze the server, and return a reponse telling you whether it worked or not. Freezing the server means it will render the server unusable, but the file will still be running. This is meant to disable the server until a person can physically access the computer and disable it from there.
