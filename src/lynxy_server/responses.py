# raw string forms
OPERATION_SUCCESS = "000"

OPERATION_FAIL = "001"

END_SESSION = "002"

INVALID_COMMAND = "003"

INVALID_USERNAME_DATA = "100"

INVALID_AUTH_TOKEN = "101"

USER_NOT_AUTHORIZED = "102"

KILL_ALL = "200"


# encoded forms
OPERATION_SUCCESS = OPERATION_SUCCESS.encode()
OPERATION_FAIL = OPERATION_FAIL.encode()
END_SESSION = END_SESSION.encode()
INVALID_COMMAND = INVALID_COMMAND.encode()
INVALID_USERNAME_DATA = INVALID_USERNAME_DATA.encode()
INVALID_AUTH_TOKEN = INVALID_AUTH_TOKEN.encode()
USER_NOT_AUTHORIZED = USER_NOT_AUTHORIZED.encode()
KILL_ALL = KILL_ALL.encode()