/*
    Процесс сбора и обработки данных на программе, читающей пословно файл и
    подсчитывающей количество вхождений слов
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define TARGET_WORD "что"
#define STRLEN_MAX 1000

/*
    Значения счетчика операций сравнения cnt и «грязного» времени 
    работы программы clock()-T0 выводятся в консоль 
*/
int loadfile(FILE* fd){
    int cnt = 0;                                    // Счетчик считанных слов 
    char str[STRLEN_MAX];
    int n = 0;				                        // Кол-во строк
    long T0 = clock();                              // Начальное значение времени [ms]

    while (fscanf(fd, "%s", str) == 1 ) {           // трудоемкость по операции имеет вид T=N
        cnt++;  						            // Увеличение счетчика

        n++;                                        // Вывод статистики на каждые 5000 слов
        if (n%5000 == 0) {
            printf("%d\t%d\t%ld\n", n, cnt, clock()-T0);
        }
    }

    printf("%d\t%d\t%ld\n", n, cnt, clock()-T0);

    return n;
}

/*
    Main driver
*/
int main() { 
    int i = 0;
    FILE *fd = fopen("text.txt", "r");
    char cc[80] = {0};
    int nwords = loadfile(fd);

    // puts("---------------------------------------------");

    // gets(cc);

    return 0;
}