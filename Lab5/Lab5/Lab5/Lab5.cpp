#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 10

int main() {
    setlocale(LC_ALL, "Russian");
    char buffer[BUFFER_SIZE]; 
    char input[100]; 

    printf("Введите данные: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        printf("Ошибка ввода!\n");
        return 1;
    }

    input[strcspn(input, "\n")] = '\0';

    if (strlen(input) >= BUFFER_SIZE) {
        printf("Ошибка: ввод превышает размер буфера!\n");
        return 1;
    }

    strcpy(buffer, input);
    buffer[BUFFER_SIZE - 1] = '\0'; 

    printf("Буфер содержит: %s\n", buffer);

    return 0;
}