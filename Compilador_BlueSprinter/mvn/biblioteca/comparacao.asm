; exportacoes
IGUAL			>
DIFERENTE		>
MAIOR			>
MAIOR_OU_IGUAL	>
MENOR			>
MENOR_OU_IGUAL	>

; importacoes
ACC_AUX 		<
PUSH 			<
POP 			<
TRUE 			<
FALSE 			<


		&   		/0000



IGUAL 				$ 	=1
					; desempilha o segundo termo
					SC 	POP
					MM 	ACC_AUX
					; desempilha o primeiro termo
					SC 	POP
					; compara
					- 	ACC_AUX
					JZ 	X1
					LD 	FALSE
					JP 	FIM_IGUAL
X1 					LD 	TRUE
FIM_IGUAL 			SC 	PUSH
					RS 	IGUAL



DIFERENTE 			$ 	=1
					; desempilha o segundo termo
					SC 	POP
					MM 	ACC_AUX
					; desempilha o primeiro termo
					SC 	POP
					; compara
					- 	ACC_AUX
					JZ 	X2
					LD 	TRUE
					JP 	FIM_DIFERENTE
X2 					LD 	FALSE
FIM_DIFERENTE 		SC 	PUSH
					RS 	IGUAL



MAIOR 				$ 	=1
					; desempilha o segundo termo
					SC 	POP
					MM 	ACC_AUX
					; desempilha o primeiro termo
					SC 	POP
					; compara
					- 	ACC_AUX
					JZ 	X3
					JN 	X3
					LD 	TRUE
					JP  FIM_MAIOR
X3 					LD  FALSE
FIM_MAIOR 			SC  PUSH
					RS 	MAIOR



MENOR 				$ 	=1
					; desempilha o segundo termo
					SC 	POP
					MM 	ACC_AUX
					; desempilha o primeiro termo
					SC 	POP
					; compara
					- 	ACC_AUX
					JN 	X4
					LD 	FALSE
					JP  FIM_MENOR
X4 					LD  TRUE
FIM_MENOR 			SC  PUSH
					RS 	MENOR



MAIOR_OU_IGUAL  	$   =1
					; desempilha o segundo termo
					SC 	POP
					MM 	ACC_AUX
					; desempilha o primeiro termo
					SC 	POP
					; compara
					- 	ACC_AUX
					JN  X5
					LD  TRUE
					JP  FIM_MAIOR_OU_IGUAL
X5 					LD 	FALSE
FIM_MAIOR_OU_IGUAL  SC  PUSH
					RS  MAIOR_OU_IGUAL



MENOR_OU_IGUAL  	$   =1
					; desempilha o segundo termo
					SC 	POP
					MM 	ACC_AUX
					; desempilha o primeiro termo
					SC 	POP
					; compara
					- 	ACC_AUX
					JZ  X6
					JN  X6
					LD  FALSE
					JP  FIM_MENOR_OU_IGUAL
X6 					LD 	TRUE
FIM_MENOR_OU_IGUAL  SC  PUSH
					RS  MENOR_OU_IGUAL

# COMPARACAO
