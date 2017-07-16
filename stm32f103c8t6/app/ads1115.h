#ifndef __ADS1115_H
#define __ADS1115_H

#include "stm32f10x.h"


void I2C_start(I2C_TypeDef* I2Cx,  uint8_t direction, uint8_t address);

void I2C_Write_Data(I2C_TypeDef* I2Cx, uint8_t data);

uint8_t I2C_Read_ack(I2C_TypeDef* I2Cx);

uint8_t I2C_Read_nack(I2C_TypeDef* I2Cx);


void InitADS1115();
void ad_get_data(char i2c_data[]);

#define ADS1115_ADDR 0x90
#define CONVERTION_REGISTER  0x00   //Convertion register
#define CONFIG_REGISTER  0x01   //Config register

#endif
