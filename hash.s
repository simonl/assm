
.section .data
.section .text

main7:
	enter $4, $0

	pushl $243892
	call __dec__
	pushl %eax
	call __println__

	leave
	ret $4


__dcp__:
	enter $0, $0
	movl 8(%ebp), %esi
	movl 12(%ebp), %edi
	movl -4(%edi), %ecx

	rep movsb

	leave
	ret $8

__bstr__:
	enter $4, $0
	movl 8(%ebp), %eax
	pushl -4(%eax)
	call __alloc__
	movl %eax, -4(%ebp)

	movl 8(%ebp), %esi
	movl -4(%eax), %ecx
	cp_loop:
		movb (%esi), %dl
		movb %dl, (%eax)
		addl $4, %esi
		incl %eax
	loop cp_loop

	movl -4(%ebp), %eax
	leave
	ret $4

hashf:
	enter $0, $0
	movl 8(%ebp), %esi
	movl -4(%esi), %ecx
	movl $0xa9a9bba9, %eax
	xorl %edx, %edx

	hash_loop:
		movb (%esi), %dl

		movb %dl, %dh
		notb %dh
		roll $11, %edx
		notl %edx

		movl %eax, %ebx
		xorl %edx, %eax

		roll $23, %edx
		addl %edx, %eax
		rorl $17, %eax
		xorl %ebx, %eax
		notl %eax

		incl %esi
	loop hash_loop

	#xorl %edx, %edx
	#movl $113, %ecx
	#divl %ecx
	#movl %edx, %eax

	leave
	ret $4
