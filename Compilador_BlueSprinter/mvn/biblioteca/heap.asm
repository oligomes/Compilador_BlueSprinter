INIT_HEAP   >
NEW_ARRAY   >
NEW_MATRIX  >
DIM_1       >
DIM_2       >

WORD_TAM    <
ACC_AUX     <
K_MM        <
K_0002 		<

            &   /0000


DIM_1       $    =1
DIM_2       $    =1


NEW_ARRAY 	$    =1
			LD   HP
			MM   ACC_AUX
			+    K_MM
			MM   X
			LD   DIM_1
X 			$    =1 ; salva a dimensao
			*    WORD_TAM
			+    WORD_TAM ; total = (DIM_1  + 1)*WORD_TAM
			+    HP ; atualiza para apontar para o próximo endereço vazio
			MM   HP ; reserva o espaco requerido
			LD   ACC_AUX ; retorna o resultado no acc
			RS   NEW_ARRAY


NEW_MATRIX  $    =1
			LD   HP
			MM   ACC_AUX
			+    K_MM
			MM   Y
			LD   DIM_1
Y 			$    =1
			LD   HP
			+    WORD_TAM
			+    K_MM
			MM   Z
			LD   DIM_2
Z 			$    =1
			*  	 DIM_1
			+    K_0002 ; total = (DIM_1 * DIM_2 + 2) * WORD_TAM
			*    WORD_TAM
			+    HP
			MM   HP
			LD   ACC_AUX
			RS   NEW_MATRIX


INIT_HEAP   $    =1
			LV   HEAP_HEAD
			+    WORD_TAM
			MM   HP
			RS   INIT_HEAP



HP          $    =1
HEAP_HEAD   K    /C0DA


# HEAP