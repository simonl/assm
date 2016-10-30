.section .data
	.globl Null
	Null: .long .

	.long 17
	indexExc:
	.ascii "IndexOutOfBounds!"

.section .text

.globl __cons__
.globl __car__
.globl __cdr__

.globl __array__
.globl __list__
.globl __attr__

.type __cons__,@function
.type __arrray_,@function
.type __list__,@function
.type __attr__,@function

__cons__:
	pushl $8
	call __alloc__
	movl 4(%esp), %ebx
	movl %ebx, (%eax)
	movl 8(%esp), %ebx
	movl %ebx, 4(%eax)
	ret $8

__car__:
	movl 4(%esp), %eax
	movl (%eax), %eax
	ret $4

__cdr__:
	movl 4(%esp), %eax
	movl 4(%eax), %eax
	ret $4

__array__: # array(size)
	enter $0, $0
	pushl 8(%ebp)
	shll $2, (%esp)
	call __alloc__
	leave
	ret $4


__append__: # append(list, element){ ... }
	enter $0, $0
 	movl 8(%ebp), %eax

	pushl -4(%eax)
	addl $4, (%esp)
	call __alloc__

	pushl %eax
	pushl 8(%ebp)
	call __cp__
	movl 12(%ebp), %ebx
	movl %ebx, (%edi)
	leave
	ret $8

__arrcp__: # copy(arr1, arr2)
	enter $0, $0
	movl 8(%ebp), %esi
	movl 12(%ebp), %edi
	movl -4(%esi), %ecx
	rep movsl
	leave
	ret $8

__list__:
	pushl 4(%esp)
	call __alloc__

	pushl %eax
	pushl %esp
	addl $12, (%esp)
	call __cp__

	popl %ebx
	subl (%esp), %esp
	pushl %ebx
	ret $4

__attr__:
	enter $0, $0
	movl 8(%ebp),  %eax
	leave
	ret

__index__: # __index__(array, i) == array[i]
	enter $0, $0
	movl 8(%ebp), %eax
	movl 12(%ebp), %ebx

	movl -4(%eax), %ecx
	shrl $2, %ecx

	cmp %ecx, %ebx
	jge outOfBounds

	shll $2, %ebx
	addl %ebx, %eax
	movl (%eax), %eax
	leave
	ret $8

	outOfBounds:
	pushl $indexExc
	call __print__
	call __ln__
	movl $0, %eax
	leave
	ret $8

	# pushl $OutOfBoundsException
	# call throw
