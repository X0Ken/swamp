#include "ads1115.h"

GPIO_InitTypeDef i2c_gpio;
I2C_InitTypeDef i2c;

void I2C_start(I2C_TypeDef* I2Cx,  uint8_t direction, uint8_t address){
	// wait until I2C1 is not busy anymore
	while(I2C_GetFlagStatus(I2Cx, I2C_FLAG_BUSY));

	// Send I2C1 START condition
	I2C_GenerateSTART(I2Cx, ENABLE);

	// wait for I2C1 EV5 --> Slave has acknowledged start condition
	while(!I2C_CheckEvent(I2Cx, I2C_EVENT_MASTER_MODE_SELECT));

	// Send slave Address for write
	I2C_Send7bitAddress(I2Cx, address, direction);

	/* wait for I2C1 EV6, check if
	 * either Slave has acknowledged Master transmitter or
	 * Master receiver mode, depending on the transmission
	 * direction
	 */
	if(direction == I2C_Direction_Transmitter){
		while(!I2C_CheckEvent(I2Cx, I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED));
	}
	else if(direction == I2C_Direction_Receiver){
		while(!I2C_CheckEvent(I2Cx, I2C_EVENT_MASTER_RECEIVER_MODE_SELECTED));
	}
}

void I2C_Write_Data(I2C_TypeDef* I2Cx, uint8_t data)
{
	/* This function transmits one byte to the slave device
	 * Parameters:
	 *		I2Cx --> the I2C peripheral e.g. I2C1
	 *		data --> the data byte to be transmitted
	 */
	I2C_SendData(I2Cx, data);
	// wait for I2C1 EV8_2 --> byte has been transmitted
	while(!I2C_CheckEvent(I2Cx, I2C_EVENT_MASTER_BYTE_TRANSMITTED));
}

uint8_t I2C_Read_ack(I2C_TypeDef* I2Cx){
	/* This function reads one byte from the slave device
	 * and acknowledges the byte (requests another byte)
	 */
	// enable acknowledge of recieved data
	I2C_AcknowledgeConfig(I2Cx, ENABLE);
	// wait until one byte has been received
	while( !I2C_CheckEvent(I2Cx, I2C_EVENT_MASTER_BYTE_RECEIVED) );
	// read data from I2C data register and return data byte
	uint8_t data = I2C_ReceiveData(I2Cx);
	return data;
}

	/* This function reads one byte from the slave device
	 * and doesn't acknowledge the recieved data
	 */
uint8_t I2C_Read_nack(I2C_TypeDef* I2Cx){
	// disabe acknowledge of received data
	// nack also generates stop condition after last byte received
	// see reference manual for more info
	I2C_AcknowledgeConfig(I2Cx, DISABLE);
	I2C_GenerateSTOP(I2Cx, ENABLE);
	// wait until one byte has been received
	while( !I2C_CheckEvent(I2Cx, I2C_EVENT_MASTER_BYTE_RECEIVED) );
	// read data from I2C data register and return data byte
	uint8_t data = I2C_ReceiveData(I2Cx);
	return data;
}

void I2c_Init()
{
    GPIO_InitTypeDef i2c_gpio;
    I2C_InitTypeDef i2c;

    RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB,ENABLE);
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO, ENABLE);
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_I2C1, ENABLE);

    i2c.I2C_ClockSpeed = 10000;
    i2c.I2C_Mode = I2C_Mode_I2C;
    i2c.I2C_DutyCycle = I2C_DutyCycle_2;
    i2c.I2C_OwnAddress1 = 0xa2;
    i2c.I2C_Ack = I2C_Ack_Enable;
    i2c.I2C_AcknowledgedAddress = I2C_AcknowledgedAddress_7bit;
    I2C_Init(I2C1, &i2c);

    i2c_gpio.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;
    i2c_gpio.GPIO_Mode = GPIO_Mode_AF_OD;
    i2c_gpio.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &i2c_gpio);

    I2C_Cmd(I2C1, ENABLE);
}



void InitADS1115()
{
	I2c_Init();
	uint8_t conf[2];
    conf[0] = 0xc0;
    conf[1] = 0xe3;
    //send config
	I2C_start(I2C1,I2C_Direction_Transmitter,ADS1115_ADDR);
	I2C_Write_Data(I2C1,CONFIG_REGISTER);
    I2C_Write_Data(I2C1,conf[0]);
	I2C_Write_Data(I2C1,conf[1]);
	I2C_GenerateSTOP(I2C1,ENABLE);
}


void ad_get_data(char i2c_data[])
{
	//Request
	I2C_start(I2C1,I2C_Direction_Transmitter,ADS1115_ADDR);
	I2C_Write_Data(I2C1,CONVERTION_REGISTER);
	I2C_GenerateSTOP(I2C1,ENABLE);
	//Response
	I2C_start(I2C1,I2C_Direction_Receiver,ADS1115_ADDR);
	i2c_data[0] = I2C_Read_ack(I2C1);
	i2c_data[1] = I2C_Read_nack(I2C1);
	I2C_GenerateSTOP(I2C1,ENABLE);
}
