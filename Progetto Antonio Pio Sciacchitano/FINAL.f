HEX

\ Indirizzo di base e registri GPIO
3F200000 CONSTANT BASE
BASE CONSTANT GPFSEL0
BASE 4 + CONSTANT GPFSEL1
BASE 8 + CONSTANT GPFSEL2
BASE 1C + CONSTANT GPSET0
BASE 28 + CONSTANT GPCLR0
BASE 34 + CONSTANT GPLEV0

1 CONSTANT OUTPUT
0 CONSTANT INPUT

\ Maschere per LED, buzzer e bottoni
00020000 CONSTANT LED1_MASK   \ GPIO 17
08000000 CONSTANT LED2_MASK  \ GPIO 18
00040000 CONSTANT LED3_MASK    \ GPIO 27
00800000 CONSTANT BUZZER_MASK \ GPIO 23
00000040 CONSTANT BOTTONE_ROSSO_MASK  \ GPIO 6
00002000 CONSTANT BOTTONE_VERDE_MASK \ GPIO 13
02000000 CONSTANT BOTTONE_BLU_MASK   \ GPIO 25

\ Maschere per LED RGB (segmenti)
00400000 CONSTANT SEG_R_MASK \ GPIO 22
04000000 CONSTANT SEG_G_MASK \ GPIO 26
00200000 CONSTANT SEG_B_MASK \ GPIO 21

\ Variabili di stato
VARIABLE STATO-GIOCO      \ 0: attesa iniziale, 1: LED acceso, 2: attesa bottone
VARIABLE LED-ATTIVO      \ -1: nessuno, 0: rosso, 1: verde, 2: blu
VARIABLE RGB-COLORE      \ Memorizza il colore RGB selezionato (0, 1 o 2)
VARIABLE rnd HERE @ rnd ! \ Inizializzazione generatore numeri casuali
VARIABLE MILLIS-COUNTER  \ Contatore per il debouncing
VARIABLE ULTIMO-ROSSO
VARIABLE ULTIMO-BLU
VARIABLE ULTIMO-VERDE
VARIABLE PARTITA-ATTIVA \ Flag per indicare se il gioco è in corso
50000 CONSTANT DEBOUNCE-DELAY \ Debouncing (anti-rimbalzo)

\ Utility di base
: ABS DUP 0< IF NEGATE THEN ;       \ Valore assoluto
: BTST AND 0<> ;                   \ Test bit
: MASK DECIMAL SWAP 10 MOD DUP 0> IF BEGIN SWAP 3 LSHIFT SWAP 1 - DUP 0= UNTIL THEN DROP ; \ Crea una maschera a partire da un numero di bit
: IN INPUT MASK ;                  \ Configura un pin come input
: OUT OUTPUT MASK ;                 \ Configura un pin come output
: SELECT DUP ROT SWAP @ OR SWAP ! ; \ Imposta i bit specificati in un registro
: DELAY BEGIN 1 - DUP 0 = UNTIL DROP ; \ Ritardo (cicli vuoti)

\ Configurazione GPIO
: GPIO17_OUT 17 OUT GPFSEL1 SELECT ; \ LED Rosso
: GPIO18_OUT 18 OUT GPFSEL1 SELECT ; \ LED Verde
: GPIO27_OUT 27 OUT GPFSEL2 SELECT ; \ LED Blu
: GPIO23_OUT 23 OUT GPFSEL2 SELECT ; \ Buzzer
: GPIO22_OUT 22 OUT GPFSEL2 SELECT ; \ RGB Rosso
: GPIO26_OUT 26 OUT GPFSEL2 SELECT ; \ RGB Verde
: GPIO21_OUT 21 OUT GPFSEL2 SELECT ; \ RGB Blu
: GPIO6_IN 6 IN GPFSEL0 SELECT ;     \ Bottone Rosso
: GPIO13_IN 13 IN GPFSEL1 SELECT ;    \ Bottone Verde
: GPIO25_IN 25 IN GPFSEL2 SELECT ;    \ Bottone Blu

