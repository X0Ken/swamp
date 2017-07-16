PREFIX := arm-none-eabi-
CC=$(PREFIX)gcc
OBJCOPY=$(PREFIX)objcopy

EXECUTABLE=stm32_executable.elf
BIN_IMAGE=stm32_bin_image.bin
STARTUP_OBJ=startup_stm32f10x_md.o

#======================================================================#
#Flags
CFLAGS=-Wall -mlittle-endian -mthumb -std=c11 --specs=nosys.specs
CFLAGS+=-mcpu=cortex-m3
CFLAGS+=-D USE_STDPERIPH_DRIVER
CFLAGS+=-D STM32F10X_MD
#stm32-flash
CFLAGS+=-Wl,-T,../stm32f103c8t6_flash_md.ld

#Stm32 libraries
ST_LIB=../lib/STM32F10x_StdPeriph_Driver
CMSIS_DEVICE_LIB=../lib/CMSIS/CM3/DeviceSupport/ST/STM32F10x

LIB=-I.
LIB+=-I$(ST_LIB)/inc
LIB+=-I../lib/CMSIS/CM3/CoreSupport
LIB+=-I../lib/CMSIS/CM3/DeviceSupport/ST/STM32F10x/

SRC=main.c \
  stm32f10x_it.c \
  serial.c \
  ads1115.c \
  delay.c \
  switch.c \
  $(ST_LIB)/src/misc.c \
  $(ST_LIB)/src/stm32f10x_rcc.c \
  $(ST_LIB)/src/stm32f10x_i2c.c \
  $(ST_LIB)/src/stm32f10x_gpio.c \
  $(ST_LIB)/src/stm32f10x_usart.c

#setup system clock
SRC+=$(CMSIS_DEVICE_LIB)/system_stm32f10x.c

STARTUP=../lib/CMSIS/CM3/DeviceSupport/ST/STM32F10x/startup/gcc_ride7/startup_stm32f10x_md.s


.PHONY: all clean

#Make all
all:$(BIN_IMAGE)

$(BIN_IMAGE):$(EXECUTABLE)
	$(OBJCOPY) -O binary $^ $@

$(STARTUP_OBJ): $(STARTUP)
	$(CC) $(CFLAGS) $^ -c $(STARTUP)

$(EXECUTABLE):$(SRC)  $(STARTUP_OBJ)
	$(CC) $(CFLAGS) $(LIB) $^ -o $@

clean:
	rm -rf $(STARTUP_OBJ)
	rm -rf $(EXECUTABLE)
	rm -rf $(BIN_IMAGE)
