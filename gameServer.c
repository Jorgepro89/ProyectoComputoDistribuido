#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <netdb.h>
#include <signal.h>	// it is required to call signal handler functions
#include <unistd.h>  // it is required to close the socket descriptor
#include <errno.h>
#include <time.h>

#define  DIRSIZE   2048      /* longitud maxima parametro entrada/salida */
#define  msgSIZE   2048      /* longitud maxima parametro entrada/salida */
#define  PUERTO   15000	     /* numero puerto arbitrario */

int                  sd, sd_actual;  /* descriptores de sockets */
int                  addrlen;        /* longitud direcciones */
struct sockaddr_in   sind, pin;      /* direcciones sockets cliente u servidor */

char* words[] = {"locomotora", "adios", "buenos", "dias", "noche", "ajedrez", "tarde", "teclado", "familia", "gracias", "manzana", "favor", "amigo", "amiga", "familia", "trabajo", "computadora", "coche", "comida", "bebida", "monitor", "pimienta", "cerveza", "fiesta", "musica", "baile", "vacuna", "teatro", "murcielago", "libro", "pelicula", "juego", "deporte", "futbol", "baloncesto", "tenis", "natacion", "pimentel", "avion", "tren", "barco", "hotel", "playa", "montana", "ciudad", "campo", "naturaleza", "vida"};

char* getRandomWord() {
  srand(time(NULL));
  int index = rand() % 50;
  return words[index];
}

/*  procedimiento de aborte del servidor, si llega una senal SIGINT */
/* ( <ctrl> <c> ) se cierra el socket y se aborta el programa       */
void aborta_handler(int sig){
   printf("....abortando el proceso servidor %d\n",sig);
   close(sd);  
   close(sd_actual); 
   exit(1);
}


