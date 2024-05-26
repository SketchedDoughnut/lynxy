# Server setup
To set up the server module, you first need to import it. 
`import lynxy_server` <br></br>
Next, there is some customization you can do. However, if you want to just start the server, skip to "Starting your server"











<!-- Instructions on how to configure the server -->
***
**Configuring your server** <br></br>
The server has a couple of parameters that can be overriden. These are: 
- the ports it attempts to connect to
- the IP it tries to run on 


**Overriding ports** <br></br>
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

It cycles through these ports so that if one is not available, it can still launch itself. You can override these ports by running the function below, and passing in a list with one or more ports (in integer form). There is no limit for how many ports you can pass into it. In this example, we use three random ports. <br></br>
`lynxy_server.override_ports([12345, 67890, 17390])`


**Overriding IP** <br></br>
The server uses the ipV4 IP of the device it is running on. It is advised to not change this. However, if you want to override the IP, you can use the following function, inputting a string. <br></br>
`lynxy_server.override_ip("123.456.789.0")`


**Overriding prints** <br></br>
If you don't want any console message to be printed, use the following command: <br></br>
`lynxy_server.disable_print()` <br></br>
If you want to enable printing, use the following command: <br></br>
`lynxy_server.enable_print()`











<!-- Instructions on how to start the server -->
***
**Starting the server** <br></br>
To start your server, you have a couple of options. If you just want to start the server without any additional work, use: <br></br>
`lynxy_server.start_server()` <br></br>