\ Setup iniziale
: LED_SET GPIO17_OUT GPIO18_OUT GPIO27_OUT ;
: BUZZER_SET GPIO23_OUT ;
: BOTTONI_SET GPIO6_IN GPIO13_IN GPIO25_IN ;
: RGB_SET GPIO22_OUT GPIO26_OUT GPIO21_OUT ;

LED_SET BUZZER_SET RGB_SET BOTTONI_SET

\ Controllo LED principali
: LED1-ON LED1_MASK GPSET0 ! ;
: LED1-OFF LED1_MASK GPCLR0 ! ;
: LED2-ON LED2_MASK GPSET0 ! ;
: LED2-OFF LED2_MASK GPCLR0 ! ;
: LED3-ON LED3_MASK GPSET0 ! ;
: LED3-OFF LED3_MASK GPCLR0 ! ;
: BUZZER-ON BUZZER_MASK GPSET0 ! ;
: BUZZER-OFF BUZZER_MASK GPCLR0 ! ;
: RGB-R-ON SEG_R_MASK GPCLR0 ! ;    \ Attiva il segmento (livello basso)
: RGB-R-OFF SEG_R_MASK GPSET0 ! ;   \ Disattiva il segmento (livello alto)
: RGB-G-ON SEG_G_MASK GPCLR0 ! ;
: RGB-G-OFF SEG_G_MASK GPSET0 ! ;
: RGB-B-ON SEG_B_MASK GPCLR0 ! ;
: RGB-B-OFF SEG_B_MASK GPSET0 ! ;

: RGB-ON RGB-R-ON RGB-G-ON RGB-B-ON ;
: RGB-OFF RGB-R-OFF RGB-G-OFF RGB-B-OFF ;
: ALL-ON LED1-ON LED2-ON LED3-ON BUZZER-ON RGB-ON ;
: ALL-OFF LED1-OFF LED2-OFF LED3-OFF BUZZER-OFF ;

\ Sequenza di lampeggio iniziale
: BLINK
    2 BEGIN
        ALL-OFF
        LED1-ON   100000 DELAY LED1-OFF
        BUZZER-ON  10000 DELAY BUZZER-OFF
        LED3-ON     100000 DELAY LED3-OFF
        BUZZER-ON  10000 DELAY BUZZER-OFF
        LED2-ON   100000 DELAY LED2-OFF
        BUZZER-ON  10000 DELAY BUZZER-OFF
        1 - DUP 0=
    UNTIL
    DROP
    ALL-OFF
;

\ Generatore numeri casuali
: RANDOM rnd @ 31421 * 6927 + DUP rnd ! ;
: CHOOSE RANDOM 3 MOD ;

: MILLIS MILLIS-COUNTER @ ;
0 MILLIS-COUNTER !

0 ULTIMO-ROSSO !
0 ULTIMO-BLU !
0 ULTIMO-VERDE !

\ Controllo bottoni con debouncing
: BOTTONE-ROSSO-PREMUTO
    BOTTONE_ROSSO_MASK GPLEV0 @ AND 0<>
    DUP IF
        ULTIMO-ROSSO @ MILLIS @ - DEBOUNCE-DELAY > IF
            MILLIS ULTIMO-ROSSO !
            TRUE
        ELSE
            DROP FALSE
        THEN
    ELSE
        DROP FALSE
    THEN ;

: BOTTONE-VERDE-PREMUTO
    BOTTONE_VERDE_MASK GPLEV0 @ AND 0<>
    DUP IF
        ULTIMO-VERDE @ MILLIS @ - DEBOUNCE-DELAY > IF
            MILLIS ULTIMO-VERDE !
            TRUE
        ELSE
            DROP FALSE
        THEN
    ELSE
        DROP FALSE
    THEN ;

