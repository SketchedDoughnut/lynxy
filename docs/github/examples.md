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

3. We want to set up events for different things if they happen. These can be helpful for triggering functions when needed. Each function has the type there as to make it easier to understand what is being passed in. More information about types can be found [here](/docs/github/data.md).

        @client.event(lynxy.Constants.Event.ON_CONNECT)
        def my_function(connect_state: boolean):
                print(input)

        @client.event(lynxy.Constants.Event.ON_MESSAGE)
        def my_function(message: lynxy.Pool.Message):
                print(message.content)

        @client.event(lynxy.Constants.Event.ON_CLOSE)
        def my_function(error: lynxy.Exceptions.BaseLynxyException | None):
                print(error)

4. In order to send data, we can use the send function. This can send anything, and the data sent will be pickled then encrypted. When data is sent, Lynxy will take that and form it into a `lynxy.Pool.Message` object, setting the timestamp for when it `created_at`. The `recieved_at` is set on the recieving end before triggering the `ON_MESSAGE` event.

        data = 'hello!'
        client.send(data)
        '''
        data -> lynxy.Pool.Message 
        attributes:
                - created_at
                - recieved_at
                - content
        '''