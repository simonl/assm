.include "STD_IO.s"
.include "Boolean.s"
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
pushl $_next_0
pushl %ebp
movl %esp, %ebp
movl $_dt_0, %eax
movl $7, %ebx
pushl %eax
movl $_print, %eax
jmp *%eax
_next_0:
pushl $_next_1
pushl %ebp
movl %esp, %ebp
movl $2, %eax
pushl %eax
movl $2, %eax
pushl %eax
movl $func, %eax
jmp *%eax
_next_1:
pushl %eax
movl $func, %eax
pushl %eax
movl -4(%ebp), %eax
pushl %eax
pushl $_next_2
pushl %ebp
movl %esp, %ebp
movl $1, %eax
pushl %eax
movl $2, %eax
pop %ebx
addl %ebx, %eax
pushl %eax
pushl $_next_3
pushl %ebp
movl %esp, %ebp
movl $3, %eax
pushl %eax
movl $other, %eax
jmp *%eax
_next_3:
pushl %eax
movl (%ebp), %eax
movl -8(%eax), %eax
jmp *%eax
_next_2:
pop %ebx
call _and
leave
ret
.type main2,@function
main2:
pushl $_next_4
pushl %ebp
movl %esp, %ebp
pushl $_next_5
pushl %ebp
movl %esp, %ebp

movl $_inputChar, %eax
jmp *%eax
_next_5:
pushl %eax
movl $_printChar, %eax
jmp *%eax
_next_4:
pushl $_next_6
pushl %ebp
movl %esp, %ebp

movl $_repeat, %eax
jmp *%eax
_next_6:


leave
ret
.type func,@function
func:
movl -4(%ebp), %eax
pushl %eax
pushl $_next_7
pushl %ebp
movl %esp, %ebp
movl (%ebp), %eax
movl -8(%eax), %eax
pushl %eax
movl $other, %eax
jmp *%eax
_next_7:
pop %ebx
call _equals
leave
ret
.type other,@function
other:
pushl $_next_8
pushl %ebp
movl %esp, %ebp
movl $_dt_1, %eax
movl $6, %ebx
pushl %eax
movl $_print, %eax
jmp *%eax
_next_8:
movl -4(%ebp), %eax
leave
ret
.section .data
_dt_0:
.ascii "Start!\n"

_dt_1:
.ascii "hello\n"