: BOTTONE-BLU-PREMUTO
    BOTTONE_BLU_MASK GPLEV0 @ AND 0<>
    DUP IF
        ULTIMO-BLU @ MILLIS @ - DEBOUNCE-DELAY > IF
            MILLIS ULTIMO-BLU !
            TRUE
        ELSE
            DROP FALSE
        THEN
    ELSE
        DROP FALSE
    THEN ;

\ Controllo se QUALSIASI bottone è premuto
: QUALSIASI-BOTTONE-PREMUTO
    BOTTONE-ROSSO-PREMUTO
    BOTTONE-VERDE-PREMUTO OR
    BOTTONE-BLU-PREMUTO OR ;

\ Accensione LED principale random
: ACCENDI-LED-RANDOM
    ALL-OFF
    CHOOSE
    DUP LED-ATTIVO !
    CASE
        0 OF LED1-ON ENDOF
        1 OF LED2-ON ENDOF
        2 OF LED3-ON ENDOF
    ENDCASE ;

\ Gestione LED RGB in base ai bottoni
: CONTROLLA-BOTTONI
    RGB-OFF 
    BOTTONE-ROSSO-PREMUTO IF RGB-R-ON THEN
    BOTTONE-VERDE-PREMUTO IF RGB-G-ON THEN
    BOTTONE-BLU-PREMUTO IF RGB-B-ON THEN ;

\ Suono di fine partita 
: RGB-FINE-PARTITA
    RGB-COLORE @ CASE
        0 OF RGB-R-ON ENDOF
        1 OF RGB-G-ON ENDOF
        2 OF RGB-B-ON ENDOF
    ENDCASE ;

: SUONO-FINE-PARTITA
    BUZZER-ON 
    200000 DELAY 
    BUZZER-OFF
    100000 DELAY
    BUZZER-ON 
    200000 DELAY 
    BUZZER-OFF ;

\ Inizializzazione
: INIT-STATE
    ALL-OFF
    RGB-OFF
    0 STATO-GIOCO !
    -1 LED-ATTIVO !
    TRUE PARTITA-ATTIVA ! ;

\ Gestione di una singola partita 
: GIOCA-PARTITA
    0 STATO-GIOCO !
    TRUE PARTITA-ATTIVA !
    BLINK
    BEGIN
        STATO-GIOCO @ CASE
            0 OF \ Stato iniziale: accendi LED principale random
                ACCENDI-LED-RANDOM
                1 STATO-GIOCO !
            ENDOF
            1 OF \ Attesa pressione bottone
                QUALSIASI-BOTTONE-PREMUTO IF
                    ALL-OFF \ Spegni il LED principale
                    2 STATO-GIOCO !
                THEN
            ENDOF
            2 OF \ Controllo LED RGB, memorizzazione colore e gestione suono
                CONTROLLA-BOTTONI
                BOTTONE-ROSSO-PREMUTO IF 0 RGB-COLORE ! THEN
                BOTTONE-VERDE-PREMUTO IF 1 RGB-COLORE ! THEN
                BOTTONE-BLU-PREMUTO IF 2 RGB-COLORE ! THEN
                QUALSIASI-BOTTONE-PREMUTO IF
                    ALL-OFF \ Spegni tutti i LED principali
                    RGB-FINE-PARTITA \ Accendi il LED RGB del colore corretto
                    SUONO-FINE-PARTITA \ Suono di fine partita
                    RGB-OFF \ Spegni il LED RGB solo dopo il suono
                    FALSE PARTITA-ATTIVA ! \ Termina la partita
                THEN
            ENDOF
        ENDCASE
        1000 DELAY 
        PARTITA-ATTIVA @ 0= IF EXIT THEN \ Esci dal loop se la partita è finita
    AGAIN ;

\ Loop principale con più partite
: AVVIA
    BEGIN
        INIT-STATE \ Inizializza una nuova partita
        GIOCA-PARTITA \ Gioca una partita
    AGAIN ;

\ Avvia il gioco
AVVIA