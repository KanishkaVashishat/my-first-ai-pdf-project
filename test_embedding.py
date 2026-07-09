from embedding import create_embedding

text = "Artificial Intelligence is changing the world."

embedding = create_embedding(text)

print(type(embedding))
print(len(embedding))
print(embedding[:10])