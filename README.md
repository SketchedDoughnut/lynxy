# **lynxy**
Local (yielding?) Network (eXchange?) (the extra y is cosmetic~)

# **Introduction**
lynxy, also known as lynx, is a LAN server-client system coded in Python. It allows for easy setup of a server, as well as easy setup for clients on the same network as the server. 
The first section will explain instructions that apply to both, and then we will cover each individual part.

# **Setup**
Before we do anything, you should first install this module with pip. <br></br>
`pip install (TBD)`
`python3 -m pip install (TBD)` <br></br>
When you do this, it will install both the modules "lynxy" and "lynxy_server". Once this is done, you are ready to read the instructions on the following sections about setting up your client, server, or both.











***
<!-- <br></br> -->
<b>Server setup</b> 

To set up the server module, you first need to import it. 
`import lynxy_server` <br></br>
Next, there is some customization you can do. However, if you want to just start the server, skip to "Starting your server"

<!-- <br></br> -->
<b>Configuring your server</b>

The server has a couple of parameters that can be overriden. These are: 
- the ports it attempts to connect to
- the IP it tries to run on 

<!-- <br></br> -->

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

<!-- <br></br> -->

**Overriding IP** <br></br>
The server uses the ipV4 IP of the device it is running on. It is advised to not change this. However, if you want to override the IP, you can use the following function, inputting a string. <br></br>
`lynxy_server.override_ip("123.456.789.0")`

<!-- <br></br> -->

# Starting the server