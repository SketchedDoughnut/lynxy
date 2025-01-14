# Examples
- [Main Github page](https://github.com/SketchedDoughnut/lynxy)
- [Home](/README.md)

***

Here is an example for setting up a Lynxy client, as well as some usages.

1. First. we want to set up your client. It is advised to keep the IP the same, but you can change it if you want. As for the port, any port will work but the default one can be used (and is, in some ways, easier). In this example, Bind is set to True, but you don't have to do that

        import lynxy
        client = lynxy.Lynxy(bind=True)

2. Now, we want to connect to the target machine. For this, we will assume it is another Lynxy client

        target = ['123.456.78.910', 12345]
        lynxy.connect(target)