; exportacoes
GET_FROM_FRAME  >
SET_TO_FRAME 	>
GET_FROM_VECT   >
SET_TO_VECT     >
BASE            >
PUSHDOWN_SUM	>
PUSHDOWN_DIF 	>
PUSHDOWN_MUL 	>
PUSHDOWN_DIV 	>
GET_LENGTH 		>
ACC_AUX 		>
FP 				>

; importacoes
PUSH 		<
POP  		<
K_MM 		<
K_LD 		<
WORD_TAM 	<


			& 		/0000

;============================
;  Registradores Auxiliares
;============================

FP    		$ 		=1


ACC_AUX		$		=1

BASE 		$ 		=1
OFFSET 		$		=1



; =====================================
;  OPERACOES SOBRE POSICOES DE MEMORIA
; =====================================

GET_FROM_FRAME	$ 		=1
				; desempilha o parametro
				; OFFSET
				SC 		POP
				MM 		OFFSET

				; corpo da função
				LD		FP
				-		OFFSET
				+		K_LD
				MM		LOAD
LOAD			K 		/0000
				RS 		GET_FROM_FRAME



SET_TO_FRAME	$		=1
				; desempilha os parametros
				; OFFSET
				SC 		POP
				MM 		OFFSET

				LD		FP
				- 		OFFSET
				+		K_MM
				MM 		MOVE
				; desempilha o valor a ser atribuido
				SC 		POP
MOVE 			K 		/0000
				RS 		SET_TO_FRAME



GET_FROM_VECT 	$ 		=1
				; OFFSET
				SC 		POP
				MM 		OFFSET
				; BASE
				SC 		POP
				MM 		BASE

				LD 		BASE
				+ 		OFFSET
				+ 		K_LD
				MM 		LOAD_2
LOAD_2 			K 		/0000
				RS 		GET_FROM_VECT



SET_TO_VECT 	$ 		=1
				; desempilha o valor a ser atribuido
				SC 		POP
				MM 		ACC_AUX
				; OFFSET
				SC 		POP
				;* 		WORD_TAM
				MM 		OFFSET
				; BASE
				SC 		POP
				;MM 		BASE

				;LD 		BASE
				+ 		OFFSET
				+ 		K_MM
				MM 		MOVE_2
				LD 		ACC_AUX
MOVE_2 			K 		/0000
				RS 		SET_TO_VECT



GET_LENGTH      $       =1
				; dim
				LD 		WORD_TAM
				SC 		PUSH
				SC 		PUSHDOWN_MUL
				; calcula a instrucao
				SC 		PUSHDOWN_SUM
				SC 		POP
				+ 		K_LD
				MM 		LOAD_3
LOAD_3 			$ 		=1
				SC 		PUSH
				RS 		GET_LENGTH


; =====================================
;  OPERACOES SOBRE OPERANDOS NA PILHA
; =====================================

PUSHDOWN_SUM 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				+ 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_SUM

PUSHDOWN_DIF 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				- 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_DIF

PUSHDOWN_MUL 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				* 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_MUL

PUSHDOWN_DIV 	$ 		=1
				SC 		POP
				MM 		ACC_AUX
				SC 		POP
				/ 		ACC_AUX
				SC 		PUSH
				RS 		PUSHDOWN_DIV


# ENV
