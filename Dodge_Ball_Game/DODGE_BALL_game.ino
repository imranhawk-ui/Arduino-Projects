

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

int player = 7;
int blockX = 3;
int blockY = 0;
int score = 0;

const int LEFT = 2;
const int RIGHT = 3;

unsigned long lastMove = 0;

void setup() {
  lcd.init();
  lcd.backlight();

  pinMode(LEFT, INPUT_PULLUP);
  pinMode(RIGHT, INPUT_PULLUP);

  randomSeed(analogRead(A0));
}

void loop() {
  // Move player
  if (digitalRead(LEFT) == LOW && player > 0) {
    player--;
    delay(120);
  }

  if (digitalRead(RIGHT) == LOW && player < 15) {
    player++;
    delay(120);
  }

  // Move falling block every 400 ms
  if (millis() - lastMove >= 400) {
    lastMove = millis();
    blockY++;

    // Block reaches the player's row
    if (blockY >= 1) {
      if (blockX == player) {
        lcd.clear();
        lcd.setCursor(3, 0);
        lcd.print("Game Over!");
        lcd.setCursor(0, 1);
        lcd.print("Score: ");
        lcd.print(score);

        delay(1500);

        score = 0;
        player = 7;
      } else {
        score++;
      }

      // Start a new falling block
      blockX = random(0, 16);
      blockY = 0;
    }
  }

  // Draw LCD
  lcd.setCursor(0, 0);
  for (int i = 0; i < 16; i++) {
    lcd.print((blockY == 0 && blockX == i) ? '#' : ' ');
  }

  lcd.setCursor(0, 1);
  for (int i = 0; i < 16; i++) {
    lcd.print(player == i ? 'X' : ' ');
  }
}
