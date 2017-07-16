#ifndef __SERIAL_H
#define __SERIAL_H

#include "stm32f10x.h"

void Serial_Init();
int Serial_Send(int ch);
int Serial_Send_Str(char* str);

char Serial_Get();

#endif
