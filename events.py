#!/usr/bin/env python3

# Internal piBot Events
# These would be used mostly by low-level "meta" plugins
# Most piBot modules use these in some form
WRITE_MESSAGE = 'writeMsgEvent'
READ_MESSAGE = 'readMsgEvent'
POST_CONNECT = 'postConnectEvent'
EXIT = 'exitEvent'

# "Real" Events
# These are public facing events, used by plugins
JOIN = 'joinEvent'
PART = 'partEvent'
