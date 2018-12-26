; exportacoes
AND 	>
OR 		>
NOT 	>

; importacoes
TRUE	<
FALSE	<

PUSH 			<
POP 			<
ACC_AUX 		<

		&		/0000


; operacao de AND
AND		$		/0001
		SC		POP
		MM 		ACC_AUX
		SC 		POP
		*		ACC_AUX
		JZ		FIM_AND
		LD		TRUE
FIM_AND SC 		PUSH
		RS		AND


; operacao de OR
OR		$		/0001
		SC 		POP
		MM 		ACC_AUX
		SC 		POP
		+		ACC_AUX
		JZ		FIM_OR
		LD		TRUE
FIM_OR	SC 		PUSH
		RS		OR


; operacao de NOT
NOT		$		/0001
		SC 		POP
		-		TRUE
		JZ		FIM_NOT
		+		TRUE
FIM_NOT	SC 		PUSH
		RS		NOT

# BOOLEAN_OP
