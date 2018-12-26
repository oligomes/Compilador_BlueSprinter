; exportacoes
TRUE	>
FALSE	>
AND 	>
OR 		>
NOT 	>
OP1 	>
OP2 	>

&				/0000

TRUE	K		/0001
FALSE	K		/0000


OP1		K		/0000
OP2		K		/0000


; operacao de AND
AND		$		/0001
		LD		OP1
		*		OP2
		JZ		FIM_AND
		LD		TRUE
FIM_AND	RS		AND


; operacao de OR
OR		$		/0001
		LD		OP1
		+		OP2
		JZ		FIM_OR
		LD		TRUE
FIM_OR	RS		OR


; operacao de NOT
NOT		$		/0001
		LD		OP1
		-		TRUE
		JZ		FIM_NOT
		+		TRUE
FIM_NOT	RS		NOT

# BOOLEAN_OP
