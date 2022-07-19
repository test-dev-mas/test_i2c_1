#include <Wire.h>

void setup() {
    DDRE |= (1 << PE3) | (1 << PE4) | (1 << PE5);
    PORTE |= (1 << PE3) | (1 << PE4) | (1 << PE5);

    DDRG |= (1 << PG5);
    PORTG |= (1 << PG5);

    DDRB |= (1 << PB7);

    Wire.begin();
    Serial.begin(115200);

    for (;;) {
        // Wire.requestFrom(8, 6);

        // while (Wire.available()) {
        //     char u = Wire.read();
        //     Serial.print(u);
        //     PORTB ^= (1 << PB7);
        // }

        // Serial.print('\t');
        
        // delay(1000);
        while (Serial.available()) {
            char u = Serial.read();
            if (u == '2') {
                Wire.requestFrom(8, 2);
                while (Wire.available()) {
                    PORTB ^= (1 << PB7);
                    uint8_t a = Wire.read();
                    uint8_t b = Wire.read();

                    // Serial.println(b|a<<8);

                    Serial.write(a);
                    Serial.write(b);
                    Serial.write('\r');
                }
                break;
            }
            Wire.beginTransmission(8);
            Wire.write(u);
            Wire.endTransmission();
            // PORTB ^= (1 << PB7);
        }
    }
}

void loop() {
}
