# Digital Wallet #
Team: Farhan Hormasji

## Runtime Environment ##
Python 3

## Features ##
Feature 1: Output 'trusted' if the 2 Ids in the transaction only have 1 degree seperation, output 'unverified' otherwise.  
Feature 2: Output 'trusted' if the 2 Ids in the transaction have at most 2 degree seperation (i.e. friend of a friend), output 'unverified' otherwise.  
Feature 3: Output 'trusted' if the 2 Ids in the transaction have at most 4 degree seperation, output 'unverified' otherwise. 
Feature 4: Output 'trusted' if the transaction amount is at most than twice the previous maximum transaction amount between the 2 Ids, output 'unverified' otherwise.   
Feature 5: Output 'trusted' if the transaction date is at most 60 days after the most recent transaction amount between the 2 Ids, output 'unverified' otherwise.  

## Implementation Decisions ##
1. Features 1,2,3 all have to do with finding the degrees of seperation between the 2 Ids involved in a transaction. To find this, the adjacency list data structure was used. The adjacency list was built from batch_payment.txt using a python dictionary. To find the number of degrees seperation between two Ids in the adjacency list, the Breadth First Search (BFS) algorithm was used because it ensures that the shortest path between two Ids will be found. BFS was implemented with the deque data structure for its O(1) time complexity for adding and removing from the deque. Because it was known that the max allowable degrees of seperation allowed was 4 (Feature 3), the BFS algorithm exits if no path of length <= 4 from Id1 to Id2 is found. This was done so that the BFS algorithm only had to be run once for each row in the stream_payment.txt file instead of three times per row (once for Feature 1,2,3). In an actual product, only one of Feature 1,2,3 would probably be used, and so the #degrees of seperation to check for would be passed as a variable to the BFS function instead.
2. Features 4 and 5 have to do with maintaining the max amount and date value for each Id involved in a transaction. To do this, the hash table data structure was used. The hash table was built from batch_payment.txt using a python dictionary. Both the max transaction amount and most recent transaction date were stored in the same hash table.
3. Several implementation decisions were made to make the code robust. 
  1. No file paths are hard-coded. This allows the code to deviate from the given directory structure, as long as the correct paths are passed to run.sh. 
  2. The number of input arguments to run.sh is not hard-coded. This allows the output files to be passed to run.sh in any order, and for any combination of features to be tested. The only requirements for the output file names and order are listed in the "Assumptions" section. 
  3. Check are done for all field names in the case of faulty data in the batch or stream files. Only the date field has a requirement for how the datetime must be formatted, and it is listed in the "Assumptions" section. 


## Assumptions ##
1. Once a row of the streaming input file has been processed, the values in the row are added to the existing adjacency list and hash table to be used to evaluate future rows in the streaming input file.
2. If 2 Ids have not had a transaction between each other before, the program should output 'unverified' for all 5 implemented features.
3. Transactions are undirected. So a transaction from Id1 to Id2 is treated the same as a transaction from Id2 to Id1.
4. Dates in only the format year-month-day and month/day/year are allowed. If a date has letters in it, the date will default to 11/2/2016.
5. If Ids have letters in it, the Id will default to 0.
6. If transaction amounts have letters in it, the transaction amount will default to 0. 
7. The output filename must match with the feature number. It must follow the naming convention output[feature#].txt (e.g., output1.txt corresponds to Feature 1). 
8. However, any amount and combination of features may be tested, and the output files don't need to be passed to run.sh in any order. For example, if only feature 1 and 3 want to be tested, only the path to output1.txt and output3.txt need to be passed to the program in run.sh.
9. The batch and streaming input files must have encoding 'utf8' (just as the input files provided do).
10. The first to files provided as inputs to the program in run.sh must be the batch_payment text file and stream_payment text file in that order. The rest of the files provided should be the output files in any amount and order.

## Test Suite ##
1. test-1-paymo-trans: simple test provided
2. Id2NotInBatch-test: validates that a transaction between 2 Ids, where at least one Id hasn't been involved in any prior transaction, is handled properly.   
3. Feature1-simple-test: validates that a transaction between 2 Ids, where neither Id has had a transaction with the other before, is handled properly.   
4. Feature2-simple-test: validates that a transaction between 2 Ids, where there is more than 2 degrees seperation between the 2 Ids, is handled properly.   
5. Feature3-simple-test: validates that a transaction between 2 Ids, where there is more than 4 degrees seperation between the 2 Ids, is handled properly.   
6. Feature4-simple-test: validates that a transaction between 2 Ids, where the transaction amount is more than twice the previous max transaction amount, is handled properly.  
7. Feature5-simple-test: validates that a transaction between 2 Ids, where the transaction date is more than 60 days after the most recent transaction date, is handled properly.  
8. 1000line-stream_payment-test (not included): Use the entire batch_payment.txt file provided and first 1000 lines of the stream_payment.txt file provided to time the program's functions. This test wasn't included in the repository because of the size of the batch_payment.txt file.  

## Program Runtime ##
It took 128 seconds to read the full batch_payment.txt input file provided and create the adjacency list for transactions and hash table for max transaction amount and most recent transaction date.
It took 346 seconds to process the first 1000 lines of the stream_payment.txt provided and output 'trusted/unverified' to the corresponding output files for all 5 implemented features. So on average it took ~2.9 seconds to process all 5 features for one transaction.
