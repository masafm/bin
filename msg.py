#!/usr/bin/env python3
import sys
import json
from msg_parser import MsOxMessage

msg = MsOxMessage(sys.argv[1])
#print(json.dumps(msg.header_dict))
#print(msg.get_message_as_json())
saved_path = msg.save_email_file('./')
print(saved_path)
