#include "stm32f10x.h"
#include "delay.h"
#include "ads1115.h"
#include "serial.h"
#include "switch.h"

#define CHECK_TIMES 500


void out_datas(char result[]){
    for (int i = 0; i < CHECK_TIMES; i++) {
        Serial_Send(result[i * 2]);
        Serial_Send(result[i * 2 + 1]);
        Serial_Send(0);
    }
}
void get_datas(char result[]){
    char r[2];
    for (int i = 0; i < CHECK_TIMES; i++) {
        ad_get_data(r);
        result[i * 2] = r[0];
        result[i * 2 + 1] = r[1];
    }
}



void checkout(){
    char result[CHECK_TIMES * 2];
    res_swtich(0);
    delay_s(1);
    power_switch(1);

    get_datas(result);
    res_swtich(1);
    delay_s(1);
    power_switch(0);

    out_datas(result);
}

int main()
{
  Serial_Init();
  init_switch();
  InitADS1115();


  res_swtich(1);
  power_switch(0);

  while(1){
      Serial_Send('c');
      switch (Serial_Get()) {
          case 'c':
              Serial_Send('o');
              checkout();
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
