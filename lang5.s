.include "std.s"
.section .data
.section .text
maps:
enter $0, $0
movl 12(%ebp), %eax
pushl %eax
movl $__cdr__, %eax
call *%eax
pushl %eax
movl 8(%ebp), %eax
call *%eax
pushl %eax
movl 12(%ebp), %eax
pushl %eax
movl $__car__, %eax
call *%eax
pushl %eax
movl 8(%ebp), %eax
call *%eax
pushl %eax
movl $__cons__, %eax
call *%eax
leave
ret $8
square:
enter $0, $0
movl 8(%ebp), %eax
pushl %eax
movl 8(%ebp), %eax
pushl %eax
movl $__mul__, %eax
call *%eax
leave
ret $4
fact:
enter $0, $0
movl 8(%ebp), %eax
cmp false, %eax
je else_clause0
movl 8(%ebp), %eax
pushl %eax
movl $__pred__, %eax
call *%eax
pushl %eax
movl $fact, %eax
call *%eax
pushl %eax
movl 8(%ebp), %eax
pushl %eax
movl $__mul__, %eax
call *%eax
leave
ret $4
jmp end_if0
else_clause0:
movl $1, %eax
leave
ret $4
end_if0:
factExpr:
enter $0, $0
movl 8(%ebp), %eax
cmp false, %eax
je else_clause1
movl 8(%ebp), %eax
pushl %eax
movl $__pred__, %eax
call *%eax
pushl %eax
movl $factExpr, %eax
call *%eax
pushl %eax
movl 8(%ebp), %eax
pushl %eax
movl $__mul__, %eax
call *%eax
jmp end_if1
else_clause1:
movl $1, %eax
end_if1:
leave
ret $4
main:
enter $0, $0
subl $4, %esp
movl $15, %eax
pushl %eax
movl $__range__, %eax
call *%eax
cmp $0, (%esp)
je end_for0
pushl %ebp
movl (%ebp), %ebp
movl %eax, -4(%ebp)
movl -4(%ebp), %eax
pushl %eax
movl $factExpr, %eax
call *%eax
pushl %eax
movl $__pdec__, %eax
call *%eax
movl $__ln__, %eax
call *%eax
popl %ebp
ret
end_for0:
addl $4, %esp
movl $2, %eax
pushl %eax
movl $3, %eax
pushl %eax
movl $__leq__, %eax
call *%eax
leave
ret $4
