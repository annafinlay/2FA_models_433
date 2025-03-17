import itertools
import time
import random

def generate_random_otp(length=6):
    """Generates a random OTP of the given length."""
    return "".join(str(random.randint(0, 9)) for _ in range(length))

def brute_force_otp(correct_otp, max_attempts=1000000):
    """Attempts to brute-force a 6-digit OTP."""
    start_time = time.time()  # Start timer
    
    for attempt, otp in enumerate(itertools.product("0123456789", repeat=len(correct_otp))):  
        guess = "".join(otp)
        
        # Simulate a delay to mimic real attack attempts
        if attempt % 10000 == 0:
            print(f"Trying OTP: {guess}")  # Show progress every 10,000 attempts
        
        if guess == correct_otp:
            end_time = time.time()  
            print(f"\nOTP cracked: {guess} in {attempt + 1} attempts")
            print(f"Time taken: {end_time - start_time:.2f} seconds")
            return True

        # Stop if max attempts reached
        if attempt >= max_attempts:
            break

    print("\nBrute force failed. Max attempts reached.")
    return False

# Example use case with randomized OTP
if __name__ == "__main__":
    real_otp = generate_random_otp()  
    print(f"Random OTP (hidden from attacker): {real_otp}")  # FOR TESTING ONLY
    brute_force_otp(real_otp)
