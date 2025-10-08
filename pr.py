from transformers import pipeline

# Load the zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Sample input
text = "Can you show me your brochure?"
labels = ["hi", "price", "brochure", "image"]

# Get prediction
result = classifier(text, labels)

print("Predicted intent:", result["labels"][0])
print("Full result:", result)
