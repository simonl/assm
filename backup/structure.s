.section .data
	.globl Null
	Null: .long .

.section .text

.globl __cons__
.globl __array__
.globl __list__
.globl __attr__

.type __cons__,@function
.type __arrray_,@function
.type __list__,@function
.type __attr__,@function

__cons__:
	enter $0, $0
	pushl $8
	call __alloc__
	movl 8(%ebp), %ebx
	movl %ebx, (%eax)
	movl 12(%ebp), %ebx
	movl %ebx, 4(%eax)
	leave
	ret $8

__array__: # array(size)
	enter $0, $0
	pushl 8(%ebp)
	shll $2, (%esp)
	call __alloc__
	leave
	ret $4

__arrcp__: # copy(arr1, arr2)
	enter $0, $0
	movl 8(%ebp), %esi
	movl 12(%ebp), %edi
	movl -4(%esi), %ecx
	rep movsl
	leave
	ret $8

__list__:
	enter $0, $0
	pushl $Null
	pushl 8(%ebp)
	call __cons__
	leave
	ret 

__attr__:
	enter $0, $0
	movl 8(%ebp),  %eax
	leave
	ret

