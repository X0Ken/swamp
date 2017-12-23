#include "stm32f10x.h"
#include "delay.h"
#include "ads1115.h"
#include "serial.h"
#include "switch.h"

#define CHECK_TIMES 900


void out_datas(char result[], int count){
    Serial_Send('s');
    Serial_Send(count >> 8);
    Serial_Send(count);
    Serial_Send('d');
    for (int i = 0; i < count; i++) {
        Serial_Send(result[i * 2]);
        Serial_Send(result[i * 2 + 1]);
        Serial_Send(0);
    }
}


int get_datas(char result[], int max_i, int max_t){
    char r[2];
    char herr=0;
    for (int i = 0; i < max_t; i++) {
        ad_get_data(r);
        result[i * 2] = r[0];
        result[i * 2 + 1] = r[1];
        if (max_i < (r[0] << 8 | r[1])){
            herr += 1;
            if (herr > 3){
                return i + 1;
            }
        }
    }
    return max_t;
}



void checkout(int max_i, int max_t){
    char result[CHECK_TIMES * 2];
    int count = 0;
    res_swtich(0);
    delay_s(1);
    power_switch(1);

    count = get_datas(result, max_i, max_t);
    res_swtich(1);
    delay_s(1);
    power_switch(0);

    out_datas(result, count);
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
              if(max_t > CHECK_TIMES){
                  Serial_Send_Str("e_maxt_");
                  break;
              }
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
