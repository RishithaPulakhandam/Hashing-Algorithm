"""The program is designed to simulate different hashing strategies for storing
and managing keys in a hash table. It evaluates the efficiency and behavior of linear probing,
quadratic probing, and chaining as collision resolution strategies. Additionally, the program
experiments with various hash functions, including simple modulo division and the mid-square
method, to understand their impact on collision occurrence and distribution of keys within the
hash table. The program reads keys from an input file, inserts them into the hash table
according to the specified configuration, and outputs detailed performance metrics and the
final state of the hash table to an output file.These metrics include runtime, number of
collisions, comparisons, items not inserted, and the load factor, providing valuable
insights for analyzing the effectiveness of each hashing strategy."""
import time

def mid_square_hash(key, table_size):
    """
        Calculates the hash value using the mid-square method.
        It squares the key, extracts the middle digits, and mods by the table size.
        """
    squared = key ** 2
    # Extract the middle portion of the squared number as the hash value
    length = len(str(table_size))
    squared_str = str(squared).zfill(length * 2)  # Ensure there's enough digits
    mid_start = len(squared_str) // 2 - length // 2
    mid_end = mid_start + length
    hash_value = int(squared_str[mid_start:mid_end]) % table_size
    return hash_value

class Node:
    """
        Node class for chaining in the hash table.
        Each node holds a key and a reference to the next node.
        """
    def __init__(self, key, next_index=None):
        self.key = key
        self.next_index = next_index  # Pointer to the next node's index in the chain

# Hash Table class definition
class HashTable:
    """
       Hash table implementation supporting different collision strategies
       and hash functions (modulo division and mid-square method).
       """
    def __init__(self, size, bucket_size, collision_strategy, modulo_divisor=None, use_mid_square=False):
        self.size = size
        self.bucket_size = bucket_size
        self.table = [None] * size
        self.collision_strategy = collision_strategy
        self.collisions = 0
        self.primary_collisions = 0
        self.secondary_collisions = 0
        self.comparisons = 0
        self.items_not_inserted = 0
        self.modulo_divisor = modulo_divisor if modulo_divisor else size
        self.use_mid_square = use_mid_square

    def hash(self, key):
        """Computes the hash value of a given key based on the selected hash function."""
        if self.use_mid_square:
            return mid_square_hash(key, self.size)
        else:
            # Ensure the hash value is within the bounds of the hash table size.
            return (key % self.modulo_divisor) % self.size

    # Linear Probing
    def linear_probing(self, key, hash_value):
        initial = True
        for i in range(self.size):
            index = (hash_value + i) % self.size
            self.comparisons += 1
            if not self.table[index] or len(self.table[index]) < self.bucket_size:
                if initial:
                    initial = False
                return index
            if initial:
                self.primary_collisions += 1  # Increment primary collisions on the first collision
                initial = False
            else:
                self.secondary_collisions += 1
            self.collisions += 1
        return None

    # Quadratic Probing
    def quadratic_probing(self, key, hash_value):
        #different constant values to see effect on total comaparisions and efficiency of inserting keys to hash table
        #c1,c2 =0.5,0.5
        #c1,c2 = 1,1
        #c1, c2 = 1, 3
        #c1, c2 = 0, 1
        initial = True
        for i in range(self.size):
            #index = (hash_value + int(c1 * i + c2 * i ** 2)) % self.size
            index = (hash_value + int(i ** 2)) % self.size
            self.comparisons += 1
            if not self.table[index] or len(self.table[index]) < self.bucket_size:
                if initial:
                    initial = False
                return index
            if initial:
                self.primary_collisions += 1
                initial = False
            else:
                self.secondary_collisions += 1
            self.collisions += 1
        return None

    def insert(self, key):
        """Inserts a key into the hash table using the specified collision strategy. """
        hash_value = self.hash(key)
        if self.collision_strategy == 'chaining':
            # Directly call insert_chaining without expecting an index in return
            self.insert_chaining(key, hash_value)
            # Since chaining should always be able to insert, there's no need to check for failure here
        else:
            # For linear and quadratic probing
            index = None
            if self.collision_strategy == 'linear':
                index = self.linear_probing(key, hash_value)
            elif self.collision_strategy == 'quadratic':
                index = self.quadratic_probing(key, hash_value)

            if index is not None:
                if self.table[index] is None:
                    self.table[index] = [key]  # Initialize a new bucket if needed
                else:
                    self.table[index].append(key)  # Append to the existing bucket
            else:
                # For probing methods, increment items_not_inserted if no suitable index was found
                self.items_not_inserted += 1
                print(f"Unable to insert key {key}: The table is full.")

    def insert_chaining(self, key, index):
        """ Handles insertion with chaining. Adds a new node at the index if empty, or
        chains the node if the index is occupied. """
        node = Node(key)
        if not self.table[index]:
            self.table[index] = node
        else:
            self.collisions += 1
            self.primary_collisions += 1
            current_node = self.table[index]
            # Traverse the chain to find the end
            while current_node.next_index is not None:
                self.comparisons += 1
                current_node = self.table[current_node.next_index]
                self.collisions += 1
                self.secondary_collisions += 1


            next_free_index = self.find_next_free_slot(0)
            if next_free_index is not None:
                current_node.next_index = next_free_index
                self.table[next_free_index] = node
            else:
                # Handle the full table situation
                self.items_not_inserted += 1
                print(f"Unable to insert key {key}: The table is full.")
        self.comparisons += 1
        return

    def find_next_free_slot(self, starting_index):
        for i in range(self.size - 1, starting_index - 1, -1):
            if not self.table[i]:
                return i
        return None

    def load_factor(self):
        total_items = 0
        for index, bucket in enumerate(self.table):
            if bucket is None:
                continue
            if self.collision_strategy == 'chaining':
                current_index = index
                while current_index is not None:
                    total_items += 1
                    current_node = self.table[current_index]
                    current_index = current_node.next_index
            else:
                # For linear or quadratic probing, each bucket has at most one item
                total_items += len(bucket)
        return total_items / self.size

    def print_table(self):
        result = []

        # Adjust for cases with a bucket size of 3 (schemes 10 and 11)
        if self.bucket_size == 3:
            # Process each index as its own bucket for these scheme
            for i in range(self.size):
                bucket_contents = []
                if self.table[i] is not None:
                    if isinstance(self.table[i], Node):
                        bucket_contents.append(f"[{self.table[i].key}]")
                    else:
                        bucket_contents += [f"[{item}]" for item in self.table[i]]
                # Ensure the bucket contents list has exactly 3 slots filled
                while len(bucket_contents) < 3:
                    bucket_contents.append("[     ]")


                result.append('   '.join(bucket_contents))
        else:
            # Handling for all other schemes remains unchanged
            for i in range(0, self.size, 5):
                row = []
                for j in range(5):
                    index = i + j
                    if index < self.size:
                        if self.table[index] is not None:
                            if isinstance(self.table[index], Node):
                                content = f"{self.table[index].key}"
                                if self.table[index].next_index is not None:
                                    content += f", {self.table[index].next_index}"
                                row.append(f"[{content}]")
                            else:
                                content = str(self.table[index]).strip('[]')
                                row.append(f"[{content}]")
                        else:
                            row.append("[     ]")  # Uniform empty bracket for other scheme
                    else:
                        row.append("[     ]")  # Ensure consistency in representing empty slots
                result.append('  '.join(row))

        return '\n'.join(result)


