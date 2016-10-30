.section .data
.section .text

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
	movl 4(%esp), %esi
	movl 8(%esp), %edi
	movl -4(%esi), %ecx
	rep movsb
	movl 8(%esp), %eax
	ret $8

__concat__:
	enter $0, $0
	movl 8(%ebp), %eax
	pushl -4(%eax)
	movl 12(%ebp), %eax
	movl -4(%eax), %eax
	addl %eax, (%esp)
	call __alloc__
	pushl %eax
	pushl 8(%ebp)
	call __cp__
	pushl %eax
	pushl %edi
	pushl 12(%ebp)
	call __cp__
	popl %eax
	leave
	ret $8

__rev__:
	movl 4(%esp), %esi
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

	movl 4(%esp), %eax
	ret $4

__exch__:
	movl 4(%esp), %eax
	movl 8(%esp), %ebx

	xchgl (%eax), %ecx
	xchgl %ecx, (%ebx)
	xchgl (%eax), %ecx

	ret $8

__strlen__:
	movl 4(%esp), %edi

	xorl %eax, %eax
	xorl %ecx, %ecx
	notl %ecx
	repne scasb

	movl 4(%esp), %eax
	subl %eax, %edi
	movl %edi, %eax
	decl %eax
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


__forstr__:
	enter $0, $0
	movl 8(%ebp), %eax
	movl -4(%eax), %ecx
	str_loop:
		pushl %ecx
		pushl %eax
	loop str_loop
	leave
	movl $0, 4(%esp)
	ret $4



__str__: # null terminated --> object
	 # str( nuls ) : return copy( nuls, alloc(len(nuls)) )
	pushl 4(%esp)
	call __strlen__
	pushl %eax
	call __alloc__
	pushl %eax
	pushl %eax
	pushl 4(%esp)
	call __cp__
	popl %eax
	ret $4
