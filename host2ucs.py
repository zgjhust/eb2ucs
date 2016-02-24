# -*- coding:utf8 -*-
import binascii
import StringIO
__REC_SIZE = 650


#第二版程序，使用StringIO，避免频繁str粘贴，然并卵
class H2UConverter(object):
    def __init__(self):
        self.__HOST2UCS_TABLE_NAME = '056C44B0.MU-R-D'
        self.__SO = '\x0E'
        self.__SI = '\x0F'
        self.__SB = 0
        self.__DB = 1
        self.__TABLE = ''

    def build_table(self):
        with open(self.__HOST2UCS_TABLE_NAME, 'rb') as fd:
            self._TABLE = fd.read()

    def generate_ucs16_from_host_strings(self, hoststrs):
        if self._TABLE:
            self.build_table()
        remain = ''
        step = 1
        pos = 0
        result = StringIO.StringIO(u'')
        for s in hoststrs:
            s = remain + s
            remain = ''
            slen = len(s)
            # result = StringIO.StringIO(u'')
            result.truncate(0)
            pos = 0
            while pos < slen:
                try:
                    ch = s[pos:pos+step]
                    if step == 1:
                        if ch != self.__SO:
                            index = ord(self._TABLE[0])
                            # result = result + unichr(int(binascii.hexlify(self._TABLE[index*512+ord(ch)*2:index*512+ord(ch)*2+2]),16))
                            tmpch = unichr(ord(self._TABLE[index*512+ord(ch)*2])*0x100+ord(self._TABLE[index*512+ord(ch)*2+1]))
                            if tmpch.isalnum():
                                #result = result + tmpch
                                result.write(tmpch)
                            else:
                                #result = result + u'\u0020'
                                result.write(u'\u0020')
                            #result = result + unichr(ord(self._TABLE[index*512+ord(ch)*2])*0x100+ord(self._TABLE[index*512+ord(ch)*2+1]))
                        else:
                            #result = result + u'\u0020'
                            result.write(u'\u0020')
                            step = 2
                        pos = pos + 1
                    else:
                        if ch[0] == self.__SI:
                            #result = result + u'\u0020'
                            result.write(u'\u0020')
                            pos = pos + 1
                            step = 1
                        else:
                            index = ord(self._TABLE[ord(ch[0])])
                            #result = result + unichr(int(binascii.hexlify(self._TABLE[index*512+ord(ch[1])*2:index*512+ord(ch[1])*2+2]),16))
                            #result = result + unichr(ord(self._TABLE[index*512+ord(ch[1])*2])*0x100+ord(self._TABLE[index*512+ord(ch[1])*2+1]))
                            tmpch = unichr(ord(self._TABLE[index*512+ord(ch[1])*2])*0x100+ord(self._TABLE[index*512+ord(ch[1])*2+1]))
                            if tmpch.isalnum():
                                #result = result + tmpch
                                result.write(tmpch)
                            else:
                                #result = result + u'\u0020'
                                result.write(u'\u0020')
                            pos = pos + 2

                except IndexError:
                    print 'index error ocurred!'
                    if step == 2:
                        remain = s[pos]
                        break
                except TypeError as e:
                    print e
                    print repr(ch)
                    return

            yield result.getvalue()
        result.close()




def yieldRec(fd, recsize=__REC_SIZE):
    rec = fd.read(recsize)
    while rec:
        yield rec
        rec = fd.read(recsize)

def test():
    with open("C#SM011.CDTEMP.P01.BIN", "rb") as fd:
        with open("testc.txt",'w') as fa:
            fa.writelines(((rec+u'\n').encode('gb18030') for rec in conv.generate_ucs16_from_host_strings(yieldRec(fd, 650))))    

if __name__ == '__main__':

    # import cProfile
    # cProfile.run('test()')
    test()
