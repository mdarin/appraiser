/*
    Процесс сбора и обработки данных на программе, читающей пословно файл и
    включающей слова в динамический массив указателей(ДМУ) с сохранением порядка.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SIZE0 100					                // Начальная размерность ДМУ

/*
    Значения счетчика операций сравнения cnt и «грязного» времени 
    работы программы clock()-T0 выводятся в консоль 
*/
char **loadfile(FILE *fd){
    int cnt = 0;                                    // Счетчик сравнений
    char str[1000] = {0};
    int i, j, n = 0, sz = SIZE0;				    // Кол-во строк и размерность ДМУ
    char **pp = malloc(sizeof(*pp) * sz);		    // Создать ДМУ
    long T0 = clock();                              // Начальное значение времени [ms]

    while (fscanf(fd, "%s", str) == 1 ) {
        for (i = 0; i < n; i++) {                   // трудоемкость по операциям сравнения имеет вид T=N2
            cnt++;						            // Увеличение счетчика сравнений      
            if (strcmp(str, pp[i]) < 0) break;
        }

        for (j = n-1; j >= i; j--) {
            pp[j+1] = pp[j];
        }

        pp[i] = strdup(str);			            // Копия строки в ДМ

        n++;                                        // Вывод статистики на каждые 5000 слов
        if (n%5000 == 0) {
            printf("%d\t%d\t%ld\n", n, cnt, clock()-T0);
        }

        if (n+1 == sz) {				            // Будет переполнение - 
            sz *= 2;					            // удвоить размерность
            pp = realloc(pp, sizeof(*pp) * sz);
        }
    }
    pp[n] = NULL;                                   // Ограничитель массива указателей

    printf("%d\t%d\t%ld\n", n, cnt, clock()-T0);

    return pp;
}

/*
    Main driver
*/
int main(){ 
    int i = 0;
    FILE *fd = fopen("text.txt", "r");
    char cc[80] = {0};
    char **pp = loadfile(fd);

    // puts("---------------------------------------------");

    // gets(cc);
    // for (i=0; pp[i]!=NULL; i++) {
    //     printf("%s\n",pp[i]);
    // }

    // убрать за собой
    for (i = 0; pp[i] != NULL; i++) free(pp[i]);
    free(pp);
    fclose(fd);

    return 0;
}