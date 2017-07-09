import serial, os, signals, sys, suggestions
from sklearn.externals import joblib
import pyttsx

engine = pyttsx.init()

def print_sentence_with_pointer(sentence, position):
	print sentence
	print " "*position + "^"

#Sentence used to get samples because it contains all letters.
#ALTERNATIVE: the quick brown fox jumps over the lazy dog
test_sentence = "pack my box with five dozen liquor jugs"

#Mode parameters, controlled using sys.argv by the terminal
TRY_TO_PREDICT = False
SAVE_NEW_SAMPLES = False
FULL_CYCLE = False
ENABLE_WRITE = False
TARGET_ALL_MODE = False
AUTOCORRECT = True
DELETE_ALL_ENABLED = False

#Serial parameters
SERIAL_PORT = "COM6"
BAUD_RATE = 38400
TIMEOUT = 100

#Recording parameters
target_sign = "a"
current_batch = "0"
target_directory = "data"

current_test_index = 0

#Analyzes the arguments to enable a specific mode

arguments = {}

for i in sys.argv[1:]:
	if "=" in i:
		sub_args = i.split("=")
		arguments[sub_args[0]]=sub_args[1]
	else:
		arguments[i]=None

#If there are arguments, analyzes them
if len(sys.argv)>1:
	if arguments.has_key("target"):
		target_sign = arguments["target"].split(":")[0]
		current_batch = arguments["target"].split(":")[1]
		print "TARGET SIGN: '{sign}' USING BATCH: {batch}".format(sign=target_sign, batch = current_batch)
		SAVE_NEW_SAMPLES = True
	if arguments.has_key("predict"):
		TRY_TO_PREDICT = True
	if arguments.has_key("write"):
		TRY_TO_PREDICT = True
		ENABLE_WRITE = True
	if arguments.has_key("test"):
		current_batch = arguments["test"]
		TARGET_ALL_MODE = True
		SAVE_NEW_SAMPLES = True
	if arguments.has_key("noautocorrect"):
		AUTOCORRECT=False
	if arguments.has_key("port"):
		SERIAL_PORT = arguments["port"]

clf = None
classes = None
sentence = ""
hinter = suggestions.Hinter.load_english_dict()

#Loads the machine learning model from file
if TRY_TO_PREDICT:
	print "Loading model..."
	clf = joblib.load('model.pkl')
	classes = joblib.load('classes.pkl')


print "OPENING SERIAL_PORT '{port}' WITH BAUDRATE {baud}...".format(port = SERIAL_PORT, baud = BAUD_RATE)

print "IMPORTANT!"
print "To end the program hold Ctrl+C and send some data over serial"

#Opens the serial port specified by SERIAL_PORT with the specified BAUD_RATE
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout = TIMEOUT)

output = []

in_loop = True
is_recording = False

current_sample = 0

#Resets the output file
output_file = open("output.txt","w")
output_file.write("")
output_file.close()

#If TARGET_ALL_MODE = True, print the sentence with the current position
if TARGET_ALL_MODE:
	print_sentence_with_pointer(test_sentence, 0)

