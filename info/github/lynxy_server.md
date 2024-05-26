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
`lynxy_server.override_ports([12345, 67890, 17390])`


**Overriding IP** <br>
The server uses the ipV4 IP of the device it is running on. It is advised to not change this. However, if you want to override the IP, you can use the following function, inputting a string. <br>
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
  - PLEASE NOTE: If you use this function, and there is no code continuing after it, the file will finish. This means that the server will get terminated. To prevent this, please include some sort of loop system that keeps the file calling on this function active, as to not close the server.
- `lynxy_server.no_thread_start_server()`
  - This option will block your code, as it is directly running the server. This does not allow for any code to run after this function is called, until the server goes offline. The only way it will go offline is if it crashes (this might be changed in a future update).
 



# Other functions
- `lynxy_server.get_data()` -> will return the following data in a dictionary:
  - server info
    - if the server is alive or not (bool)
    - the ip the server is on (string)
    - the port the server is on (int)
  - client info (dict)
    - example username (str)
      - (example ip, example port) (tuple)
- `lynxy_server.shutdown_server()` -> will shutdown the server, and return a bool telling you whether it worked or not.