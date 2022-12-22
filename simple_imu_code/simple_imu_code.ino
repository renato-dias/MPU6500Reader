#include <SPI.h>

#define MPU6500_I2C_ADDRESS 0x68
#define MPU6500_REG_ACCEL_CONFIG 0x1C
#define MPU6500_ACCEL_FS_2G 0x00
#define MPU6500_ACCEL_FS_4G 0x08
#define MPU6500_ACCEL_FS_8G 0x10
#define MPU6500_ACCEL_FS_16G 0x18
    // ±2 g: 0x00
    // ±4 g: 0x08
    // ±8 g: 0x10
    // ±16 g: 0x18

const int MPU_CS = 10;  // Chip select pin for the MPU

void setup() {
  // Initialize the SPI interface and the MPU
  Serial.begin(2000000);
  SPI.begin();
  pinMode(MPU_CS, OUTPUT);
  digitalWrite(MPU_CS, HIGH);
  initMPU();
}

void loop() {
  // Read the raw acceleration data from the MPU
  int16_t ax, ay, az;
  readAccelerationData(ax, ay, az);

  // Print the acceleration data to the serial console
  Serial.print(micros());
  Serial.print(",");
  Serial.print(ax);
  Serial.print(",");
  Serial.print(ay);
  Serial.print(",");
  Serial.println(az);
}

void initMPU() {
  // Put the MPU into sleep mode
  writeMPU(0x6B, 0x00);
  // Set the accelerometer full scale range to +/- 2g
  writeMPU(MPU6500_REG_ACCEL_CONFIG, MPU6500_ACCEL_FS_16G);
  // Set the gyro full scale range to +/- 250 degrees/sec
  writeMPU(0x1B, 0x00);
}

void readAccelerationData(int16_t& ax, int16_t& ay, int16_t& az) {
  // Read the raw acceleration data from the MPU
  digitalWrite(MPU_CS, LOW);
  SPI.transfer(0x3B | 0x80);  // Read from the ACCEL_XOUT_H register
  ax = ((int16_t)SPI.transfer(0x00) << 8) | SPI.transfer(0x00);
  ay = ((int16_t)SPI.transfer(0x00) << 8) | SPI.transfer(0x00);
  az = ((int16_t)SPI.transfer(0x00) << 8) | SPI.transfer(0x00);
  digitalWrite(MPU_CS, HIGH);
}

void writeMPU(uint8_t reg, uint8_t data) {
  // Write a value to a register on the MPU
  digitalWrite(MPU_CS, LOW);
  SPI.transfer(reg);
  SPI.transfer(data);
  digitalWrite(MPU_CS, HIGH);
}