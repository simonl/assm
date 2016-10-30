.include "lambdatest.s"
.section .text
main:
enter $0, $0
pushl Null
pushl $lambda0
call __lambda__
pushl %eax
call __force__
leave
ret $4


lambda0:
enter $0, $0
movl $3, %eax
leave
ret $4
