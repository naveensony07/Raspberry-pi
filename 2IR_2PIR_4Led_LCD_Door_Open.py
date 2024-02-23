import time
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


'''
define pin for lcd
'''
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
delay = 1
led1=12
led2=13
led3=16
led4=17

GPIO.setup(led1, GPIO.OUT)  
GPIO.setup(led2, GPIO.OUT)  
GPIO.setup(led3,GPIO.OUT)
GPIO.setup(led4,GPIO.OUT)

# Define GPIO to LCD mapping
LCD_RS = 23
LCD_E  = 22
LCD_D4 = 21
LCD_D5 = 20
LCD_D6 = 19
LCD_D7 = 18
IR_Sensor=6
IR_Sensor2=7
Pir1 =4
Pir2=5
GPIO.setup(LCD_E,GPIO.OUT)  # E
GPIO.setup(LCD_RS,GPIO.OUT) # RS
GPIO.setup(LCD_D4,GPIO.OUT) # DB4
GPIO.setup(LCD_D5,GPIO.OUT) # DB5
GPIO.setup(LCD_D6,GPIO.OUT) # DB6
GPIO.setup(LCD_D7,GPIO.OUT) # DB7
GPIO.setup(IR_Sensor, GPIO.IN) # DB7
GPIO.setup(IR_Sensor2,GPIO.IN)
GPIO.setup(Pir1,GPIO.IN)
GPIO.setup(Pir2,GPIO.IN)
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

'''
Function Name :lcd_init()
Function Description : this function is used to initialized lcd by sending the different commands
'''
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
'''
Function Name :lcd_byte(bits ,mode)
Fuction Name :the main purpose of this function to convert the byte data into bit and send to lcd port
'''
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
'''
Function Name : lcd_toggle_enable()
Function Description:basically this is used to toggle Enable pin
'''
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
'''
Function Name :lcd_string(message,line)
Function  Description :print the data on lcd 
'''
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

lcd_init()
lcd_string("welcome ",LCD_LINE_1)
time.sleep(0.03);
# Define delay between readings
delay = 5
count = 0
while True:
 if GPIO.input(Pir2) and GPIO.input(Pir1) and GPIO.input(IR_Sensor) and GPIO.input(IR_Sensor2):
      lcd_string("Door open",LCD_LINE_1)
      lcd_string("Welcome" ,LCD_LINE_2)
      GPIO.output(led2,GPIO.HIGH)
      GPIO.output(led1,GPIO.HIGH)
      GPIO.output(led3,GPIO.HIGH)
      GPIO.output(led4,GPIO.HIGH)
 else:
 
   if GPIO.input(IR_Sensor):
      lcd_string("Detected IR1   ",LCD_LINE_1)
      GPIO.output(led2,GPIO.HIGH)
   else:
      lcd_string("NO IR1 ",LCD_LINE_1)
      GPIO.output(led2,GPIO.LOW)
      
      
   if GPIO.input(IR_Sensor2):
      lcd_string("Detected IR2",LCD_LINE_2)
      GPIO.output(led1,GPIO.HIGH)    
   else:
      lcd_string("No IR2  ",LCD_LINE_2)
      GPIO.output(led1,GPIO.LOW)
   
   if GPIO.input(Pir1):
      lcd_string("Detected PIR1   ",LCD_LINE_1)
      GPIO.output(led3,GPIO.HIGH)
      
   else:
      lcd_string("NO PIR1 ",LCD_LINE_1)
      GPIO.output(led3,GPIO.LOW)
      
      
   if GPIO.input(Pir2):
      lcd_string("Detected PIR2",LCD_LINE_2)
      GPIO.output(led4,GPIO.HIGH)    
   else:
      lcd_string("NO PIR2  ",LCD_LINE_2)
      GPIO.output(led4,GPIO.LOW)