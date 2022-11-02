#include <iostream>
#include <vector>
#include <string>
#include "hardware/i2c.h" //i2c protocol library
#include "pico/stdlib.h" //raspberry pi pico library

#define I2C_PORT i2c0; //GPIO Pins 4 and 5
static int addr = 0x28; // default adafruit address (peripheral)

// Initialize Accelerometer Function
void accel_init(void){
    //check to see that connection is correct
    //should expect the chip to have an ID of 0xA0 or 1010_0000
    sleep_ms(10000); //add short delay to help  BNO055
    uint8_t reg = 0x00;
    uint8_t chipID[1];
    i2c_write_blocking(I2C_PORT, addr, &reg, 1, true); //true: controller maintains control of I2C bus - no stop msg
    i2c_read_blocking(I2C_PORT, addr, chipID, 1, false); //false: controller releases control

    if(chipID[0] != 0xA0){
        while(1){
            printf("Chip ID Not Correct - Check Connection");
            sleep_ms(5000);
        }
    }

    // Use internal oscillator
    uint8_t data[2]; //2 unsigned 8 bit ints
    data[0] = 0x3F; //register addr we want to send
    data[1] = 0x40; //data we want to transmit
    i2c_write_blocking(I2C_PORT, addr, data, 2, true);

    // Reset all interrupt status bits
    data[0] = 0x3F;
    data[1] = 0x01;
    i2c_write_blocking(I2C_PORT, addr, data, 2, true);

    // Configure Power Mode
    data[0] = 0x3E;
    data[1] = 0x00;
    i2c_write_blocking(I2C_PORT, addr, data, 2, true);
    sleep_ms(50);

    // Defaul Axis Configuration
    data[0] = 0x41;
    data[1] = 0x24;
    i2c_write_blocking(I2C_PORT, addr, data, 2, true);

    // Default Axis Signs
    data[0] = 0x42;
    data[1] = 0x00;
    i2c_write_blocking(I2C_PORT, addr, data, 2, true);

    // Set units to m/s^2
    data[0] = 0x3B;
    data[1] = 0b0001000;
    i2c_write_blocking(I2C_PORT, addr, data, 2, true);
    sleep_ms(30);

    // Set operation to acceleration only
    data[0] = 0x3D;
    data[1] = 0x0C;
    i2c_write_blocking(I2C_PORT, addr, data, 2, true);
    sleep_ms(100);

}//end accel_init

int main(){
    //Initizalize STD I/O for printing over serial over USB interface
    stdio_init_all();

    //Configure the I2C Coms
    12c_init(I2C_PORT, 400000); //400kHz
    gpio_set_function(4, GPIO_FUNC_I2C); //SCL - GPIO 4
    gpio_set_function(5, GPIO_FUNC_I2C); //SDA - GPIO 5
    //enable pull-up resistors for SCL and SDA
    gpio_pull_up(4); 
    gpio_pull_up(5);

    //Call accelerometer initialization funct
    accel_init();

    uint8_t accel[6]; // Store data from the 6 acceleration regs
    int16_t accelX, accelY, accelZ; // combined 3 axis data
    float f_accelX, f_accelY, f_accelZ; // float type of accel data
    uint8_t val = 0x08; // start reg addr

    while(1){
        i2c_write_blocking(I2C_PORT, addr, &val, 1, true);
        i2c_read_blocking(I2C_PORT, addr, accel, 6, false);

        accelX = ((accel[1] << 8) | accel[0]);
        accelY = ((accel[3] << 8) | accel[2]);
        accelZ = ((accel[5] << 8) | accel[4]);

        f_accelX = accelX / 100.00;
        f_accelY = accelY / 100.00;
        f_accelZ = accelZ / 100.00;

        // Print to serial monitor
        printf("X: &6.2f    Y: %6.2f    Z: %6.2f\n", f_accelX, f_accelY, f_accelZ);
        sleep_ms(300);
    }

}//end main

/*
Data Output from BNO0
-Absolute Orientation - Euler Vector 100Hz
    3 axis orientation data based on a 360 degrees sphere
-Absolute Orientation - Quaterion 100Hz
    4 point quaternion output for more accurate data manipulation

-Angular Velocity Vector 100Hz - gyroscope
    3 axis of 'rotation speed' in rad/s

-Acceleration Vector 100Hz
    3 axis of acceleration (gravity + linear motion) in m/s^2
-Linear Acceleration Vector 100Hz
    3 axis of linear acceleration data (acceleration minus gravity) in m/s^2
-Gravity Vector 100Hz
    3 axis of gravitational acceleration (minus any movement) in m/s^2

-Magnetic Field Strength Vector 20Hz
    3 axis of magnetic field sensing in micro Tesla (uT)







*/
