 -- Compiling -- 
{'a': '4', 'b': '8'}
[['__asg__'], [['&a'], [['__asg__'], [['&b'], ['5']]]]] 

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
pushl $__next__0
pushl %ebp
movl %esp, %ebp
movl %ebp, %eax
movl (%eax), %eax

subl $4, %eax
pushl %eax
pushl $__next__1
pushl %ebp
movl %esp, %ebp
movl %ebp, %eax
movl (%eax), %eax
movl (%eax), %eax

subl $8, %eax
pushl %eax
movl $5, %eax
pushl %eax
movl $__asg__, %eax
jmp *%eax
__next__1:
pushl %eax
movl $__asg__, %eax
jmp *%eax
__next__0:
leave
ret
