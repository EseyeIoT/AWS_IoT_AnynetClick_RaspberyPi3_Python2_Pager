import time
import py2_oled as oled
import ctypes
import ctypes.util
import json
import py2_aws_click as aws

# want to use atoi() from run-time
mylib = ctypes.util.find_library('c')
clib = ctypes.cdll.LoadLibrary(mylib)



    
def setup():
    print("setting up AWS")
    aws.sendcmd("ATE0\r\n")
    aws.recvdata("OK\r\n")

    aws.sendcmd('AT+AWSSUBCLOSE=0\r\n')
    aws.recvdata('+AWSSUBCLOSE:0,')

    aws.sendcmd('AT+AWSSUBOPEN=0,"msgout"\r\n')
    aws.recvdata('+AWSSUBOPEN:0,0\r\n')

    oled.OLED_M_Init()
    oled.OLED_Clear()


def main():
    setup()
    aws.resetaws()
    print("ready to receive...")
    while True:
        awsmessage = ''
        lenstr = ''
        msglen = 0

        aws.recvdata('+AWS:0,')
        lenstr = aws.recvMessageDataLen('\r\n')
        msglen = clib.atoi(lenstr)

        awsmessage = aws.recvMessageData(msglen)

        jsonformat = True
        jsondata = None
        try:
            jsondata = json.loads(awsmessage.decode('utf-8'))
        except Exception as ex:
            jsonformat = False
        
        oled.OLED_Clear()
        if jsonformat == True:
            oled.OLED_Puts(0, 1, jsondata['message'])
        else:
            oled.OLED_Puts(0, 1, awsmessage)
    
    ser.close()

if __name__=="__main__":
    main()

