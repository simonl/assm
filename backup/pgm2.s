.include "std.s"
.section .data
.section .text
.globl _start
_start:
movl %esp, %ebp
pushl $__next__
pushl %ebp
movl %esp, %ebp
jmp main
__next__:
movl %eax, %ebx
movl $1, %eax
int $0x80
.type main,@function
main:
subl $0, %esp
#__sub__(__mul__,__add__)
#Calling __sub__
pushl $__next__0
pushl %ebp
movl %esp, %ebp
movl $__mul__, %eax
pushl %eax
movl $__add__, %eax
pushl %eax
movl $__sub__, %eax
jmp *%eax
__next__0:
leave
ret
