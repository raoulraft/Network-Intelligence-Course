import wandb
import csv
import random
import time

# Define max number of steps inside an episode 
n_max_steps = 100
# Define max number of episodes
n_max_episodes = 100


# Set the number of actions (0 = BPSK, 1 = 8PSK, 2 = 16PSK)
num_actions = 3

# Define the UCB1 exploration parameter
exploration_param = 2.0

# For each action, initialize the action-value estimates to 0 
action_counts = [0] * num_actions
total_rewards = [0] * num_actions


# Define wandb run parameters and start the wandb logging run
run_name = "ucb"
project_name = "DESERT"
wandb.init(name=run_name, project=project_name, tags=["static"], entity="unwis24", reinit=True)


# Function to select an action using UCB1
def select_action():
    for action in range(num_actions):
        if action_counts[action] == 0:
            return action  # Select unexplored action

    # Calculate ucb value for each arm, and return the arm with the max value
    ucb_values = [total_rewards[action] / action_counts[action] + exploration_param * math.sqrt(math.log(sum(action_counts)) / action_counts[action]) for action in range(num_actions)]
    return ucb_values.index(max(ucb_values))

# [...]

# Define the episode counter
n_episode = 0

while(n_episode < n_max_episodes):

    # [...]

    n_step = 1
    cumulative_reward = 0
    # Define the list to later calculate the mean throughput for each episode
    throughput_list = []

    while (n_step < n_max_steps):

        # Select an action based on the UCB1 algorithm
        action = select_action()

        # send action to env (Desert Simulator), even with txt file

        # [...]])

        # Wait for the next reward to be written (by DESERT) to the file before taking the next step
        while True:

            # wait for the env (DESERT) to send the reward back

            # [...]

            time.sleep(0.2)

        # IMPORTANT: both executing the action and receiving the reward are usually
        # done in a single line of code:
        # reward = env.step(action)
        # This means that you would define an env object where internally you would define all the logic
        # to execute the action and calculate the rewarD


        # Log the step reward and step action in wandb
        wandb.log({"reward": reward},commit=False)
        wandb.log({"action": action},commit=False)
        # wandb.log({"state": state}, commit=True)

        # increase UCB1 counters and internal step counters
        action_counts[action] += 1
        total_rewards[action] += reward
        internal_step += 1
        n_step += 1

        # Check that both scripts are correctly going into the next step without missing any step
        # [...]

    # Calculate the mean throughput from the list defined earlier  
    mean_throughput = statistics.mean(throughput_list)

    # Log the mean throughput and cumulative reward (sum of rewards inside the episode) to wandb
    wandb.log({"mean throughput": mean_throughput, "episode": n_episode},commit=False)
    wandb.log({"cumulative reward": cumulative_reward, "episode": n_episode},commit=True)

    # Increase episode counter
    n_episode += 1


