#include <SPI.h>

#define NUM_REGISTERS 128
#define DATA_LENGTH_BYTES 2

volatile uint64_t registers[NUM_REGISTERS] = {0};
volatile uint8_t buffer[10];
volatile uint8_t responseBuffer[10];
volatile uint8_t byteIndex = 0;
volatile bool frameReady = false;

void setup() {
  Serial.begin(115200);
  
  // 기본 에코 응답 설정
  responseBuffer[0] = 0x00;  // 첫 번째 명령 헤더
  responseBuffer[1] = 0x00;  // 첫 번째 데이터
  responseBuffer[2] = 0x00;  // 두 번째 데이터
  
  pinMode(MISO, OUTPUT);
  SPCR |= _BV(SPE);
  SPDR = responseBuffer[0];  // 첫 번째 응답 로드
  SPI.attachInterrupt();
  Serial.println("SPI Slave ready. Data length: 2 bytes");
}

ISR(SPI_STC_vect) {
  uint8_t received = SPDR;
  buffer[byteIndex] = received;
  
  // 다음 바이트 응답 즉시 준비
  byteIndex++;
  
  if (byteIndex < 3) {
    SPDR = responseBuffer[byteIndex];
  } else {
    SPDR = 0x00;
    frameReady = true;
    byteIndex = 0;
  }
}

void loop() {
  if (frameReady) {
    frameReady = false;
    
    uint8_t header = buffer[0];
    uint8_t rw = (header & 0x80) >> 7;
    uint8_t addr = header & 0x7F;
    
    if (addr < NUM_REGISTERS) {
      uint16_t data = (buffer[1] << 8) | buffer[2];
      
      if (rw == 0) {
        registers[addr] = data;
        Serial.print("Write [0x");
        Serial.print(addr, HEX);
        Serial.print("] = 0x");
        Serial.print(data, HEX);
        Serial.println(" (2 bytes)");
        
        responseBuffer[0] = header;
        responseBuffer[1] = buffer[1];
        responseBuffer[2] = buffer[2];
      } else {
        Serial.print("Read [0x");
        Serial.print(addr, HEX);
        Serial.print("] -> 0x");
        Serial.print((uint16_t)registers[addr], HEX);
        Serial.println(" (2 bytes)");
        
        responseBuffer[0] = header;
        responseBuffer[1] = (registers[addr] >> 8) & 0xFF;
        responseBuffer[2] = registers[addr] & 0xFF;
      }
    }
  }
}
