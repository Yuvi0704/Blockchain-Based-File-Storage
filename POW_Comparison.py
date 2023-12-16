from Blockchain import Blockchain
from Block import Block
from timeit import default_timer as timer
import random
import string
import threading
import matplotlib.pyplot as plt

pow_run = []  # to store running time of pow algorithm with various difficulty levels
pow2_run = []  # to store running time of pow2 algorithm with various difficulty levels

# generates random string
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

# this is method to add transactions to the block on the fly to make it more realistic
def add_transaction(block):
    global transactions_length
    global transactions

    for i in range(transactions_length):
        if random.random() > 0.9:
            name = random_char(random.randint(0, 20))
            file_name = random_char(random.randint(0, 20))
            file_data = random_char(random.randint(0, 200))

            t = {
                "user": name,
                "v_file": file_name,
                "file_data": file_data,
                "file_size": random.randint(0, 1000)
            }

            block.add_t(t)

# Lists to store data for plotting
difficulty_levels = list(range(2, 6))
pow_run_times = []
pow2_run_times = []

for j in difficulty_levels:
    block_index = random.randint(0, 2000)
    transactions_length = random.randint(10, 20)
    transactions = []

    # creates a random block
    b = Block(block_index, transactions, "0")
    chain = Blockchain()
    Blockchain.difficulty = j

    # thread to add transactions on the fly
    new_thread = threading.Thread(target=add_transaction, args=(b,))
    new_thread.start()

    # calculating running time for POW algorithm
    start = timer()
    chain.p_o_w(b)
    end = timer()
    pow_run_times.append(end - start)

    # calculating running time for POW2 algorithm
    start = timer()
    chain.p_o_w_2(b)
    end = timer()
    pow2_run_times.append(end - start)

# Create a graph to visualize the running times
plt.plot(difficulty_levels, pow_run_times, label="PoW with Random Nonce")
plt.plot(difficulty_levels, pow2_run_times, label="PoW with Iterative Nonce")
plt.xlabel("Difficulty Level")
plt.ylabel("Running Time (seconds)")
plt.title("Performance Comparison of PoW Algorithms")
plt.legend()
plt.show()

# Print the running times
print("------------Proof of Work with Random Nounce ------------")
for i, time in enumerate(pow_run_times):
    print(f"Difficulty {difficulty_levels[i]}: {time:.5f} seconds")

print("------------Proof of Work with Iterative Nounce ------------")
for i, time in enumerate(pow2_run_times):
    print(f"Difficulty {difficulty_levels[i]}: {time:.5f} seconds")
