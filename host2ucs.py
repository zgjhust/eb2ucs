# -*- coding:utf8 -*-
import binascii
import array

__REC_SIZE = 650


#第三版本，_TABLE使用array替换str,提高indexing效率，减少了ord()函数调用次数，result使用list
#使用list comprehension，避免频繁str concatenation，提升明显（20%）
class H2UConverter(object):
    def __init__(self):
        self.__HOST2UCS_TABLE_NAME = '056C44B0.MU-R-D'
        self.__SO = '\x0E'
        self.__SI = '\x0F'
        self.__SB = 0
        self.__DB = 1
        self._TABLE = array.array('B')

    def build_table(self):
        # chang _TABLE from str to array, seems imporved performance(indexing,reduced call to ord())
        with open(self.__HOST2UCS_TABLE_NAME, 'rb') as fd:
            self._TABLE.fromstring(fd.read())

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
            # use list to store characters,avoid frequently usage of str concatenation
            result = []
            pos = 0
            while pos < slen:
                try:
                    ch = s[pos:pos+step]
                    if step == 1:
                        if ch != self.__SO:
                            index = self._TABLE[0]
                            # result = result + unichr(int(binascii.hexlify(self._TABLE[index*512+ord(ch)*2:index*512+ord(ch)*2+2]),16))
                            tmpch = self._TABLE[index*512+ord(ch)*2]*0x100+self._TABLE[index*512+ord(ch)*2+1]
                            result.append(tmpch)
                            #result = result + unichr(ord(self._TABLE[index*512+ord(ch)*2])*0x100+ord(self._TABLE[index*512+ord(ch)*2+1]))
                        else:
                            result.append(0x0020)
                            step = 2
                        pos = pos + 1
                    else:
                        if ch[0] == self.__SI:
                            result.append(0x0020)
                            pos = pos + 1
                            step = 1
                        else:
                            index = self._TABLE[ord(ch[0])]
                            #result = result + unichr(int(binascii.hexlify(self._TABLE[index*512+ord(ch[1])*2:index*512+ord(ch[1])*2+2]),16))
                            #result = result + unichr(ord(self._TABLE[index*512+ord(ch[1])*2])*0x100+ord(self._TABLE[index*512+ord(ch[1])*2+1]))
                            tmpch = self._TABLE[index*512+ord(ch[1])*2]*0x100+self._TABLE[index*512+ord(ch[1])*2+1]
                            result.append(tmpch)
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
            # use list comprehension to improve performance
            yield u''.join([unichr(x) if unichr(x).isalnum() else u'\u0020' for x in result])




def yieldRec(fd, recsize=__REC_SIZE):
    rec = fd.read(recsize)
    while rec:
        yield rec
        rec = fd.read(recsize)

def test():
    conv = H2UConverter()
    conv.build_table()
    with open("C#SM011.CDTEMP.P01.BIN", "rb") as fd:
        with open("testd.txt",'w') as fa:
            fa.writelines(((rec+u'\n').encode('gb18030') for rec in conv.generate_ucs16_from_host_strings(yieldRec(fd, 650))))

if __name__ == '__main__':
  
    # import cProfile
    # cProfile.run('test()')
    test()

# [Finished in 71.4s]

 #         202516694 function calls in 115.556 seconds

 #   Ordered by: standard name

 #   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 #        1    0.000    0.000  115.556  115.556 <string>:1(<module>)
 #        1    0.000    0.000    0.000    0.000 __init__.py:49(normalize_encoding)
 #        1    0.000    0.000    0.001    0.001 __init__.py:71(search_function)
 #        1    0.000    0.000    0.000    0.000 codecs.py:77(__new__)
 #        1    0.000    0.000    0.000    0.000 gb18030.py:12(Codec)
 #        1    0.000    0.000    0.000    0.000 gb18030.py:16(IncrementalEncoder)
 #        1    0.000    0.000    0.000    0.000 gb18030.py:20(IncrementalDecoder)
 #        1    0.000    0.000    0.000    0.000 gb18030.py:24(StreamReader)
 #        1    0.000    0.000    0.000    0.000 gb18030.py:27(StreamWriter)
 #        1    0.000    0.000    0.000    0.000 gb18030.py:30(getregentry)
 #        1    0.000    0.000    0.000    0.000 gb18030.py:7(<module>)
 #        2    0.000    0.000    0.001    0.000 host2ucs-v5.py:16(build_table)
 #    60340   87.349    0.001  114.873    0.002 host2ucs-v5.py:20(generate_ucs16_from_host_strings)
 #        1    0.000    0.000    0.000    0.000 host2ucs-v5.py:8(__init__)
 #    60340    0.044    0.000    0.295    0.000 host2ucs-v5.py:80(yieldRec)
 #        1    0.002    0.002  115.556  115.556 host2ucs-v5.py:86(test)
 #    60340    0.096    0.000  115.273    0.002 host2ucs-v5.py:91(<genexpr>)
 #        1    0.001    0.001    0.001    0.001 {__import__}
 #        1    0.000    0.000    0.000    0.000 {_codecs_cn.getcodec}
 #        1    0.000    0.000    0.000    0.000 {built-in method __new__ of type object at 0x1E1D4498}
 #        1    0.000    0.000    0.000    0.000 {hasattr}
 #        2    0.000    0.000    0.000    0.000 {isinstance}
 #    60339    0.009    0.000    0.009    0.000 {len}
 # 38581325    3.469    0.000    3.469    0.000 {method 'append' of 'list' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 #    60339    0.303    0.000    0.304    0.000 {method 'encode' of 'unicode' objects}
 #        2    0.000    0.000    0.000    0.000 {method 'fromstring' of 'array.array' objects}
 #        3    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
 # 38581325    4.078    0.000    4.078    0.000 {method 'isalnum' of 'unicode' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
 #    60339    0.713    0.000    0.713    0.000 {method 'join' of 'unicode' objects}
 #    60342    0.251    0.000    0.251    0.000 {method 'read' of 'file' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'replace' of 'str' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
 #        1    0.000    0.000    0.000    0.000 {method 'translate' of 'str' objects}
 #        1    0.279    0.279  115.552  115.552 {method 'writelines' of 'file' objects}
 #        4    0.001    0.000    0.001    0.000 {open}
 # 77527879    5.684    0.000    5.684    0.000 {ord}
 # 47403750   13.275    0.000   13.275    0.000 {unichr}