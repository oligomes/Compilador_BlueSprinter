; exportacoes
PUSH	>
POP		>
SP 		>

; importacoes
K_MM 	<
K_LD	<
WORD_TAM 	<
ACC_AUX     <


			&		/0000


SP			K		/0FFE
SP_MAX 		K 		/1000



PUSH 		$ 		/0001
			MM		ACC_AUX
			LD		K_MM
			+		SP
			MM 		EMPILHA
			LD	 	ACC_AUX
EMPILHA		K 		/0000
			LD 		SP
			; atualiza o topo da pilha
			-		WORD_TAM
			MM 		SP
FIM_PUSH 	RS 		PUSH



POP 		$ 		/0001
			; atualiza o topo da pilha
			LD 		SP
			+		WORD_TAM
			MM 		SP
			; verifica se o topo estourou
			LD 		SP_MAX
			-		SP
			; testa se eh zero o resultado
POP_IF		JZ		POP_THEN
POP_ELSE	JP		POP_END_IF
POP_THEN	LD 		SP_MAX
			-		WORD_TAM
			MM 		SP
			; le o topo da pilha
POP_END_IF	LD		K_LD
			+		SP
			MM 		LE 
LE 			K 		/0000
			; retorna com o valor desempilhado no acumulador
FIM_POP 	RS 		POP


# PUSH_POP
