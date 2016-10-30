#.include "STD_IO.s"
.section .data

	.long 5
	my_str:
	.ascii "SUM: "

	.long 4
	cur_iter:
	.ascii "x = "

	.long 5
	inner_iter:
	.ascii "\ty = "

.section .text

.globl _start433
_start433:
	movl %esp, %ebp
	call main2
	movl %eax, %ebx
	movl $1, %eax
	int $0x80


main322:
	enter $12, $0
	movl $0, -4(%ebp)

	#'for x in iterator()' becomes :
	#	call iterator
	#	cmp $0, (%esp)
	#	je end_iter0
	#
	#	pushl %ebp
	#	movl (%ebp), %ebp
	#	movl %eax, "INDEX"
	#		-- stuff --
	#	popl %ebp
	#	ret
	#	end_iter0:
	#	addl $4+, %esp --> 4 for callback address + 4 for each iteration variable

	#call iterator : range(4)
	pushl $4
	call __range__

	#check for end of iteration : callback address is 0
	cmp $0, (%esp)
	je end_iter0

	#restore frame
	pushl %ebp
	movl (%ebp), %ebp

	#put the value of the iterator in local variable
	movl %eax, -8(%ebp)

		pushl $cur_iter
		call __print__
		pushl -8(%ebp)
		call __dec__
		call __ln__

		#do stuff, item is in -8(%ebp)
		#in this case, a nested iteration works
		pushl $7
		call __range__
		cmp $0, (%esp)
		je end_iter1

		pushl %ebp
		movl (%ebp), %ebp
		movl %eax, -12(%ebp)

			#accumulate result
			addl %eax, -4(%ebp)

			#print inner-loop value
			pushl $inner_iter
			call __print__
			pushl -12(%ebp)
			call __dec__
			call __ln__


		popl %ebp
		ret
		end_iter1:
		addl $4, %esp

	#get next item
	# range.next()
	popl %ebp
	ret
	end_iter0:
	#iteration is done, clean iteration variables + callback address
	addl $12, %esp

	pushl $my_str
	call __print__
	pushl -4(%ebp)
	call __dec__
	call __ln__

	#do some other stuff

	leave
	ret



.type __range__,@function
__range__:
	enter $4, $0
	movl $0, -4(%ebp)
	range_loop:
		movl -4(%ebp), %eax

		cmp %eax, 8(%ebp)
		je end_range

		# yield, value in %eax
		call *4(%ebp)
		# could receive a value back from the yield, possibly

		incl -4(%ebp)
		jmp range_loop
	end_range:
	leave
	movl  $0, 4(%esp) #make (%esp + 4*params) zero
	ret 			#final yield with address 0,
				# clean (#params - 1) from stack on return
				# in this case, (1 - 1) = 0


main2:
	enter $0, $0

	call __printback__
	cmpl $0, (%esp)
	je end_iter2

	pushl %ebp
	movl (%ebp), %ebp

		call __printback__
		cmpl $0, (%esp)
		je end_iter3

		pushl %ebp
		movl (%ebp), %ebp

		call __inputc__ #"return" a value to the iterator
		popl %ebp
		ret

		end_iter3:
		addl $4, %esp

	call __inputc__
	popl %ebp
	ret

	end_iter2:
	addl $4, %esp

	leave
	ret

__printback__:
	enter $0, $0

	pushl $'A'
	call __printc__
	call __ln__

	back_loop:
		xorl %eax, %eax
		call *4(%ebp)

		cmpl $'A', %eax
		je end_back

		pushl %eax
		call __printc__
		jmp back_loop
	end_back:
	leave
	pushl (%esp)
	movl $0, 4(%esp)
	ret
