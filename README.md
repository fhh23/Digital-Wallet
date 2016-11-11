# Digital Wallet #
Farhan Hormasji

## Run Environment ##
Python 3

## Features ##
Feature 1: Output 'trusted' if the 2 Ids in the transaction only have 1 degree seperation, output 'unverified' otherwise.  
Feature 2: Output 'trusted' if the 2 Ids in the transaction have at most 2 degree seperation (i.e. friend of a friend), output 'unverified' otherwise.  
Feature 3: Output 'trusted' if the 2 Ids in the transaction have at most 4 degree seperation, output 'unverified' otherwise. 
Feature 4: Output 'trusted' if the transaction amount is at most than twice the previous maximum transaction amount between the 2 Ids, output 'unverified' otherwise.   
Feature 5: Output 'trusted' if the transaction date is at most 60 days after the most recent transaction amount between the 2 Ids, output 'unverified' otherwise.  

## Design Decisions ##
1. Once a row of the streaming input file has been processed, the values in the row are added to the existing adjacency list and hash table to be used to evaluate future rows in the streaming input file.
2. If 2 Ids have not had a transaction between each other before, the program should output 'unverified' for all 5 implemented features.
3. Transactions are undirected. So a transaction from Id1 to Id2 is treated the same as a transaction from Id2 to Id1.
4. Dates in only the format year-month-day and month/day/year are allowed. If a date has letters in it, the date will default to 11/2/2016.
5. If Ids have letters in it, the Id will default to 0.
6. If transaction amounts have letters in it, the transaction amount will default to 0. 
7. The output filename must match with the feature number. It must follow the naming convention output<feature#>.txt (e.g., output1.txt corresponds to Feature 1). 
8. However, any amount and combination of features may be tested, and the output files don't need to be passed to run.sh in any order. For example, if only feature 1 and 3 want to be tested, only the path to output1.txt and output3.txt need to be passed to the program in run.sh.
9. The batch and streaming input files must have encoding 'utf8' (just as the input files provided do).
10. The first to files provided as inputs to the program in run.sh must be the batch_payment text file and stream_payment text file in that order. The rest of the files provided should be the output files in any amount and order.

## Program Runtime ##
It took 128 seconds to read the full batch_payment.txt input file provided and create the adjacency list for transactions and hash table for max transaction amount and most recent transaction date.
It took 346 seconds to process the first 1000 lines of the stream_payment.txt provided and output 'trusted/unverified' to the corresponding output files for all 5 implemented features. So on average it took ~2.9 seconds to process all 5 features for one transaction.
