import time
import csv
from multiprocessing import Pool

# -----------------------------------
# Sentiment Word Lists
# -----------------------------------
positive_words = ["good", "excellent", "love", "amazing", "best"]
negative_words = ["bad", "terrible", "hate", "worst"]


# -----------------------------------
# Sentiment Analysis Function
# -----------------------------------
def analyze_review(review):
    score = 0
    words = review.lower().split()

    for word in words:
        if word in positive_words:
            score += 1
        elif word in negative_words:
            score -= 1

    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return (review.strip(), score, label)


# -----------------------------------
# Process One File
# -----------------------------------
def process_file(filename):
    results = []
    with open(filename, "r") as file:
        for line in file:
            results.append(analyze_review(line))
    return results


# -----------------------------------
# Single Processing
# -----------------------------------
def single_processing(files):
    all_results = []
    for file in files:
        all_results.extend(process_file(file))
    return all_results


# -----------------------------------
# Multiprocessing
# -----------------------------------
def multi_processing(files):
    with Pool(processes=4) as pool:
        results = pool.map(process_file, files)

    # Flatten nested list
    final_results = [item for sublist in results for item in sublist]
    return final_results


# -----------------------------------
# Main Execution
# -----------------------------------
if __name__ == "__main__":

    files = ["text1.txt", "text2.txt", "text3.txt", "text4.txt"]

    # -------- Single Processing --------
    start_single = time.time()
    single_results = single_processing(files)
    end_single = time.time()
    single_time = end_single - start_single

    # -------- Multiprocessing --------
    start_multi = time.time()
    multi_results = multi_processing(files)
    end_multi = time.time()
    multi_time = end_multi - start_multi

    # -------- Save to CSV --------
    with open("output.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Review", "Score", "Sentiment"])
        writer.writerows(multi_results)

    print("Single Processing Time:", single_time, "seconds")
    print("Multiprocessing Time:", multi_time, "seconds")
    print("Results saved to output.csv")