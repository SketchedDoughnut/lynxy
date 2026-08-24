**This changelog was started at 6/3/24**
- [Main Github page](https://github.com/SketchedDoughnut/lynxy)
- [Home](/README.md)

***

# v0.0.3 - v0.0.6
**5/28/24 - 6/4/24**
- Releases for the old system of Lynxy, before the full rewrite of Lynxy (>=1.0.0). This version is drastically different then the full rewrite, and considerably worse.

# v1.0.0
**1/6/25** - [44fc5bc](https://github.com/SketchedDoughnut/lynxy/commit/44fc5bce7c79b888aeea0f3c562dd0db9b79afd2) (estimate)
- The first official release of the completely refactored and re-written Lynxy client. The lynxy_server implementation has been dropped for now, and plans for that as a seperate package are coming in the future. As of when this release was made, no documentation was written but was being worked on. 
- This release defines how Lynxy will work from now on, and sets the starting point for growth in the future. 

# V1.1.0 - 1.2.0
**8/24/26** - [eb922ff](https://github.com/SketchedDoughnut/lynxy/tree/eb922ffbe1936e2925700825207ee22d9b18899e) (estimate)
- This release fixed a variety of issues and introduced some new features. Thank you [i1aw](https://github.com/i1aw) for helping with testing and recommending these changes.
- A bug was fixed where the events would never be added and would fail to be dispatched. 
- A variety of imports were changed in order to make accessing things such as `lynxy.Message` easier for typehinting and general usage. 
- The `Lynxy()` class was renamed to `Client()` to make its purpose clearer. 
- The `ON_CLOSE` event was renamed to `ON_DISCONNECT`
- The `bind` parameter of `Client()` was removed as it caused errors when set to `False` and was not a necessary option when using the client.
- New exceptions were added to make errors more graceful:
    - `ConnectionFailedError` -> when the connection has failed 
    - `TargetUnavailableError` -> when the target machine is not available for connection
    - `InvalidFunctionError` -> when a callback function for an event has invalid inputs
    - `AddrAlreadyBindedError` -> when a socket is already binded to the inputted host IP / port

# V1.2.1
**8/24/26** - [3206210](https://github.com/SketchedDoughnut/lynxy/tree/32062103a43357fca18a9cd637d642402b7083c2) (estimate)
- Added a feature that allows you to decide which connection attempts get accepted or rejected via the `lynxy.Event.ON_CONN_ATTEMPT` event. If no event is created, any connection will be rejected unless it is the target you passed in to `client.connect()`. However, you can make your own callback with `client.event()` if you want to do more. Just remember to return a bool!
