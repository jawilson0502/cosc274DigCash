Project 3 Electronic Cash 
Jessica Wilson, Alex Prindle, Corey Jagodzinski
Eastern Michigan University
COSC 274 Intro to Applied Cryptography
December 7th, 2017

----------------------------------
Table of Contents
----------------------------------
	1. About
	2. Project Contents
	3. Using the Program

----------------------------------
1. About
----------------------------------
Objectives: To implement a protocol for the use of electronic cash using various protocols for maintaining secrecy, anonymity, authenticity, integrity, and mutual trust.

Description: This project implements an electronic cash system, in which the digital cash cannot be copied or used more than once and the privacy of the customer's identity is guaranteed.

The system allows money transaction between two parties: the customer (Alice) and the bank (Bob). The electronic cash used during these transactions is a file that contains:
	1. The amount of the transaction involved
	2. A uniqueness string number
	3. Customer ID which uniquely identifies the customer
	4. Bank's signature (before the customer can use the ecash)

The customer (Alice) generates three money orders (MO). A different random uniqueness string number is applied to each MO. Secret splitting and bit commitment protocols are implemented on the identity strings that describes the customer and a blind signature protocol is implemented for all three money orders.

The bank (Bob) randomly choose one out of three money orders sent by the customer (Alice) to remain unopened. Finally, an algorithm certifies that the two money orders have been filled with valid information.

----------------------------------
2. Project Contents
----------------------------------
The files inlcuded in this project are:

	1. README.md
	2. requirements.txt
	3. bank.py
	4. customer.py
	5. transaction.py

----------------------------------
3. Using the Program
----------------------------------
For this program, we assume you have python3 and pip3 installed.

To create the necessary virtual environment:

* `git clone https://github.com/jawilson0502/cosc274DigCash`
* `cd cosc274DigCach`
* `pip3 install virtualenv`
* `virtualenv venv`
* `source venv/bin/activate`
* `pip install -r requirements.txt`

To customize the inputs for the digital cash, edit `transaction.py` and replace the
necessary variables at the beginning

To run the program, assuming the user is in the virtual environment:

* `python transaction.py`

After running the program, there will be 3 blinded money order files created 
(blind\_mo\*.txt), 2 unblinded money order files (unblinded\_mo\*.txt), 1 signed
blinded money order file (signed\_mo\*.txt), and 1 signed unblinded money order file
(unblindsigned\_mo\*.txt)

