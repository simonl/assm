
.section .data

	.long 6
	str1:
	.ascii "hello!"

	.long 5
	str2:
	.ascii "hello"

	.long 9
	str3:
	.ascii "A string!"

.section .text

.globl _start44
_start44:
	movl %esp, %ebp

	call __meminit__
	call __setargv__

	pushl %eax
	call __main__

	movl %eax, %ebx
	movl $1, %eax
	int $0x80

__strcmp__:
	enter $0, $0
	movl 8(%ebp), %esi
	movl 12(%ebp), %edi
	movl -4(%esi), %eax
	movl -4(%edi), %ebx

	movl %eax, %ecx
	cmp %ecx, %ebx
	jg compare
	movl %ebx, %ecx

	compare:
	repe cmpsb
	je equals
	jl lesser
	jg greater

	equals:
	cmp %ebx, %eax
	jl lesser
	jg greater
	movl $0, %eax
	jmp end_cmp

	lesser:
	movl $-1, %eax
	jmp end_cmp

	greater:
	movl $1, %eax

	end_cmp:
	leave
	ret $8

__cp__:
	enter $0, $0
	movl 8(%ebp), %esi
	movl 12(%ebp), %edi
	movl -4(%esi), %ecx

	rep movsb

	leave
	ret $8

__rev__:
	enter $0, $0
	movl 8(%ebp), %esi
	movl -4(%esi), %ecx
	movl %esi, %edi
	addl %ecx, %edi
	shrl %ecx

	exch:
	decl %edi

	xchgb (%esi), %cl
	xchgb %cl, (%edi)
	xchgb (%esi), %cl

	incl %esi
	loop exch

	movl 8(%ebp), %eax
	leave
	ret $4

__exch__:
	enter $0, $0
	movl 8(%ebp), %eax
	movl 12(%ebp), %ebx

	xchgl (%eax), %ecx
	xchgl %ecx, (%ebx)
	xchgl (%eax), %ecx

	leave
	ret $8

__strlen__:
	enter $0, $0
	movl 8(%ebp), %edi

	xorl %eax, %eax
	xorl %ecx, %ecx
	notl %ecx
	repne scasb

	movl 8(%ebp), %eax
	subl %eax, %edi
	movl %edi, %eax
	decl %eax
	leave
	ret $4

_printStringArray: # printStringArray(String[])
	enter $0, $0
	movl 8(%ebp), %eax #array pos
	movl -4(%eax), %ecx #array counter
	shrl $2, %ecx
	arrayLoop:
		pushl %ecx
		movl 8(%ebp), %eax

		pushl (%eax)
		call __print__
		call __ln__

		addl $4, 8(%ebp)
		popl %ecx
		loop arrayLoop
	endArrayLoop:
	leave
	ret $4

_printNull:
	enter $0, $0
	movl 8(%ebp), %eax
	pushl %eax
	pushl %eax
	call __strlen__
	popl %ebx
	movl %eax, -4(%ebx)
	pushl %ebx
	call __print__
	leave
	ret $4


__main__:
	enter $0, $0
	pushl 8(%ebp)
	call _printStringArray
	leave
	ret $4


__str__: # string(size)
	enter $0, $0
	pushl 8(%ebp)
	call __alloc__
	leave
	ret

