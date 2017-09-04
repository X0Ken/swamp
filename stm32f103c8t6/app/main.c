#include "stm32f10x.h"
#include "delay.h"
#include "ads1115.h"
#include "serial.h"
#include "switch.h"

#define CHECK_TIMES 500


void out_datas(char result[], int max_t){
    for (int i = 0; i < max_t; i++) {
        Serial_Send(result[i * 2]);
        Serial_Send(result[i * 2 + 1]);
        Serial_Send(0);
    }
}
void get_datas(char result[], int max_i, int max_t){
    char r[2];
    for (int i = 0; i < max_t; i++) {
        ad_get_data(r);
        result[i * 2] = r[0];
        result[i * 2 + 1] = r[1];
        if (max_i < (result[i * 2] << 8 | result[i * 2 + 1])){
            for (; i <  max_t; i++){
                result[i * 2] = 0x34;
                result[i * 2 + 1] = 0x15;
            }
        }
    }
}



void checkout(int max_i, int max_t){
    char result[CHECK_TIMES * 2];
    res_swtich(0);
    delay_s(1);
    power_switch(1);

    get_datas(result, max_i, max_t);
    res_swtich(1);
    delay_s(1);
    power_switch(0);

    out_datas(result, max_t);
}

int main()
{
  char r[2];
  int max_i = 0;
  int max_t = 0;

  Serial_Init();
  init_switch();
  InitADS1115();


  res_swtich(1);
  power_switch(0);

  while(1){
      switch (Serial_Get()) {
          case 'c':
              max_i = Serial_Get() << 8;
              max_i |= Serial_Get();
              max_t = Serial_Get() << 8;
              max_t |= Serial_Get();
              Serial_Send('o');
              checkout(max_i, max_t);
              Serial_Send('o');
              break;
          case '1':
              Serial_Send('o');
              ad_get_data(r);
              out_datas(r, 1);
              Serial_Send('o');
              break;
          case 'o':
              Serial_Send('o');
              break;
          default:
              Serial_Send('e');
              break;
      }
  }
}
