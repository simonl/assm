.include "std.s"
.section .data
.section .text
main:
enter $0, $0
movl $3, %eax
pushl %eax
movl $__pdec__, %eax
call *%eax
movl $__ln__, %eax
call *%eax
movl $0, %eax
pushl %eax
movl 8(%ebp), %eax
pushl %eax
movl $__index__, %eax
call *%eax
pushl %eax
movl $__println__, %eax
call *%eax
leave
ret $4
