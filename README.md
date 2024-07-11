# IMPORTANT: THIS REPOSITORY IS CURRENTLY GOING UNDER RENOVATIONS. THIS INCLUDES SOURCE CODE AND INCLUDED DOCUMENTATION. SORRY!


<!-- title -->
# **lynxy**
<b>Local <br>
(Yielding?) <br>
Network <br>
(eXchange?) <br>
(the extra y is cosmetic~)</b>

***

<!-- introduction -->
# **Introduction**
Lynxy is a LAN server-client system coded in Python. It allows for easy setup of a server, as well as easy setup for clients on the same network as the server.
The use of this module is so that if people were to make programs that require a LAN system, they can use what is provided here as terms for communication for a game, a texting platform, and more! <br>
*This project is also named after my ~ windy ~ friend :3* <br>
The first section will explain instructions that apply to both, and then we will cover each individual part. <br>

***

<!-- general setup -->
# **General setup**
Before we do anything, you should first install this module with pip.
-     pip install lynxy
-     python3 -m pip install lynxy
When you do this, it will install both the modules "lynxy" and "lynxy_server". Once this is done, you are ready to read the instructions on the following sections about setting up your client, server, or both.

***

<!-- information for setting up lynxy_server -->
# Server setup
If you are looking for instructions on how to setup lynxy_server, go [**here!**](./documentation/github/lynxy_server.md)

***

<!-- information for setting up lynxy -->
# Client setup
If you are looking for instructions on how to setup lynxy, go [**here!**](./documentation/github/lynxy.md)

***

<!-- extra info -->
# Etc
<!-- info about official releases -->
**Official release info** <br>
- You can find official releases for lynxy [**here!**](https://pypi.org/project/lynxy/)
- You can view the release changelog for both lynxy and lynxy_server [**here!**](./documentation/github/changelogs/release_changelog.md)

<!-- info about experimental releases -->
**Experimental release info** <br>
- You can find the experimental releases for lynxy [**here!**](https://test.pypi.org/project/lynxy/)
- You can view the experimental changelog for both lynxy and lynxy_server [**here!**](./documentation/github/changelogs/experimental_changelog.md)
  - To install experimental releases, do the following.
  - **NOTE:** FUNCTIONALITY CAN NOT BE GUARANTEED IF YOU ARE USING A EXPERIMENTAL RELEASE. 

    -       pip install -i https://test.pypi.org/simple/ lynxy
    -       python3 -m pip install -i https://test.pypi.org/simple/ lynxy