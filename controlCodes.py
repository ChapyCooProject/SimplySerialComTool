#CHARACTOR_CODE = "ascii"
#CHARACTOR_CODE = "shift-jis"
#CHARACTOR_CODE = "utf-8"
CharCode = "ascii"

NUL = b"\x00".decode(CharCode)
SOH = b"\x01".decode(CharCode)
STX = b"\x02".decode(CharCode)
ETX = b"\x03".decode(CharCode)
EOT = b"\x04".decode(CharCode)
ENQ = b"\x05".decode(CharCode)
ACK = b"\x06".decode(CharCode)
BEL = b"\x07".decode(CharCode)
BS = b"\x08".decode(CharCode)
HT = b"\x09".decode(CharCode)
LF = b"\x0A".decode(CharCode)
VT = b"\x0B".decode(CharCode)
FF = b"\x0C".decode(CharCode)
CR = b"\x0D".decode(CharCode)
SO = b"\x0E".decode(CharCode)
SI = b"\x0F".decode(CharCode)
DLE = b"\x10".decode(CharCode)
DC1 = b"\x11".decode(CharCode)
DC2 = b"\x12".decode(CharCode)
DC3 = b"\x13".decode(CharCode)
DC4 = b"\x14".decode(CharCode)
NAK = b"\x15".decode(CharCode)
SYN = b"\x16".decode(CharCode)
ETB = b"\x17".decode(CharCode)
CAN = b"\x18".decode(CharCode)
EM = b"\x19".decode(CharCode)
SUB = b"\x1A".decode(CharCode)
ESC = b"\x1B".decode(CharCode)
FS = b"\x1C".decode(CharCode)
GS = b"\x1D".decode(CharCode)
RS = b"\x1E".decode(CharCode)
US = b"\x1F".decode(CharCode)
DEL = b"\x7F".decode(CharCode)

def bin2str_controlCode(targetStr):
    targetStr = targetStr.replace(NUL,"<NUL>")
    targetStr = targetStr.replace(SOH,"<SOH>")
    targetStr = targetStr.replace(STX,"<STX>")
    targetStr = targetStr.replace(ETX,"<ETX>")
    targetStr = targetStr.replace(EOT,"<EOT>")
    targetStr = targetStr.replace(ENQ,"<ENQ>")
    targetStr = targetStr.replace(ACK,"<ACK>")
    targetStr = targetStr.replace(BEL,"<BEL>")
    targetStr = targetStr.replace(BS,"<BS>")
    targetStr = targetStr.replace(HT,"<HT>")
    targetStr = targetStr.replace(LF,"<LF>")
    targetStr = targetStr.replace(VT,"<VT>")
    targetStr = targetStr.replace(FF,"<FF>")
    targetStr = targetStr.replace(CR,"<CR>")
    targetStr = targetStr.replace(SO,"<SO>")
    targetStr = targetStr.replace(SI,"<SI>")
    targetStr = targetStr.replace(DLE,"<DLE>")
    targetStr = targetStr.replace(DC1,"<DC1>")
    targetStr = targetStr.replace(DC2,"<DC2>")
    targetStr = targetStr.replace(DC3,"<DC3>")
    targetStr = targetStr.replace(DC4,"<DC4>")
    targetStr = targetStr.replace(NAK,"<NAK>")
    targetStr = targetStr.replace(SYN,"<SYN>")
    targetStr = targetStr.replace(ETB,"<ETB>")
    targetStr = targetStr.replace(CAN,"<CAN>")
    targetStr = targetStr.replace(EM,"<EM>")
    targetStr = targetStr.replace(SUB,"<SUB>")
    targetStr = targetStr.replace(ESC,"<ESC>")
    targetStr = targetStr.replace(FS,"<FS>")
    targetStr = targetStr.replace(GS,"<GS>")
    targetStr = targetStr.replace(RS,"<RS>")
    targetStr = targetStr.replace(US,"<US>")
    targetStr = targetStr.replace(DEL,"<DEL>")
    return targetStr

def str2bin_controlCode(targetStr):
    targetStr = targetStr.replace("<NUL>",NUL)
    targetStr = targetStr.replace("<SOH>",SOH)
    targetStr = targetStr.replace("<STX>",STX)
    targetStr = targetStr.replace("<ETX>",ETX)
    targetStr = targetStr.replace("<EOT>",EOT)
    targetStr = targetStr.replace("<ENQ>",ENQ)
    targetStr = targetStr.replace("<ACK>",ACK)
    targetStr = targetStr.replace("<BEL>",BEL)
    targetStr = targetStr.replace("<BS>",BS)
    targetStr = targetStr.replace("<HT>",HT)
    targetStr = targetStr.replace("<LF>",LF)
    targetStr = targetStr.replace("<VT>",VT)
    targetStr = targetStr.replace("<FF>",FF)
    targetStr = targetStr.replace("<CR>",CR)
    targetStr = targetStr.replace("<SO>",SO)
    targetStr = targetStr.replace("<SI>",SI)
    targetStr = targetStr.replace("<DLE>",DLE)
    targetStr = targetStr.replace("<DC1>",DC1)
    targetStr = targetStr.replace("<DC2>",DC2)
    targetStr = targetStr.replace("<DC3>",DC3)
    targetStr = targetStr.replace("<DC4>",DC4)
    targetStr = targetStr.replace("<NAK>",NAK)
    targetStr = targetStr.replace("<SYN>",SYN)
    targetStr = targetStr.replace("<ETB>",ETB)
    targetStr = targetStr.replace("<CAN>",CAN)
    targetStr = targetStr.replace("<EM>",EM)
    targetStr = targetStr.replace("<SUB>",SUB)
    targetStr = targetStr.replace("<ESC>",ESC)
    targetStr = targetStr.replace("<FS>",FS)
    targetStr = targetStr.replace("<GS>",GS)
    targetStr = targetStr.replace("<RS>",RS)
    targetStr = targetStr.replace("<US>",US)
    targetStr = targetStr.replace("<DEL>",DEL)
    return targetStr


def calculate_checksum(strings):
    checksum = 0
    for char in strings:
        checksum = (checksum + ord(char)) % 256
    checksum_hex = "{:02X}".format(checksum) # 前ゼロ2桁の16進数に変換して取得
    return checksum_hex
