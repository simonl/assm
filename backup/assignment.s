.section .data
.section .text

.globl __rasg
.globl __as__

.type __rasg__,@function
.type __as__,@function

__rasg__:
	enter $0, $0
	movl 8(%ebp), %ebx
	movl 12(%ebp), %eax
	movl %eax, (%ebx)
	leave
	ret $8

__as__:
	enter $0, $0
	movl 8(%ebp), %eax
	movl 12(%ebp), %ebx
	movl %eax, (%ebx)
	leave
	ret $8

# __addasg__
# __shrasg__
# __...asg___

