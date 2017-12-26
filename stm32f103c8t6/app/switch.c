#include "switch.h"

void init_switch()
{
	GPIO_InitTypeDef GPIO_InitStructure;
	/* GPIOA Periph clock enable */
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

	/* Configure PA0 and PA1 in output pushpull mode */
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
}


void power_switch(int x){
    if (x) {
        GPIO_SetBits(GPIOA, GPIO_Pin_0);
    }
    else{
        GPIO_ResetBits(GPIOA, GPIO_Pin_0);
    }
}

void res_swtich(int x){

    if (x) {
        GPIO_SetBits(GPIOA, GPIO_Pin_1);
    }
    else{
        GPIO_ResetBits(GPIOA, GPIO_Pin_1);
    }
}
