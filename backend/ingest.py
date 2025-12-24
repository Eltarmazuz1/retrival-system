import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file")
    exit(1)

if not PINECONE_API_KEY:
    print("Error: PINECONE_API_KEY not found in .env file")
    exit(1)

# Initialize OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "rag-gadgets"

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def setup_index():
    # Check if index exists
    existing_indexes = [index.name for index in pc.list_indexes()]
    
    if INDEX_NAME not in existing_indexes:
        print(f"Creating index '{INDEX_NAME}'...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536, # OpenAI text-embedding-3-small dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Wait for index to be ready
        while not pc.describe_index(INDEX_NAME).status['ready']:
            time.sleep(1)
        print("Index created and ready.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

def ingest_data():
    setup_index()
    index = pc.Index(INDEX_NAME)

    # Read Dataset
    try:
        with open("paragraphs.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: paragraphs.txt not found")
        return

    print(f"Found {len(lines)} lines. Starting ingestion...")

    # Limit to first 200 lines to keep it "Very Small" and cheap
    count = 0
    batch_size = 50
    vectors_to_upsert = []

    for idx, line in enumerate(lines):
        text = line.strip()
        if not text:
            continue
            
        if count >= 200:
            break

        print(f"Processing item {count+1}/200...")
        
        try:
            embedding = get_embedding(text, model="text-embedding-3-small")
            
            # Pinecone expects (id, values, metadata)
            vector = (
                str(count),
                embedding,
                {
                    "text": text,
                    "source": "paragraphs.txt",
                    "line_number": idx + 1
                }
            )
            vectors_to_upsert.append(vector)
            
            # Upsert in batches
            if len(vectors_to_upsert) >= batch_size:
                index.upsert(vectors=vectors_to_upsert)
                print(f"Upserted batch of {len(vectors_to_upsert)} vectors.")
                vectors_to_upsert = []

            count += 1
        except Exception as e:
            print(f"Error embedding line {idx}: {e}")

    # Upsert remaining
    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert)
        print(f"Upserted final batch of {len(vectors_to_upsert)} vectors.")

    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()
