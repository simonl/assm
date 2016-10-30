.data


.text

_start:
	xorl %eax, %eax
	int $0x80

main:
	addl $4, %esi
	jmp *-4(%esi)