int main(){
  
	char  dir[DIRSIZE];	     /* parametro entrada y salida */
	char usernames[100][11];
    int numUsernames = 0;
    char passwords[100][11];
    int numPasswords = 0;
    char victorias[100][3];
    int numVictorias = 0;
    char derrotas[100][3];
    int numDerrotas = 0;
    FILE *fp;
    char buffer[100];
    fp = fopen("users.txt", "r");
    if (fp == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    while (fgets(buffer, 100, fp)) {
        buffer[strcspn(buffer, "\n")] = '\0';
        char input[100];
        strcpy(input,buffer);
        char* token;
        token = strtok(input, " ");
        while (token != NULL) {
            if(numPasswords <= numDerrotas){
                if(numUsernames == numPasswords){
                    strcpy(usernames[numUsernames], token);
                    numUsernames++;
                }else{
                    strcpy(passwords[numPasswords], token);
                    numPasswords++;
                }
            }else{
                if(numVictorias == numDerrotas){
                    strcpy(victorias[numVictorias], token);
                    numVictorias++;
                }else{
                    strcpy(derrotas[numDerrotas], token);
                    numDerrotas++;
                }
            }
           
            token = strtok(NULL, " ");
        }
    }
    fclose(fp);
    /*for (int i = 0; i < numUsernames; i++)
    {
        printf("%s -- %s -- %s-%s\n", usernames[i], passwords[i], victorias[i], derrotas[i]);
    }*/
    

	/*
	When the user presses <Ctrl + C>, the aborta_handler function will be called, 
	and such a message will be printed. 
	Note that the signal function returns SIG_ERR if it is unable to set the 
	signal handler, executing line 54.
	*/	
    if(signal(SIGINT, aborta_handler) == SIG_ERR){
        perror("Could not set signal handler");
        return 1;
    }

/* obtencion de un socket tipo internet */
	if ((sd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
		perror("socket");
		exit(1);
	}

/* asignar direcciones en la estructura de direcciones */
	sind.sin_family = AF_INET;
	sind.sin_addr.s_addr = INADDR_ANY;   /* INADDR_ANY=0x000000 = yo mismo */
	sind.sin_port = htons(PUERTO);       /*  convirtiendo a formato red */

/* asociando el socket al numero de puerto */
	if (bind(sd, (struct sockaddr *)&sind, sizeof(sind)) == -1) {
		perror("bind");
		exit(1);
	}

/* ponerse a escuchar a traves del socket */
	if (listen(sd, 5) == -1) {
		perror("listen");
		exit(1);
	}
    int numConnections = 0;
    int numConnectionsFd[2]; // array to hold read and write file descriptors
    char ncbuf[1024];
    int buscandoJugarFd[2]; // array to hold read and write file descriptors
    char bjbuf[2048];
    int EncontradoJugarFd[2]; // array to hold read and write file descriptors
    char ejbuf[2048];
    int jugandoFd[2];
    char jgbuf[2048];
    if (pipe(numConnectionsFd) == -1) {
        perror("pipe");
        //exit(EXIT_FAILURE);
    }
    if (pipe(buscandoJugarFd) == -1) {
        perror("pipe");
        //exit(EXIT_FAILURE);
    }
    if (pipe(EncontradoJugarFd) == -1) {
        perror("pipe");
        //exit(EXIT_FAILURE);
    }
    if (pipe(jugandoFd) == -1) {
        perror("pipe");
        //exit(EXIT_FAILURE);
    }
    pid_t child_pid = 1;
    int running = 1;
    int startScreen = 1;
    int mainMenu = 0;
    int buscando = 0;
    int info = 0;
    char predBmsg[msgSIZE] = "$$$";
    if (write(buscandoJugarFd[1], predBmsg, strlen(predBmsg)+1) == -1) {
        perror("Error writing to pipe");
        //exit(EXIT_FAILURE);
    }else{
        //close(buscandoJugarFd[1]);
    }
    //close(buscandoJugarFd[1]);
    if (write(EncontradoJugarFd[1], predBmsg, strlen(predBmsg)+1) == -1) {
        fprintf(stderr, "Error writing to pipe: %s\n", strerror(errno));
        //exit(EXIT_FAILURE);
    }else{
        //close(EncontradoJugarFd[1]);
    }
    do
    {
    
        //close(EncontradoJugarFd[1]);
        if (child_pid != 0){
            /* esperando que un cliente solicite un servicio */
            sd_actual = accept(sd, (struct sockaddr *)&pin, &addrlen);
            if (sd_actual == -1) {
                perror("accept");
                exit(1);
            }
            child_pid = fork();
        }
        if (child_pid == 0){
            int new_fd = numConnectionsFd[0]+numConnectionsFd[1]+buscandoJugarFd[0]+buscandoJugarFd[1]+EncontradoJugarFd[0]+EncontradoJugarFd[1]+jugandoFd[0]+jugandoFd[1];
            if (dup2(sd_actual, new_fd) == -1) {}
            sd_actual = new_fd;
            while(running){
                char username[11]="";
                char password[11]="";
                char win[3] = "";
                char lose[3] = "";
                if(startScreen){
                    char msg[msgSIZE];	     /* parametro entrada y salida */
                    int n = recv(sd_actual, msg, sizeof(msg), 0);
                    if (n == -1) {
                        perror("recv");
                        exit(1);
                    }
                    msg[n] = '\0';
                    char* token;
                    token = strtok(msg, " ");
                    while (token != NULL) {
                        if(strcmp(username,"")==0){
                            strcpy(username, &token[1]);
                        }else{
                            strcpy(password, token);
                        }
                        token = strtok(NULL, " ");
                    }
                    if(msg[0] == 'L'){
                        int correctLogin = 0;
                        char retMsg[msgSIZE];
                        for (int i = 0; i < numUsernames; i++)
                        {
                            if(strcmp(usernames[i],username)==0){
                                if(strcmp(passwords[i],password)==0){
                                    correctLogin = 1;
                                    strcpy(win, victorias[i]);
                                    strcpy(lose, derrotas[i]);
                                }
                            }
                        }
                        printf("%s %s\n",username,password);
                        if(correctLogin){
                            strcpy(retMsg, "Correct");
                            numConnections++;
                            char connections[2048];
                            sprintf(connections, "%d", numConnections);
                            if (write(numConnectionsFd[1], connections, strlen(connections)+1) == -1) {
                                perror("Error writing to pipe");
                                //exit(EXIT_FAILURE);
                            }
                            mainMenu = 1;
                            startScreen = 0;
                        }else{
                            strcpy(retMsg, "Incorrect");
                        }
                        int sent;
                        sent = send(sd_actual, retMsg, strlen(retMsg), 0);
                        if ( sent == -1) {
                            printf("%s\n",retMsg);
                            perror("send");
                            exit(1);
                        }             
                    }else if(msg[0] == 'R'){
                        int correctRegister = 0;
                        int userExists = 0;
                        char retMsg[msgSIZE];
                        for (int i = 0; i < numUsernames; i++)
                        {
                            if(strcmp(usernames[i],username)==0){
                                userExists = 1;
                                break;
                            }
                        }
                        if(!userExists){
                            strcpy(retMsg, "Correcto Registro");
                            strcpy(usernames[numUsernames], username);
                            numUsernames++;
                            strcpy(passwords[numPasswords], password);
                            numPasswords++;
                            strcpy(win,"0");
                            strcpy(lose,"0");
                            strcpy(victorias[numVictorias], "0");
                            numVictorias++;
                            strcpy(derrotas[numDerrotas], "0");
                            numDerrotas++;
                            FILE *file;
                            file = fopen("users.txt", "a");
                            char text[50];
                            strcpy(text,username);
                            strcat(text," ");
                            strcat(text,password);
                            strcat(text," ");
                            strcat(text, win);
                            strcat(text, " ");
                            strcat(text, lose);
                            strcat(text, '\n');
                            fprintf(file, "%s", text);
                            fclose(file);
                            
                            numConnections++;
                            char connections[2048];
                            sprintf(connections, "%d", numConnections);
                            if (write(numConnectionsFd[1], connections, strlen(connections)+1) == -1) {
                                perror("Error writing to pipe");
                                //exit(EXIT_FAILURE);
                            }
                                (numConnectionsFd[1]);
                            mainMenu = 1;
                            startScreen = 0;
                        }else{
                            strcpy(retMsg, "Incorrecto Registro");
                        }
                        int sent;
                        sent = send(sd_actual, retMsg, strlen(retMsg), 0);
                        if ( sent == -1) {
                            perror("send");
                            exit(1);
                        }
                    }
                }
                char msg[msgSIZE];
                char retMsg[msgSIZE];
                while(mainMenu){
                    /* parametro entrada y salida */
                    int n = recv(sd_actual, msg, sizeof(msg), 0);
                    if (n == -1) {
                        perror("recv");
                        exit(1);
                    }
                    msg[n] = '\0';
                    printf("--%s\n",msg);
                    if(msg[0]=='M'){
                        // Close the write end of the pipe
                        //close(numConnectionsFd[1]);
                        // Read from the pipe
                        /*int bytesRead = read(numConnectionsFd[0], ncbuf, sizeof(ncbuf));
                        if (bytesRead == -1) {
                            // Handle read error
                            //perror("Error reading from pipe");
                            strcpy(retMsg,"err");
                            //exit(EXIT_FAILURE);
                        } else if (bytesRead == 0) {
                            // Pipe has been closed unexpectedly
                            fprintf(stderr, "Unexpected end of file from pipe");
                            //exit(EXIT_FAILURE);
                        } else {
                            // Read successful
                            // Copy contents of buffer to return message
                            strcpy(retMsg, ncbuf);
                        }*/
                        strcpy(retMsg,"..");
                        // Close the read end of the pipe
                        //close(numConnectionsFd[0]);
                    }else if(msg[0] == 'B'){
                        mainMenu = 0;
                        buscando = 1;
                    }
                    else{
                        strcpy(retMsg,"err");
                    }
                    int sent;
                    sent = send(sd_actual, retMsg, strlen(retMsg), 0);
                    if ( sent == -1) {
                        perror("send");
                        exit(1);
                    }
                }
                while (buscando)
                {
                    printf("Buscando\n");
                    /* parametro entrada y salida */
                    int n = recv(sd_actual, msg, sizeof(msg), 0);
                    if (n == -1) {
                        printf("recvError\n");
                        perror("recv");
                        exit(1);
                    }
                    msg[n] = '\0';
                    printf("%s\n",msg);
                    if(msg[0]=='B'){
                        strcpy(retMsg,"#");
                        char bMsg[msgSIZE];
                        strcpy(bMsg,"#");
                        strcat(bMsg,username);
                        strcat(bMsg," ");
                        strcat(bMsg,password);
                        strcat(bMsg," ");
                        strcat(bMsg,win);
                        strcat(bMsg," ");
                        strcat(bMsg,lose);
                        // Close the write end of the pipe
                        //close(numConnectionsFd[1]);
                        // Read from the pipe
                        int bytesRead = read(buscandoJugarFd[0], bjbuf, sizeof(bjbuf));
                        if (bytesRead == -1) {
                            // Handle read error
                            //perror("Error reading from pipe");
                            strcpy(retMsg,"err");
                            //exit(EXIT_FAILURE);
                        } else if (bytesRead == 0) {
                            // Pipe has been closed unexpectedly
                            fprintf(stderr, "Unexpected end of file from pipe1");
                            //exit(EXIT_FAILURE);
                        } else {
                            // Read successful
                            // Copy contents of buffer to return message
                            if (bjbuf[0] != '#')
                            {
                                if (write(buscandoJugarFd[1], bMsg, strlen(bMsg)+1) == -1) {
                                    perror("Error writing to pipe");
                                    //exit(EXIT_FAILURE);
                                }
                                else{
                                    printf("***%s\n",bMsg);
                                }
                                //close(buscandoJugarFd[1]);
                                printf("Jugador Encontrado\n");
                                char sendWord[100] = "!";
                                char* randomWord = getRandomWord();
                                strcat(sendWord, randomWord);
                                strcpy(retMsg, sendWord);
                                //close(buscandoJugarFd[1]);
                                //close(EncontradoJugarFd[1]);
                                buscando = 0;
                                info = 0;

                            }else{
                                /*if (write(buscandoJugarFd[1], bjbuf, strlen(bjbuf)+1) == -1) {
                                    perror("Error writing to pipe");
                                    //exit(EXIT_FAILURE);
                                }*/
                                int bytesRead = read(EncontradoJugarFd[0], ejbuf, sizeof(ejbuf));
                                if (bytesRead == -1) {
                                    // Handle read error
                                    //perror("Error reading from pipe");
                                    strcpy(retMsg,"err");
                                    //exit(EXIT_FAILURE);
                                } else if (bytesRead == 0) {
                                    // Pipe has been closed unexpectedly
                                    fprintf(stderr, "Unexpected end of file from pipe2");
                                    //exit(EXIT_FAILURE);
                                } else {
                                    // Read successful
                                    // Copy contents of buffer to return message
                                    if (ejbuf[0] != '#')
                                    {
                                        if (write(EncontradoJugarFd[1], bMsg, strlen(bMsg)+1) == -1) {
                                            perror("Error writing to pipe");
                                            //exit(EXIT_FAILURE);
                                        }
                                        //close(EncontradoJugarFd[1]);
                                        buscando = 0;
                                        info = 0;
                                        //close(buscandoJugarFd[1]);
                                        //close(EncontradoJugarFd[1]);
                                        printf("Jugador Encontrado\n");
                                        char txt[10] = "1";
                                        if (write(jugandoFd[1], txt, strlen(txt)) == -1) {
                                            perror("Error writing to pipe");
                                            //exit(EXIT_FAILURE);
                                        }
                                        char sendWord[100] = "!";
                                        char* randomWord = getRandomWord();
                                        strcat(sendWord, randomWord);
                                        strcpy(retMsg, sendWord);
                                    }else{
                                        
                                    }                            
                                }                               
                                
                            }
                            
                        }
                        
                        // Close the read end of the pipe
                        //close(numConnectionsFd[0]);
                    }else if(msg[0] == 'C'){
                        mainMenu = 1;
                        buscando = 0;
                    }
                    else{
                        strcpy(retMsg,"err");
                    }
                    int sent;
                    sent = send(sd_actual, retMsg, strlen(retMsg), 0);
                    if ( sent == -1) {
                        perror("send");
                        exit(1);
                    }
                }
                char p1[2048];
                char p2[2048];
                while (info)
                {
                    /* parametro entrada y salida */
                    int n = recv(sd_actual, msg, sizeof(msg), 0);
                    if (n == -1) {
                        perror("recv");
                        exit(1);
                    }
                    msg[n] = '\0';
                    int bytesRead = read(jugandoFd[0], jgbuf, sizeof(jgbuf));
                    if (jgbuf[0]=='1'){
                        info = 0;
                        strcpy(retMsg,"play");
                    }
                                       
                    int sent;
                    retMsg[strlen(retMsg)] = '\0';
                    sent = send(sd_actual, retMsg, strlen(retMsg)+1, 0);
                    if ( sent == -1) {
                        perror("send");
                        exit(1);
                    }
                    
                }

                while (1)
                {
                    /* parametro entrada y salida */
                    int n = recv(sd_actual, msg, sizeof(msg), 0);
                    if (n == -1) {
                        perror("recv");
                        exit(1);
                    }
                    msg[n] = '\0';
                    if (msg[0]=='F')
                    {
                        strcpy(retMsg,"Close");
                        running = 1;
                        int sent;
                        retMsg[strlen(retMsg)] = '\0';
                        sent = send(sd_actual, retMsg, strlen(retMsg)+1, 0);
                        if ( sent == -1) {
                            perror("send");
                            exit(1);
                        }
                        break;
                    }else{
                        strcpy(retMsg,"Open");
                    }
                    
                    int sent;
                    retMsg[strlen(retMsg)] = '\0';
                    sent = send(sd_actual, retMsg, strlen(retMsg)+1, 0);
                    if ( sent == -1) {
                        perror("send");
                        exit(1);
                    }
                }
                
                
                
            }
        }
        
    } while (1);	

	/* cerrar los dos sockets */
	close(sd_actual);  
	close(sd);
	printf("Conexion cerrada\n");
	return 0;
}
