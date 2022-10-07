import logging
from . import epdconfig
from . import gtconfig

class GT_Development:
    def __init__(self):
        self.Touch = 0
        self.TouchpointFlag = 0
        self.TouchCount = 0
        self.Touchkeytrackid = [0, 1, 2, 3, 4]
        self.X = [0, 1, 2, 3, 4]
        self.Y = [0, 1, 2, 3, 4]
        self.S = [0, 1, 2, 3, 4]
    
class GT1151:
    def __init__(self, i2cAddress):
        # e-Paper
        self.ERST = epdconfig.RST_PIN  
        self.DC = epdconfig.DC_PIN
        self.CS = epdconfig.CS_PIN
        self.BUSY = epdconfig.BUSY_PIN
        # TP
        self.TRST = gtconfig.TRST_PIN
        self.INT = gtconfig.INT_PIN
        
        gtconfig.address = i2cAddress

    def digital_read(self, pin):
        return gtconfig.digital_read(pin)
    
    def GT_Reset(self):
        gtconfig.digital_write(self.TRST, 1)
        gtconfig.delay_ms(100)
        gtconfig.digital_write(self.TRST, 0)
        gtconfig.delay_ms(100)
        gtconfig.digital_write(self.TRST, 1)
        gtconfig.delay_ms(100)

    def GT_Write(self, Reg, Data):
        gtconfig.i2c_writebyte(Reg, Data)

    def GT_Read(self, Reg, len):
        return gtconfig.i2c_readbyte(Reg, len)
         
    def GT_ReadVersion(self):
        buf = self.GT_Read(0x8140, 4)
        print(buf)

    def GT_Init(self):
        if (gtconfig.module_init() != 0):
            return -1

        self.GT_Reset()
        self.GT_ReadVersion()

    def GT_Scan(self, GT_Dev, GT_Old):
        buf = []
        mask = 0x00
        
        if(GT_Dev.Touch == 1):
            GT_Dev.Touch = 0
            buf = self.GT_Read(0x814E, 1)
            
            if(buf[0]&0x80 == 0x00):
                self.GT_Write(0x814E, mask)
                gtconfig.delay_ms(10)
                
            else:
                GT_Dev.TouchpointFlag = buf[0]&0x80
                GT_Dev.TouchCount = buf[0]&0x0f
                
                if(GT_Dev.TouchCount > 5 or GT_Dev.TouchCount < 1):
                    self.GT_Write(0x814E, mask)
                    return
                    
                buf = self.GT_Read(0x814F, GT_Dev.TouchCount*8)
                self.GT_Write(0x814E, mask)
                
                GT_Old.X[0] = GT_Dev.X[0];
                GT_Old.Y[0] = GT_Dev.Y[0];
                GT_Old.S[0] = GT_Dev.S[0];
                
                for i in range(0, GT_Dev.TouchCount, 1):
                    GT_Dev.Touchkeytrackid[i] = buf[0 + 8*i] 
                    GT_Dev.X[i] = (buf[2 + 8*i] << 8) + buf[1 + 8*i]
                    GT_Dev.Y[i] = (buf[4 + 8*i] << 8) + buf[3 + 8*i]
                    GT_Dev.S[i] = (buf[6 + 8*i] << 8) + buf[5 + 8*i]

                print(GT_Dev.X[0], GT_Dev.Y[0], GT_Dev.S[0])
                
    def exit(self):
        gtconfig.module_exit()
