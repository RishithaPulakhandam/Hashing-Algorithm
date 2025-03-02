# Hash Table Implementation Programming Project 02

This programming project 02 includes a script for simulating hash table operations with different collision handling strategies: linear probing, quadratic probing, and chaining. It provides a flexible implementation for hash table operations and supports a mid-square hashing option for key insertion.

I have submitted the original input file (`LabHashingInput.txt`), which contains keys for insertion into the hash table. The output file (`LabHashingoutput.txt`) contains the performance analysis and final state of the hash table after all keys have been inserted.Additionally input files of sizes 36 (input-36.txt),84 (input-84.txt), 108 (input-108.txt),127 (input-127.txt) are created to observe the efficiency (no.of comparisons) across various file sizes.The output are written into output-36.txt, output-84.txt, output-108.txt, output-127.txt respectively.

## Features

- Accepts integer keys from a specified input file.
- Supports three collision handling schemes: linear probing, quadratic probing, and chaining.
- Includes a mid-square hash function for key hashing.
- Outputs the results, including runtime analysis, number of collisions, comparisons, and the final state of the hash table.

## Requirements

- Python 3.x

## Usage

1. **Prepare the Input File**: Create an input text file containing integer keys, one key per line.

2. **Run the Script**: Execute the script from the command line. When prompted, enter the paths to the input file and desired output file location.

3. **Review the Output**: Open the output file to review the results, including runtime performance and the final state of the hash table.

## Functions

### `linear_probing(key, hash_value)`
- **Purpose**: Finds an open slot for the key using linear probing in case of a collision. This method iteratively checks the next slot in the table until an empty slot is found.
- **Parameters**:
  - `key`: The key to insert.
  - `hash_value`: The initial hash value generated for the key, usually by another hashing function.
- **Returns**: The hash value for the key.

### `quadratic_probing(key, hash_value)`
- **Purpose**: Resolves collisions using quadratic probing. Unlike linear probing, which checks slots in linear succession, quadratic probing adds a quadratic factor to the probing sequence to reduce clustering in the hash table.
- **Parameters**:
  - `key`: The key to insert.
  - `hash_value`: The initial hash value generated for the key.
- **Returns**: The index of an open slot where the key can be inserted.

### `insert_chaining(key, index)`
- **Purpose**: Inserts a key into the hash table using chaining as a collision resolution strategy. If a collision occurs at the hashed index, the new key is added to a linked list (or chain) at that index.
- **Parameters**:
  - `key`: The key to insert/hash.
  - `index`: The index at which to attempt the insertion, typically determined by a hash function.
- **Returns**: Nothing directly, but the method links the new key into the chain at the specified index if the slot is already occupied.

### `mid_square_hash(key, table_size)`
- **Purpose**: Generates a hash value using the mid-square method.
- **Parameters**:
  - `key`: The key to hash.
  - `table_size`: The size of the hash table.
- **Returns**: The hash value for the key.

 Other functions like `load_factor`, `find_next_free_slot`, and `print_table` serve auxiliary roles in managing the hash table, such as calculating its load factor, finding the next available slot, and displaying the table's current state, rather than directly performing collision resolution.

## Hash Table Class

The `HashTable` class includes methods to perform hash table operations with a specified size, bucket size, collision handling strategy, modulo divisor, and mid-square option.

## Execution

The `insert` function of the script initiates the hash table creation and insertion process. The code prompts the user for input and output file locations and runs the simulation for the configured hash table scenarios.The `print_table` prints the table according to specified configurations into the output file.

## Note

The hash table simulation provides a comprehensive analysis of different hashing and collision resolution strategies. The output files contain statistics such as the Total collisions,Primary Collisions, Secondary Collisions, Total comparison, No.of keys not inserted to understand the performance and behavior of hash tables under various collision conditions.If a key is not inserted as the table is full an appropriate message is included as an error message on the terminal.

## Author
Rishitha Pulakhandam <br>
rpulakh1@jh.edu
