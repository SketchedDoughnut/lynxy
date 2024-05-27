# Table of contents
[Client setup](./lynxy.md#client-setup) <br>
[Configuring your client](./lynxy.md#configuring-your-client) <br>
[Starting your client](./lynxy.md#starting-your-client) <br>
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




# Starting your client
To start your client, all you need to do is call one function, passing in the ip of the server. In this example, we use a loopback address: <br>
- `lynxy.start_client('127.0.0.1')`
    - To get the servers ip, please refer to the server setup page. This IP should be distributed to anyone with the code containing the lynxy client code.
 
 # Client to server usage
 To find information about how to use the client to communicate with the server, go to the "Server functions key" section of the server setup page. Or, click the link below!
 [I'm a link!](lynxy_server.md#server-functions-key)


# Other functions
- `lynxy.get_data()` -> Will return the following data in a dictionary:
  - the ip the client is connected to (string)
  - the port the client is connected to (int)
- `lynxy.shutdown_client()` -> will shutdown the client, and return a bool telling you whether it worked or not. Server-side, there is error handling to account for this.