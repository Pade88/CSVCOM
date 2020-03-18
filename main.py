#@Author: OPA
#@Date: 18.03.2020 2:00 AM GMT+2
#@Version 1.0.0.1
#@pack and unpack methods updated for binary representation in CSV file

import csv
import time

tx_chanID = 0
rx_chanID = 0
ack = True
comOk = False

class ARINC429:
	def __init__(self):
		if self:
			global comOk
			print("ARINC429 activated!")
			ARINC429.setup()
			if(ARINC429.checkComm()):
				print("Receiver and Transmitter have the same ID, communication established!")
				comOk = True
			else:
				print("Fail to establish communication beetween Receiver and Transmitter (BAD ID)")

			while True:
				lv_transmitted_value = int(input("Insert value that should be transmitted: "))
				Tx.transmit(lv_transmitted_value)
				print("Value received: " + str(Rx.receive()))
				time.sleep(0.5)

	# BinaryCodedDecimal to be implemented
	#@Param: pv_value
	#@Return: a binary sequence after conversion from decimal of pv_value
	def BCD(pv_value):
		if not pv_value:
			print("Unvalid value inserted!")

		## To be updated!
		return bin(pv_value)

	#@Void param, this function takes channel ID from user input and initialize RX and TX
	def setup():
		lv_tx_id = int(input("Insert Transmitter ID!: "))
		lv_rx_id = int(input("Insert Receiver ID!: "))
		Tx.__init__(lv_tx_id)
		Rx.__init__(lv_rx_id)


	#@Void param, check if receiver and transmitter have the same channel ID.
	def checkComm():
		return True if (tx_chanID == rx_chanID) else False



class Tx(ARINC429):
	#Param: pv_chanID takes channel ID and check if it's a non 0 value.
	#Out: global tx_chanID copy of pv_chanID used in checkCom()
	def __init__(pv_chanID):
		global tx_chanID
		if pv_chanID:
			print("Transmitter configured! Establishing communication!")
			tx_chanID = pv_chanID

	#Param: pv_value int, function parse through param and fill lv_pack list with pv_value digits.
	#		insert(0, XXXX) is used to keep number consistency (otherwise, lv_pack will be populated with inverse order of pv_value digits)
	def unpack_word(pv_value):
		lv_binary = int(bin(pv_value)[2:])
    		unpacked = []
    		while lv_binary:
        		unpacked.insert(0, lv_binary%10)
        		lv_binary = lv_binary / 10
    
   		return unpacked

	#Param: pv_value - integer that should be transmitted, comOk, ack - internal flags.
	# Function check if communication is established through <<comOK>> and if RX received last message through <<ack>>.
	# Function opens 'bits_buffer.csv' file in write mode, and transmits input digits. (Delay is 0.1 sec, To be evaluated) 
	def transmit(pv_value):
		global comOk
		global ack
		#pv_value = Tx.pack_word(pv_value)

		if comOk and ack:
			with open('bits_buffer.csv', mode = 'w') as transmission:
				buffer_writer = csv.writer(transmission, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				buffer_writer.writerow(Tx.pack_word(pv_value))
				time.sleep(0.1)


class Rx(ARINC429):
	#Param: pv_chanID takes channel ID and check if it's a non 0 value.
	#Out: global rx_chanID copy of pv_chanID used in checkCom()
	def __init__(pv_chanID):
		global rx_chanID
		if pv_chanID:
			print("Receiver configured! Establishing communication!")
			rx_chanID = pv_chanID

	def unpack(pv_list):
    		lv_packed = 0
    		lv_pow = 0
    		lv_decimal = 0
    		for index in reversed(pv_list):
        		lv_packed = lv_packed * 10 + index
        		lv_decimal = lv_decimal + 2**lv_pow * index
        		lv_pow = lv_pow + 1
     
    		return lv_decimal


    #Param: comOk, ack - global flags for internal use.
    # Function checks if communication is established and open file written by TX.
    # ack is set to false while function parse.
    # lv_buffer_reader parse through CSV file and return every bit to main function.
    # If read status is OK, ack becomes True and a new bit-read procces begins.
	def receive():
		global comOk
		global ack
		ack = False
		if comOk:
			with open('bits_buffer.csv') as transmission:
				lv_buffer_reader = csv.reader(transmission, delimiter=',')
				for bit in lv_buffer_reader:
					ack = True
					time.sleep(0.1)
					return bit



if __name__== "__main__":
	ARINC429.__init__(1)
	
