# Table of contents
[Server setup](./lynxy_server.md#server-setup) <br>
[Configuring your server](./lynxy_server.md#configuring-your-server) <br>
[Starting the server](./lynxy_server.md#starting-the-server) <br>
[Server response key](./lynxy_server.md#server-response-key) <br>
[Server functions key](./lynxy_server.md#server-functions-key) <br>
[Other functions](./lynxy_server.md#other-functions) 

***
# Introduction
The main part of this server acts as a database. There are settings you can configure before lanching the server. When clients connect, they can submit a username that gets associated with their info (ip, port). Then, other users can request the data associated with that username. Finally, clients are able to directly connect to each other using that information. <br>
But this is only the foundations. There is other modes you can put the server into, if you want! Given.. I remember to implement those features.. 😅

***
# Server setup
To set up the server module, you first need to import it. <br>
`import lynxy_server` <br>
Next, there is some customization you can do. However, if you want to just start the server, skip to "Starting your server"











<!-- Instructions on how to configure the server -->
***
# Configuring your server <br>
The server has a couple of parameters that can be overriden. These are: 
- the ports it attempts to connect to
- the IP it tries to run on 
- whether the program prints or not
<br><br>

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
<br><br>

**Overriding IP** <br>
The server uses the ipv4 IP of the device it is running on. It is advised to not change this. However, if you want to override the IP, you can use the following function, inputting a string. <br>
`lynxy_server.override_ip("123.456.789.0")`
<br><br>

**Overriding prints** <br>
If you don't want any console message to be printed, use the following command: <br>
`lynxy_server.disable_print()` <br>
If you want to enable printing, use the following command: <br>
`lynxy_server.enable_print()` <br>
**NOTE**: Prints are enabled by default.
<!-- <br><br>

**Creating custom functions** <br>
The server has the ability to execute a custom function, if you choose to create one. The server's code to communicate with the client runs in a while loop, only exiting when the client disconnects, there is an issue, or the server is remotely told to by an authorized user. When creating your own function, there are some rules you need to follow.
- Your function HAS to take two inputs, both strings. One is the message the server recieves, and the other is the address of the client. Additionally, your function must return a string telling the server what to do once your function is done. There are 4 possibilities.
  - "exit"
    - will make the server severe its current connection with the client
  - "continue"
    - will make the loop restart again
  - "break"
    - will break out of the current loop
  - anything else
    - nothing will happen
- Example function
  - `def foo(message: str, addr: str) -> str`  -->
<br>

**Overriding other features** <br>
There are a couple of other things you can ovverride. These are variables you can set. You can change all of them directly. For example, `(var) = True`, or `(var) = False`.

`limit_username`
  - This boolean decides whether or not the server will limit the client to only being able to submit a single username to the server.

`overwrite_usernames`
  - This boolean decides whether the client can override a username that already exists in the database.

`clear_dead_usernames`
  - This boolean decides whether the server will clear usernames (and the data associated with them) from the database when the client disconnects / crashes.








<!-- Instructions on how to start the server -->
***
# Starting the server
To start your server, you have a couple of options. Here is the rundown: <br>
- `ip, port, token = lynxy_server.start_server()`
  - This option will not block your code, as it will run the server in a seperate thread. This allows for use of functions such as `lynxy_server.get_data()`, and more.
  - If you disable print and then call on this function, absolutely nothing will be printed. You can get the IP the server is on, the port the server is on, and the session token from `lynxy_server.get_data()`. Alternatively, `lynxy_server.start_server()` returns a tuple containing all of these (in respective order) which you can also use to get data from. Clients will need the IP address to connect to the server, and if you want to remotely control the server then you will also need the session token. Usage of this token is elaborated on more in the client setup page.
  - **PLEASE NOTE**: If you use this function, and there is no code continuing after it, the file will finish. This means that the server will get terminated. To prevent this, please include some sort of loop system AFTER calling the function that keeps the file in which you called on this function active, as to not close the server.
- `lynxy_server.no_thread_start_server()`
  - This option will block your code, as it is directly running the server. This does not allow for any code to run after this function is called, until the server goes offline. The server will only go offline if it crashes, or if someone remotely shuts it down by authorizing their user, and then commanding the server to shut down. This is explained more in the client setup page, and the shutdown feature is explained below. <br>

**BEFORE CONTINUING**: Check the IP your server is on. If it is on an ip such as 127.0.0.1, then it will not work. You need the public ipv4 address of the device running the server, typically labeled with "LAN" or something of the sort.
 
***
# Server response key
The server has a variety of numbers it will return as responses to actions. Codes from 0 to 99 are status codes. Codes from 100 to 199 is regarding invalid messages from the clients. Codes from 200 to 299 are regarding system settings, set by an authorized client. These include being denied if you do not have the right permissions.
The key is below. 
- 000
  - the operation was successful
- 001
  - the server failed to do an operation
- 002
  - the client requested to end the communication channel with the server
- 003
  - the message the the client sent to the server is not connected to any command, and so it did nothing
- 004
  - The session between the server and client crashed
- 100
  - the client requested data associated with a username that does not exist
- 101
  - the user tried to authorize themself, but had an invalid auth token
- 102
  - the user has not been authorized, and can not do what they just tried to
- 103
  - The message is invalid (meaning it is empty or corrupt in some way)
- 104:
  - You have already registered a username on the server for this client instance
- 105:
  - The username you are trying to submit to the database has already been submitted
- 200
  - the server has been commanded to deny every client that connects to it





***
# Server functions key
There are set commands that one can send to the server, from the client. They are as follows. <br>
**NOTE**: The functions used here are: `lynxy.submit_username_data()`, `lynxy.request_username_data()`, `lynxy.send_msg()`.
These functions are elaborated on more in the client setup page, but what you do need to know is that they all return data.

- **username (name)**
  - This argument submits a username to the server database. Example usage is below.
    - `lynxy.submit_username_data('SketchedDoughnut')`
    - or `lynxy.send_msg('username SketchedDougnut')`
  - **NOTE**: NO SPACES ARE ALLOWED, AND WILL BE REMOVED FROM YOUR USERNAME UPON SUBMISSION

- **request_by_user (name)**
  - This argument requests the data (data being IP, port) associated with a username that is pre-existing in the servers database. Example usage is below.
    - `lynxy.request_username_data('SketchedDoughnut')`
    - or `lynxy.send_msg('request_by_user SketchedDougnut' )`
  - **NOTE**: NO SPACES ARE ALLOWED, AND WILL BE REMOVED FROM YOUR USERNAME UPON SUBMISSION

- **auth (token)**
  - This argument attempts to authorize the client. If the token is equal to the session token generated on the servers start, then the client will be authorized. Example usage is below.
    - `lynxy.send_msg('auth (token)' )`

- **clear_client**
  - If the user is authorized, this argument will clear the client dictionary. This is helpful if, for some reason, you would need to reset it. Example usage is below.
    - `lynxy.send_msg('clear_client' )`

- **freeze_server**
  - If the user is authorized, this function will freeze the server. This will either make the server not exist for new clients, and/or severe the current connections with the clients. This function is intended for use if someone does not have direct access to the computer itself, or if you are running the server with `lynxy_server.no_thread_start_server()`. The reason why is because if you run the server directly instead of via a thread, you would not be able to call on the dedicated function for freezing the server, as your code would be blocked. This is a get-around to that. Example usage is below.
    - `lynxy.send_msg('freeze_server' )`

- **end_session**
  - This argument ends the session between the client and the server. Example usage is below.
    - `lynxy.send_msg('end_session' )`









***
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
- `lynxy_server.help()` -> has an optional argument, if it is set to True it will open a link to the Github page for this project. Otherwise, it will return a link to that page.
- `lynxy_server.license()` -> has an optional argument, if it is set to True it will open a link to the license page on the Github for this project. Otherwise, it will return a link to that page.
- `lynxy_server.credits()` -> will return a string containing information about the credits for this project.
