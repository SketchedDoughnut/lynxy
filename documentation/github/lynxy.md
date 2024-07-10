<!-- table of contents -->
# Table of contents
[Home](https://github.com/SketchedDoughnut/lynxy) <br>
[Client setup](./lynxy.md#client-setup) <br>
[Customizing your client](./lynxy.md#customizing-your-client) <br>
[Starting your client](./lynxy.md#starting-your-client) <br>
[Function explanations](lynxy.md#function-explanations) <br>
[Client to server usage](./lynxy.md#client-to-server-usage) <br>
[Other features](./lynxy.md#other-features)


***


<!-- client setup -->
# Client setup
To set up the client, you first need to import lynxy. <br>
-     import lynxy
Next, there is some customization you can do. However, if you want to just start the client, skip to ["Starting your client"](./lynxy.md#starting-your-client)


***


<!-- info on customizing client features -->
# Customizing your client <br>
The client has some parameters that can be overriden before it is started. These are:
- the ports it attempts to connect to
- whether the program prints or not

<!-- information on overriding ports -->
**Overriding ports** <br>
The server has a default list of ports it will try to connect to. These can be found [**here!**](./shared/ports.md) <br>
It cycles through these ports so that if one is not available, it can still launch itself. You can override these ports by running the function below, and passing in a list with one or more ports (in integer form). There is no limit for how many ports you can pass into it. In this example, we use three random ports: <br>
**NOTE:** YOU MUST HAVE PORTS ON THE CLIENT AND THE SERVER THAT ARE THE SAME, SO THAT THEY CAN FIND EACH OTHER
-     lynxy.override_ports([12345, 67890, 17390])

<!-- information on overriding prints -->
**Overriding prints** <br>
**NOTE**: Prints are disabled by default. <br>
If you don't want any console message to be printed, use the following command:
-     lynxy.disable_print()
If you want to enable printing, use the following command:
-     lynxy.enable_print()


***


<!-- information on starting client -->
# Starting your client
To start your client, all you need to do is call one function, passing in the ip of the server as a string. In this example, we use a loopback address:
-     lynxy.start_client('127.0.0.1')
  - **ARGS:**
    - ip: str
      - To get the servers ip, please refer to the server setup page, specifically the section named ["Starting the server"](lynxy_server.md#starting-the-server). This IP should be distributed to anyone with the code containing the lynxy client code. <br>
  - **RETURNS**
    - connection status: bool
 

***


<!-- explenations for other functions -->
# Function explanations
This section is dedicated towards explaining the functions that lynxy has.

-     lynxy.submit_username_data()
  - **ARGS**
    - username: str
  - **RETURNS**
    - status code: str
  - This is a function meant for submitting username data to the server, to be logged.
  - **NOTE**: Please refrain from using spaces in your username.

-     lynxy.request_username_data()
  - **ARGS**
    - username: str
  - **RETURNS**
    - requested info: list
  - This is a function meant for requesting data (ip, port) associated with a username (a username being submitted from ones client using `lynxy.submit_username_data()`). The client will attempt to fetch the data associated with that username. The goal of this function is to use this function to get the data about the other player / client you want to connect to, so you can direct connect to them. It returns a list, with list[0] being the ip and list[1] being the port.
  - **NOTE**: Please refrain from using spaces in your username.
  
-     lynxy.send_msg()
  - **ARGS**
    - message: str
    - recieve: bool = True
  - **RETURNS**
    - status code: str (if recieve = True)
  - This is a function meant for general communication to whoever is on the other end. While the first two functions are meant specifically for server communication, this function is meant for communicating with whoever you are connected to (server, another client, etc). When communicating with the server, the recieve argument needs to be True (it is, by default). However, when communicating with another client, this can be toggled on or off depending on what your intent is.

***
# Client to server usage
To find information about how to use the client to communicate with the server, go to the ["Server functions key"](lynxy_server.md#server-functions-key) section of the server setup page! <br>
**NOTE**: If the server goes offline, the client is not notified and the connection is terminated. For this reason, please put anything interacting with the server (sending / recieving data) in a try and except, and try to catch the errors, to make the code cancel more gracefully.
***
# Other features
- `lynxy.get_data()` -> Will return the following data in a dictionary:
  - the ip the client is connected to (string)
  - the port the client is connected to (int)
- `lynxy.shutdown_client()` -> will shutdown the client, and return a bool telling you whether it worked or not. Server-side, there is error handling to account for this.
- `lynxy.help()` -> has an optional argument, if it is set to True it will open a link to the Github page for this project. Otherwise, it will return a link to that page.
- `lynxy.license()` -> has an optional argument, if it is set to True it will open a link to the license page on the Github for this project. Otherwise, it will return a link to that page.
- `lynxy.credits()` -> will return a string containing information about the credits for this project.
