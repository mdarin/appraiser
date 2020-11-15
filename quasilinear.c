/*
    Процесс сбора и обработки данных на программе, читающей пословно файл и
    включающей слова в динамический массив указателей(ДМУ) с сохранением порядка,
    для каждого слова производится бинарный поиск его длины от 0 до текущего sz. 
    И для каждого слова вычисляется чило Фибоначчи.
    При этом sz периодически удваиватеся.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>

#define SIZE0 100					                // Начальная размерность ДМУ
#define STRLEN_MAX 1000


int cnt = 0;                                        // Счетчик сравнений

int binary_search(int a, int b, int item);
char **loadfile(FILE *fd);
int fib(int n);

/*
    Значения счетчика операций сравнения cnt и «грязного» времени 
    работы программы clock()-T0 выводятся в консоль 
*/
char **loadfile(FILE *fd) {
    char str[STRLEN_MAX] = {0};
    int n = 0;				                        // Кол-во строк
    size_t sz = SIZE0;                              // размерность ДМУ
    char **pp = malloc(sizeof(*pp) * sz);		    // Создать ДМУ
    long T0 = clock();                              // Начальное значение времени [ms]

    while (fscanf(fd, "%s", str) == 1 ) {

        pp[n] = strdup(str);			            // Копия строки в ДМ

        binary_search(0, sz, strlen(pp[n]));        // трудоёмкость по операциям дихотомии  имеет вид T=log(N)

        fib(1000*sz);                               // трудоёмкость по операции вычисления чисела Фибоначи быстрым
                                                    // возведением матрицы в степень имеет вид T=log(N)

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
    A dichotomy method
 */
int binary_search(int a, int b, int item) {
    int low = a;
    int high = b;
    int mid = 0;

    while (low <= high) {
        for (int i = 0; i < 2000; i++) { // артефакт утяжелитель
            continue;
        }

        cnt++;		        			// Увеличение счетчика сравнений

        mid = low + (high - low) / 2;                 

        if (mid < item) {                         
            low = mid + 1;                
        } else {
            high = mid - 1;      
        }
    }  

    mid = (low + high) / 2 + 1;

    return mid; 
}


/* 
    Вычисление чисел Фибоначчи быстрым возведением матрицы в степень
    Функция возвращает n-е число Фибоначчи
*/
int fib(int n) {
                                         // Инициализируем матрицу
    int a = 1, ta, 
        b = 1, tb,
        c = 1, rc = 0,  tc,
        d = 0, rd = 1; 
        
    while (n) { 
        for (int i = 0; i < 2000; i++) { // артефакт утяжелитель
            continue;
        }

        cnt++;		        		    // Увеличение счетчика сравнений

        if (n & 1) {                    // Если степень нечетная
                                        // Умножаем вектор R на матрицу A
            tc = rc;
            rc = rc*a + rd*c;
            rd = tc*b + rd*d;
        } 

                                        // Умножаем матрицу A на саму себя
        ta = a; tb = b; tc = c;
        a = a*a  + b*c;
        b = ta*b + b*d;
        c = c*ta + d*c;     
        d = tc*tb+ d*d;

        n >>= 1;                        // Уменьшаем степень вдвое

    }  

    return rc;
}


/*
    Main driver
*/
int main(){ 
    int i = 0;
    FILE *fd = fopen("text2.txt", "r");
    char **pp = loadfile(fd);

    // убрать за собой
    for (i = 0; pp[i] != NULL; i++) free(pp[i]);
    free(pp);
    fclose(fd);

    return 0;
}