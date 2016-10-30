.include "Boolean.s"
.section .data
.section .text
.globl _start
.globl main
_start:
movl %esp, %ebp
pushl $next
pushl %ebp
movl %esp, %ebp
jmp main
next:
movl %eax, %ebx
movl $1, %eax
int $0x80
.type main,@function
main:
movl $3, %eax
pushl %eax
movl $3, %eax
pop %ebx
imull %ebx, %eax
pushl %eax
movl -4(%ebp), %eax
pushl %eax
pushl $_next_0
pushl %ebp
movl %esp, %ebp
jmp other
_next_0:
pop %ebx
addl %ebx, %eax
movl %ebp, %esp
popl %ebp
ret
.type other,@function
other:
movl $3, %eax
pushl %eax
pushl $_next_1
pushl %ebp
movl %esp, %ebp
movl $8, %eax
pushl %eax
movl $5, %eax
pushl %eax
jmp another
_next_1:
pop %ebx
addl %ebx, %eax
movl %ebp, %esp
popl %ebp
ret
.type another,@function
another:
movl -4(%ebp), %eax
pushl %eax
movl -8(%ebp), %eax
pop %ebx
imull %ebx, %eax
movl %ebp, %esp
popl %ebp
ret
