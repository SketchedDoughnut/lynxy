# Table of contents
[Client setup](./lynxy.md#client-setup) <br>
[Configuring your client](./lynxy.md#configuring-your-client) <br>
[Starting your client](./lynxy.md#starting-your-client) <br>
[Client communication function explanations](lynxy.md#client-communication-function-explanations) <br>
[Client to server usage](./lynxy.md#client-to-server-usage) <br>
[Other functions](./lynxy.md#other-functions)
***




# Client setup
To set up the client module, you first need to import it. <br>
`import lynxy` <br>
Next, there is some customization you can do. However, if you want to just start the client, skip to "Starting your client"

***
# Configuring your client <br>
The client has some parameters that can be overriden. These are:
- the ports it attempts to connect to
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
`lynxy.override_ports([12345, 67890, 17390])`
**NOTE**: YOU MUST HAVE PORTS ON THE CLIENT AND THE SERVER THAT ARE THE SAME, SO THAT THEY CAN FIND EACH OTHER


**Overriding prints** <br>
If you don't want any console message to be printed, use the following command: <br>
`lynxy.disable_print()` <br>
If you want to enable printing, use the following command: <br>
`lynxy.enable_print()` <br>
**NOTE**: Prints are disabled by default.



***
# Starting your client
To start your client, all you need to do is call one function, passing in the ip of the server. In this example, we use a loopback address: <br>
- `lynxy.start_client('127.0.0.1')`
  **ARGS: None -> returns bool on status of connection**
    - To get the servers ip, please refer to the server setup page, specifically the section named ["Starting the server"](lynxy_server.md#starting-the-server). This IP should be distributed to anyone with the code containing the lynxy client code.
 
***
# Client communication function explanations
This section is dedicated towards explaining the functions that the lynxy module has.
- `lynxy.submit_username_data()` 
  - **ARGS: username: str -> returns string from server**
  - **NOTE: Please refrain from using spaces in your username.**
  - This is a function meant for submitting username data to the server, to be logged.
- `lynxy.request_username_data()`
  - **ARGS: username: str -> returns list from server**
  - **NOTE: Please refrain from using spaces in your username.**
  - This is a function meant for requesting data (ip, port) associated with a username (a username being submitted from ones client using `lynxy.submit_username_data()`). The client will attempt to fetch the data associated with that username. The goal of this function is to use this function to get the data about the other player / client you want to connect to, so you can direct connect to them. It returns a list, with list[0] being the ip and list[1] being the port.
- `lynxy.send_msg()`
  - **ARGS: message: str, recieve: bool = True -> returns string from server**
  - This is a function meant for general communication to whoever is on the other end. While the first two functions are meant specifically for server communication, this function is meant for communicating with whoever you are connected to (server, another client, etc). When communicating with the server, the recieve argument needs to be True (it is, by default). However, when communicating with another client, this can be toggled on or off depending on what your intent is.

***
# Client to server usage
To find information about how to use the client to communicate with the server, go to the ["Server functions key"](lynxy_server.md#server-functions-key) section of the server setup page!

<!-- ***
# Client to client usage
If you want to communicate to another client using this client, it is easy! Here are the steps.
- First, end your current session with the server if you have not already.
  - `lynxy.send_msg('end_session', recieve=True)`
    - This ends the communication channel with the server gracefully
  - `lynxy.shutdown_client()`
    - This can be called without the above function, but it is preferred if you do both. This completely closes the client.
- Override the ports with a list of one int, that being the port of your target client. In this case, pretend 12345 is our target clients port.
  - `lynxy.override_ports([12345])`
- Start the client with your target clients ip. in this example, we use a loopback ip.
  - `lynxy.start_client('127.0.0.1')`
- Communicate with the other client!
  - To send strings,
    - `lynxy.send_msg(msg)`
      - if you want to immediately recieve a message back from the other client, set the optional flag of recieve to True.
        - `lynxy.send_msg(msg, recieve=True)`
  - To send files,
    - this feature is not yet available, sorry! -->



***
# Other functions
- `lynxy.get_data()` -> Will return the following data in a dictionary:
  - the ip the client is connected to (string)
  - the port the client is connected to (int)
- `lynxy.shutdown_client()` -> will shutdown the client, and return a bool telling you whether it worked or not. Server-side, there is error handling to account for this.
- `lynxy.help()` -> has an optional argument, if it is set to True it will open a link to the Github page for this project. Otherwise, it will return a link to that page.
- `lynxy.license()` -> has an optional argument, if it is set to True it will open a link to the license page on the Github for this project. Otherwise, it will return a link to that page.
- `lynxy.credits()` -> will return a string containing information about the credits for this project.