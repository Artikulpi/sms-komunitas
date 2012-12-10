#!/usr/bin/env python

import time
from db import *

def main():
    while True:
        last_sms = get_latest_sms()
        last_queue = get_latest_queue()
        
        if last_sms > last_queue:
            while last_sms >= last_queue:
                last_queue = last_queue + 1
                if last_queue <= last_sms:
                    sms = get_sms(last_queue)
                    
                    # Send to Queue
                    save_queue(sms[0].ReceivingDateTime, sms[0].SenderNumber, sms[0].TextDecoded)
                    # Send notification
                    broadcast = get_broadcast()
                    for person in broadcast:
                        save_outbox(person.phone, sms[0].TextDecoded, 1)
                        
                    # Write Logs
                    print "%s | %s" % (sms[0].SenderNumber, sms[0].TextDecoded)
                    
            update_last_queue(last_sms)
            
        time.sleep(5)
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'

