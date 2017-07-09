# Hand-gesture-to-speech
Hello i'm working on a project to convert hand gestures to speech. It is mainly focused to help mute people to communicate with people who does'nt know sign languuage.
This was a team project which I completed as my Final Year project with Ishan Goel, Aash Mohd, Saurav Pratap Singh.

  Items Required:

  Arduino Uno

  Python IDE(Anaconda, Spyder, Python(x,y))
  
  MPU9150 or MPU 6050(You could use any motion sensor just retrieve the raw accl,gyro,mag value and send to python script)

  1-Push Button

  Flex Sensors(You can also use velostat for making your own flex sensor.)

  Resistors
  
  Arduino USB cable type A/B

  Steps:
  
  1. Make connections between Arduino and MPU9150(SDA-A4 , SCL-A5 , Vcc-3.3V , GND-Ground , INT-Digital Pin 2)

  2. Install Python and the required libraries.

  3. Now burn the Arduino code in Arduino.

                              STARTING BATCH
                              START -296 280 17140 -501 225 -1154 END
                              START 724 152 16228 -396 298 -176 END
                              START 372 16 16740 -346 219 -180 END
                              ...
                              START 1096 1200 16644 -206 288 -2445 END
                              START 1632 1060 16104 -290 95 -3108 END
                              CLOSING BATCH

Open the Serial monitor and the press the button the output looks like the above format.
 4.Now fpr Python part there are two steps:
 
  
  Training : This Involves teaching the algorithm what kind of data it data it should expect. As of now each gesture is associated with   a character ( case sensitive ). This means that you can teach the algorithm a maximum of about 60 different gestures.
  
  Enter the following command in cmd to execute the python script. [port=your arduino com port, target= (gesture):(batch)]
                            
                            python start.py target=a:0 port=COM6
  
  Train the model: trainign the model lets you save gestures and be able to use them later.
                            
                            python learn.py
    
  Testing : Command for predictng a gesture and speech output
  
                            python start.py port=<YOUR_SERIAL_PORT> predict
  
