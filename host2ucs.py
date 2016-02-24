# -*- coding:utf8 -*-
import binascii

__REC_SIZE = 650


# 第一版程序无优化措施

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
        
        for s in hoststrs:
            s = remain + s
            remain = ''
            slen = len(s)
            result = u''
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
                                result = result + tmpch
                            else:
                                result = result + u'\u0020'
                            #result = result + unichr(ord(self._TABLE[index*512+ord(ch)*2])*0x100+ord(self._TABLE[index*512+ord(ch)*2+1]))
                        else:
                            result = result + u'\u0020'
                            step = 2
                        pos = pos + 1
                    else:
                        if ch[0] == self.__SI:
                            result = result + u'\u0020'
                            pos = pos + 1
                            step = 1
                        else:
                            index = ord(self._TABLE[ord(ch[0])])
                            #result = result + unichr(int(binascii.hexlify(self._TABLE[index*512+ord(ch[1])*2:index*512+ord(ch[1])*2+2]),16))
                            #result = result + unichr(ord(self._TABLE[index*512+ord(ch[1])*2])*0x100+ord(self._TABLE[index*512+ord(ch[1])*2+1]))
                            tmpch = unichr(ord(self._TABLE[index*512+ord(ch[1])*2])*0x100+ord(self._TABLE[index*512+ord(ch[1])*2+1]))
                            if tmpch.isalnum():
                                result = result + tmpch
                            else:
                                result = result + u'\u0020'
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

            yield result




def yieldRec(fd, recsize=__REC_SIZE):
    rec = fd.read(recsize)
    while rec:
        yield rec
        rec = fd.read(recsize)

def test():
    conv = H2UConverter()
    conv.build_table()
    with open("C#SM011.CDTEMP.P01.BIN", "rb") as fd:
        with open("testa.txt",'w') as fa:
            fa.writelines(((rec+u'\n').encode('gb18030') for rec in conv.generate_ucs16_from_host_strings(yieldRec(fd, 650))))

if __name__ == '__main__':
   
    import cProfile
    cProfile.run('test()')
    #test()

#[Finished in 89.1s]
#        270112088 function calls in 144.222 seconds

#    Ordered by: standard name

#    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
#         1    0.000    0.000  144.222  144.222 <string>:1(<module>)
#         1    0.000    0.000    0.000    0.000 __init__.py:49(normalize_encoding)
#         1    0.000    0.000    0.021    0.021 __init__.py:71(search_function)
#         1    0.000    0.000    0.000    0.000 codecs.py:77(__new__)
#         1    0.000    0.000    0.000    0.000 gb18030.py:12(Codec)
#         1    0.000    0.000    0.000    0.000 gb18030.py:16(IncrementalEncoder)
#         1    0.000    0.000    0.000    0.000 gb18030.py:20(IncrementalDecoder)
#         1    0.000    0.000    0.000    0.000 gb18030.py:24(StreamReader)
#         1    0.000    0.000    0.000    0.000 gb18030.py:27(StreamWriter)
#         1    0.000    0.000    0.000    0.000 gb18030.py:30(getregentry)
#         1    0.000    0.000    0.000    0.000 gb18030.py:7(<module>)
#         2    0.000    0.000    0.027    0.014 host2ucs.py:15(build_table)
#     60340  112.767    0.002  143.345    0.002 host2ucs.py:19(generate_ucs16_from_host_strings)
#         1    0.000    0.000    0.000    0.000 host2ucs.py:7(__init__)
#     60340    0.045    0.000    0.405    0.000 host2ucs.py:85(yieldRec)
#         1    0.002    0.002  144.222  144.222 host2ucs.py:91(test)
#     60340    0.093    0.000  143.788    0.002 host2ucs.py:96(<genexpr>)
#         1    0.020    0.020    0.021    0.021 {__import__}
#         1    0.000    0.000    0.000    0.000 {_codecs_cn.getcodec}
#         1    0.000    0.000    0.000    0.000 {built-in method __new__ of type object at 0x1E1D4498}
#         1    0.000    0.000    0.000    0.000 {hasattr}
#         2    0.000    0.000    0.000    0.000 {isinstance}
#     60339    0.010    0.000    0.010    0.000 {len}
#         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
#     60339    0.329    0.000    0.350    0.000 {method 'encode' of 'unicode' objects}
#         3    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
#  38444427    4.571    0.000    4.571    0.000 {method 'isalnum' of 'unicode' objects}
#         1    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
#     60342    0.359    0.000    0.359    0.000 {method 'read' of 'file' objects}
#         1    0.000    0.000    0.000    0.000 {method 'replace' of 'str' objects}
#         1    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
#         1    0.000    0.000    0.000    0.000 {method 'translate' of 'str' objects}
#         1    0.351    0.351  144.139  144.139 {method 'writelines' of 'file' objects}
#         4    0.080    0.020    0.080    0.020 {open}
# 192861160   13.412    0.000   13.412    0.000 {ord}
#  38444427   12.181    0.000   12.181    0.000 {unichr}
