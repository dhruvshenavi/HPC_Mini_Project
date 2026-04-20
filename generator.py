import random

sentences = [
    "AI is transforming the world",
    "Machine learning is powerful",
    "Data annotation is important",
    "Parallel processing improves speed",
    "Hello world example",
    "Deep learning uses neural networks",
    "This is a random sentence",
    "AI helps in automation",
    "Python is great for data processing",
    "Natural language processing is interesting"
]

def generate_data(filename="data.txt", lines=500):
    with open(filename, "w") as f:
        for i in range(lines):
            sentence = random.choice(sentences)

            # Add variations
            if i % 5 == 0:
                sentence += " with AI"
            elif i % 7 == 0:
                sentence += " and machine learning"
            elif i % 11 == 0:
                sentence += " in annotation task"

            f.write(sentence + "\n")

    print(f"✅ Generated {lines} lines in {filename}")

if __name__ == "__main__":
    generate_data()