try:
    while in_loop:
    	#Read a line over serial and deletes the line terminators
		line = ser.readline().replace("\r\n","")
		#If it receive "STARTING BATCH" it starts the recording
		if line=="STARTING BATCH":
			#Enable the recording
			is_recording = True
			#Reset the buffer
			output = []
			print "RECORDING...",
		elif line=="CLOSING BATCH": #Stops recording and analyzes the result
			#Disable recording
			is_recording = False
			if len(output)>1: #If less than 1, it means error
				print "DONE, SAVING...",

				#If TARGET_ALL_MODE is enabled changes the target sign
				#according to the position
				if TARGET_ALL_MODE:
					if current_test_index<len(test_sentence):
						target_sign = test_sentence[current_test_index]
					else:
						#At the end of the sentence, it quits
						print "Target All Ended!"
						quit()

				#Generates the filename based on the target sign, batch and progressive number
				filename = "{sign}_sample_{batch}_{number}.txt".format(sign = target_sign, batch = current_batch, number = current_sample)
				#Generates the path
				path = target_directory + os.sep + filename
				
				#If SAVE_NEW_SAMPLES is False, it saves the recording to a temporary file
				if SAVE_NEW_SAMPLES == False:
					path = "tmp.txt"
					filename = "tmp.txt"

				#Saves the recording in a file
				f = open(path, "w")
				f.write('\n'.join(output))
				f.close()
				print "SAVED IN {filename}".format(filename = filename)

				current_sample += 1

				#If TRY_TO_PREDICT is True, it utilizes the model to predict the recording
				if TRY_TO_PREDICT:
					print "PREDICTING..."
					#It loads the recording as a Sample object
					sample_test = signals.Sample.load_from_file(path)

					linearized_sample = sample_test.get_linearized(reshape=True)
					#Predict the number with the machine learning model
					number = clf.predict(linearized_sample)
					#Convert it to a char
					char = chr(ord('a')+number[0])

					#Get the last word in the sentence
					last_word = sentence.split(" ")[-1:][0]

					#If AUTOCORRECT is True, the cross-calculated char will override the predicted one
					if AUTOCORRECT and char.islower():
						predicted_char = hinter.most_probable_letter(clf, classes, linearized_sample, last_word)
						if predicted_char is not None:
							print "CURRENT WORD: {word}, PREDICTED {old}, CROSS_CALCULATED {new}".format(word = last_word, old = char, new = predicted_char)
							char = predicted_char
					
					#If the mode is WRITE, assigns special meanings to some characters
					#and builds a sentence with each char
					if ENABLE_WRITE:
						if char == 'D': #Delete the last character
							sentence = sentence[:-1]
						elif char == 'A': #Delete all characters
							if DELETE_ALL_ENABLED:
								sentence = ""
							else:
								print "DELETE_ALL_ENABLED = FALSE"
						else: #Add the char to the sentence
							sentence += char
						#Prints the last char and the sentence
						print "[{char}] -> {sentence}".format(char = char, sentence = sentence)
						#Saves the output to a file
						output_file = open("output.txt","w")
						output_file.write(sentence)
						output_file.close()
					else:
						print char
						if(char == 'a'):
                                                        engine.say("Hello")
                                                        engine.runAndWait()
                                                elif(char == 'b'):
                                                        engine.say("Welcome")
                                                        engine.runAndWait()
                                                        #pass
                                                elif(char == 'c'):
                                                        engine.say("to our")
                                                        engine.runAndWait()
                                                        #pass
                                                elif(char == 'd'):
                                                        engine.say("College")
                                                        engine.runAndWait()
                                                        #pass
                                                elif(char == 'e'):
                                                        engine.say("Thank You")
                                                        engine.runAndWait()
                                                        #pass
                                                elif(char == 'f'):
                                                        #engine.say()        Uncomment these lines and fill with appropriate word for a gesture
                                                        #engine.runAndWait()
                                                        pass
                                                elif(char == 'g'):
                                                        #engine.say()
                                                        #engine.runAndWait()
                                                        pass
                                                elif(char == 'h'):
                                                        #engine.say()
                                                        #engine.runAndWait()
                                                        pass
                                                elif(char == 'i'):
                                                        #engine.say()
                                                        #engine.runAndWait()
                                                        pass
                                                elif(char == 'j'):
                                                        #engine.say()
                                                        #engine.runAndWait()
                                                        pass
                                                elif(char == 'k'):
                                                        #engine.say()
                                                        #engine.runAndWait()
                                                        pass
                                                elif(char == 'l'):
                                                        #engine.say()
                                                        #engine.runAndWait()
                                                        pass
                                                else:
                                                        #engine.say()
                                                        #engine.runAndWait()
                                                        pass
			else: #In case of a corrupted sequence
				print "ERROR..."
				current_test_index -= 1

			#If TARGET_ALL_MODE=True it shows the current position in the sentence
			if TARGET_ALL_MODE:
				current_test_index += 1
				print_sentence_with_pointer(test_sentence, current_test_index)
		else:
			#Append the current signal line in the recording
			output.append(line)
except KeyboardInterrupt: #When Ctrl+C is pressed, the loop terminates
    print 'CLOSED LOOP!'

#Closes the serial port
ser.close()
