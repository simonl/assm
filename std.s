.include "memory.s"
.include "io.s"
.include "old_io.s"
.include "structure.s"
.include "arithmetic.s"
.include "boolean.s"
.include "string.s"
.include "assignment.s"
.include "itertest.s"
.include "hash.s"
.include "exceptions.s"

.section .data

	GLOBAL_CONTEXT:
	.long 0

	FRAME_STACK:
	.long GLOBAL_CONTEXT
	.long Null

	HANDLER_STACK:
	.long DEFAULT_HANDLER
	.long Null


.section .text
.globl _start

_start:
	movl %esp, %ebp
	call __meminit__
	call __setargv__

	pushl %eax
	call main

__exit__:
	movl %eax, %ebx
	movl $1, %eax
	int $0x80


main0:
	enter $4, $0

	movl 8(%ebp), %eax
	pushl 4(%eax)
	call __print__
	call __ln__

	movl $quad, %eax
	subl $testfunc, %eax
	pushl %eax
	call __dec__
	call __ln__

	pushl testfunc
	call __hex__
	call __ln__
	pushl quad
	call __hex__
	call __ln__

	movl $quad, %eax
	#subl $datafunc, %eax
	decl %eax
	#movb $0, 1(%eax)

	pushl testfunc
	call __hex__
	call __ln__

	pushl $2
	call testfunc

	leave
	ret $4

testfunc:
	jmp sqr
quad:
	enter $0, $0
	movl 8(%ebp), %eax
	mull %eax
	mull %eax
	leave
	ret $4

car:
	enter $0, $0
	movl 8(%ebp), %eax
	movl (%eax), %eax
	leave
	ret $4

cdr:
	enter $0, $0
	movl 8(%ebp), %eax
	movl 4(%eax), %eax
	leave
	ret $4

sqr:
	enter $0, $0
	movl 8(%ebp), %eax
	mull %eax
	leave
	ret $4

map:
	enter $0, $0
	movl 8(%ebp), %ebx
	movl 12(%ebp), %ecx

	map_loop:
		cmpl $Null, %ecx
		je endmap

		pushl %ecx
		pushl (%ecx)
		call *%ebx
		popl %ecx
		movl %eax, (%ecx)

		movl 4(%ecx), %ecx
		movl 8(%ebp), %ebx
		jmp map_loop
	endmap:
	leave
	ret $8

sidemap:
	enter $0, $0
	movl 8(%ebp), %ebx
	movl 12(%ebp), %ecx
	side_loop:
		cmpl $Null, %ecx
		je end_sideloop

		pushl %ecx
		pushl (%ecx)
		call *%ebx
		popl %ecx

		movl 4(%ecx), %ecx
		movl 8(%ebp), %ebx
		jmp side_loop
	end_sideloop:
	leave
	ret $8

printAll:
	enter $0, $0
	movl 8(%ebp), %eax

	printall_loop:
		pushl %eax
		pushl (%eax)
		call __dec__
		call __ln__
		popl %eax

		cmpl $Null, 4(%eax)
		je end_loopall

		movl 4(%eax), %eax
		jmp printall_loop
	end_loopall:
	leave
	ret $4

__setargv__:
	enter $8, $0
	movl (%ebp), %eax
	movl (%eax), %ecx
	movl %ecx, -4(%ebp)
	addl $4, %eax

	pushl %eax
	pushl %ecx
	shll $2, (%esp)
	call __alloc__
	movl %eax, -8(%ebp)

	popl %ebx
	pushl %eax
	pushl %ebx
	call __arrcp__

	movl -4(%ebp), %ecx
	movl -8(%ebp), %esi
	array_loop:
		pushl %ecx
		pushl %esi

		pushl (%esi)
		call __fixstring__
		popl %esi
		movl %eax, (%esi)

		addl $4, %esi
		popl %ecx
	loop array_loop
	movl -8(%ebp), %eax
	leave
	ret

__fixstring__:
	enter $0, $0
	pushl 8(%ebp)
	call __strlen__
	pushl %eax
	call __alloc__

	movl %eax, %edi
	movl 8(%ebp), %esi
	movl -4(%eax), %ecx

	rep movsb

	leave
	ret $4
