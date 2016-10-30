.section .data
	HEAP_START: .long 0
	HEAP_END: .long 0

.section .text

.globl __meminit__
.globl __alloc__
.globl __gc__
.globl __heapsize__

.type __meminit__,@function
.type __alloc__,@function
.type __gc__,@function
.type __heapsize__,@function

.equ BREAK, 45
.equ SYS_CALL, 0x80
.equ UNUSED, 0
.equ USED, 1
.equ MARKED, 2
.equ HEAD_SIZE, 8
.equ STEP, 4

_start1:
	movl %esp, %ebp

	call __meminit__

	movl $20, %ecx
	movl $23, %eax
	alloc_loop:
		pushl %ecx
		pushl %eax
		pushl %eax
		call __alloc__
		call traverse_mem
		call __ln__
		popl %eax
		decl %eax
		popl %ecx
	loop alloc_loop

	movl HEAP_END, %eax
	movl HEAP_START, %ebx
	subl %ebx, %eax

	movl %eax, %ebx
	movl $1, %eax
	int $SYS_CALL


__meminit__: # mem_init() : initializes the heap
	enter $0, $0
	movl $BREAK, %eax
	movl $0, %ebx
	int $SYS_CALL
	incl %eax
	movl %eax, HEAP_END
	movl %eax, HEAP_START
	leave
	ret

__heapsize__:
	movl HEAP_END, %eax
	movl HEAP_START, %ebx
	subl %ebx, %eax
	ret

# __alloc__(size)
#
# Registers used :
# 	%eax > current block ( header :%eax: rest of block )
# 	%ebx > end of heap
# 	%ecx > size to allocate
# 	%edx > size of current block

__alloc__:
	enter $0, $0
	movl 8(%ebp), %ecx
	movl HEAP_END, %ebx
	movl HEAP_START, %eax

	check_loop:
		cmp  %eax, %ebx
		je newMem

		addl $HEAD_SIZE, %eax
		movl -STEP(%eax), %edx
		cmp $UNUSED, -HEAD_SIZE(%eax)
		jne nextBlock

		#check for perfect match
		cmp %ecx, %edx
		je put

		#check for sufficient size
		subl $HEAD_SIZE, %edx
		cmp %ecx, %edx
		jge split
		addl $HEAD_SIZE, %edx

		#keep going
		nextBlock:
		addl %edx, %eax
		jmp check_loop


newMem: #asks Linux for more memory and allocates one block
	pushl %eax
	pushl %ecx

	movl $BREAK, %eax	#brk system call
	movl %ecx, %ebx
	shll $4, %ebx
	addl HEAP_END, %ebx	#we want to add : size to allocate x 16 (%ecx << 4)
	int $SYS_CALL

	cmp $0, %eax
	jle error

	movl %eax, %edx		# Set the end_of_heap to the new break
	subl HEAP_END, %edx	#	and get the size of the displacement in %edx
	subl $16, %edx		# size of new block = displacement - 2 headers
	movl %eax, HEAP_END

	popl %ecx
	popl %eax
	addl $HEAD_SIZE, %eax

	# end-of-sys_call status:
	#	%eax, large new block
	#	%ebx, not needed
	#	%ecx, size to allocate
	#	%edx, size of new block - 2 headers

split: 	#split a large free block into what is needed and the remainder
	# %eax : found block, %ebx : end_of_heap, %ecx : size to allocate, %edx : size found
	movl %eax, %ebx
	addl %ecx, %ebx		#place %ebx on remainder
	subl %ecx, %edx		#remainder size = block size - alloc size - 8
	movl $UNUSED, (%ebx)	#mark the remainder as unused
	movl %edx, 4(%ebx)	#put the size of the remainder
	movl %ecx, -4(%eax)	#finally put the used size on the block

put: #block address in %eax : only marks as used and returns
	movl $USED, -HEAD_SIZE(%eax)	#mark the block as used and return
	leave
	ret $4

error: #ERROR MESSAGE, then keep going
	# pushl MEMORY_ERROR
	# call throw
	xorl %eax, %eax
	leave
	ret $4


# __gc__()
#
# Registers used :
#	%esi : current object on the stack
#	%edi : current base pointer
#

__gc__:
	enter $0, $0
	call mark
	call sweep
	leave
	ret

mark:
	enter $0, $0
	movl %esp, %esi
	movl %ebp, %edi

	stack_loop:
		cmp %esi, %edi
		je nextFrame
		pushl %esi
		pushl %edi

		pushl (%esi)
		call mark_object

		popl %edi
		popl %esi
		addl $4, %esi
		jmp stack_loop

		nextFrame:
		cmp $0, %edi
		je end_mark
		movl (%edi), %edi
		addl $8, %esi
		jmp stack_loop
	end_mark:
	leave
	ret

mark_object:
	enter $0, $0
	movl 8(%ebp), %eax

	cmp $MARKED, -8(%eax)
	je end_marking

	movl $MARKED, -8(%eax)
	movl -4(%eax), %ecx
	shrl $2, %ecx
	
	mark_fields:
		pushl %eax
		pushl %ecx

		pushl (%eax)
		call mark_object

		popl %ecx
		popl %eax
		addl $4, %eax
	loop mark_fields
	end_marking:
	leave
	ret $4

traverse_mem:
sweep: #sweep
	enter $0, $0
	movl HEAP_START, %eax
	block_loop:
		cmp %eax, HEAP_END
		je end_block_loop

		addl $8, %eax
		pushl %eax
		pushl -4(%eax)
		call __dec__
		call __ln__
		popl %eax
		addl -4(%eax), %eax
		jmp block_loop
	end_block_loop:
	leave
	ret

	# f @ g @ h
	# __comp__(f, __comp__(g, h))

	# __comp__ = (f, g){ return (*x){ return f(g(*x)); }; };
