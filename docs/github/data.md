# Objects and data types
- [home](/README.md)

***

This page contains information about the objects Lynxy uses, as well as data types.

***

# Objects
**lynxy.Pool.Message** <br>
Attributes:
- content: data being sent
- created_at: time the object was created, made by doing `datetime.strftime(datetime.now(), "%d/%m/%Y, %H:%M:%S")`
- recieved at: time the object was recieved on the target machine, set by doing `datetime.strftime(datetime.now(), "%d/%m/%Y, %H:%M:%S")`

***

# Data types
Lynxy uses events to trigger functions for when different things happen. Lynxy also attempts to pass inputs to these functions and there is by default, always 1 input. <br>
Note: Event constants can be found in `lynxy.Constants.Event`

**ON_CONNECT**
- Input type: Boolean, `True`

**ON_MESSAGE**
- Input type: `lynxy.Pool.Message`

**ON_CLOSE**
- Input type: Exception from `lynxy.Exceptions`