def main():
    input_filepath = input("Enter the input file location: ")
    output_filepath = input("Enter the output file location: ")

    keys = []  # Initialize an empty list for storing keys

    with open(input_filepath, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            try:
                # Attempt to convert each line to an integer
                num = int(stripped_line)
                keys.append(num)  # Add the integer to the list of keys
            except ValueError:
                continue

    # Configurations based on the hashing schemes provided
    configurations = [
        (120, 1, 'linear', 120),
        (120, 1, 'quadratic', 120),
        (120, 1, 'chaining', 120),
        (120, 1, 'linear', 127),
        (120, 1, 'quadratic', 127),
        (120, 1, 'chaining', 127),
        (120, 1, 'linear', 113),
        (120, 1, 'quadratic', 113),
        (120, 1, 'chaining', 113),
        (40, 3, 'linear', 41),
        (40, 3, 'quadratic', 41),
        (120, 1, 'linear', None, True),
        (120, 1, 'quadratic', None, True),
        (120, 1, 'chaining', None, True),
    ]

    # Open the output file once and write all configurations output
    with open(output_filepath, 'w') as file:
        for config in configurations:
            if len(config) == 5:
                size, bucket_size, strategy, _, use_mid_square = config
                hash_table = HashTable(size, bucket_size, strategy, use_mid_square=use_mid_square)
            else:
                size, bucket_size, strategy, modulo_divisor = config
                hash_table = HashTable(size, bucket_size, strategy, modulo_divisor=modulo_divisor)

            # Insert keys into the hash table and measure runtime
            start_time = time.time()
            for key in keys:
                hash_table.insert(key)
            end_time = time.time()

            runtime = (end_time - start_time) * 1000  # Convert to milliseconds

            if hash_table.use_mid_square:
                hashing_description = "with division modulo-None"
            else:
                hashing_description = f"with division modulo-{hash_table.modulo_divisor}"

            # Generate and write the output for each configuration
            output = f"Runtime for {hash_table.collision_strategy} {hashing_description} and bucket size {hash_table.bucket_size}: {runtime:.7f}ms\n"
            output += "=========================\n"
            output += f"Hash table size: {hash_table.size}\n"
            output += f"Bucket Size: {hash_table.bucket_size}\n"
            output += f"Number of collisions: {hash_table.collisions}\n"
            output += f"Number of Primary collisions: {hash_table.primary_collisions}\n"
            output += f"Number of Secondary collisions: {hash_table.secondary_collisions}\n"
            output += f"Number of comparisons: {hash_table.comparisons}\n"
            output += f"Number of keys not inserted: {hash_table.items_not_inserted}\n"
            output += f"Load factor: {hash_table.load_factor():.2f}\n\n"
            output += "Resulting hash table:\n"
            output += hash_table.print_table() + "\n\n"

            file.write(output)


if __name__ == "__main__":
    main()





