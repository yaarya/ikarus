import os
from fastapi import FastAPI
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# --- 1. Load Environment Variables and Initialize Clients ---
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- 2. Load Models and Connect to Pinecone Index ---
print("Loading sentence transformer model...")
text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
print("Model loaded.")

print("Connecting to Pinecone indexes...")
text_index = pc.Index("furniture-text-search")
image_index = pc.Index("furniture-image-search")
print("Connection successful.")

# --- 3. Initialize FastAPI App ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Define Pydantic Models ---
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class Product(BaseModel):
    id: str
    title: str
    brand: str
    price: str
    image_url: str
    creative_description: str

# --- 5. Helper Function for GenAI ---
def generate_creative_description(title: str, brand: str) -> str:
    prompt = f"Generate a short, creative, and appealing product description for a piece of furniture. Make it sound enticing. Do not include the product name or brand in your response. Product Name: {title}, Brand: {brand}."
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating description with Gemini: {e}")
        return "Discover a piece that perfectly complements your living space."

# --- 6. API Endpoints ---
@app.post("/recommend", response_model=list[Product])
def recommend_products(request: QueryRequest):
    print(f"Received query: {request.query}")
    query_embedding = text_model.encode(request.query).tolist()
    
    query_results = text_index.query(vector=query_embedding, top_k=request.top_k, include_metadata=True)
    
    response_products = []
    # CORRECTED: Use modern dot notation for the new Pinecone library
    for match in query_results.matches:
        metadata = match.metadata
        creative_desc = generate_creative_description(title=metadata.get("title", ""), brand=metadata.get("brand", ""))
        product = Product(
            id=match.id,
            title=metadata.get("title", ""),
            brand=metadata.get("brand", ""),
            price=metadata.get("price", ""),
            image_url=metadata.get("image_url", ""),
            creative_description=creative_desc
        )
        response_products.append(product)
    return response_products

@app.get("/analytics-data")
def get_analytics_data():
    try:
        df = pd.read_csv("furniture_dataset.csv")
        df['price_numeric'] = df['price'].str.replace('$', '', regex=False).astype(float)
        top_brands = df['brand'].value_counts().nlargest(10).reset_index()
        top_brands.columns = ['name', 'products']
        price_dist = df['price_numeric'].dropna().tolist()
        return {"top_brands": top_brands.to_dict('records'), "price_distribution": price_dist, "total_products": int(df.shape[0]), "products_with_price": int(df['price_numeric'].count())}
    except Exception as e:
        return {"error": str(e)}

@app.get("/similar/{product_id}", response_model=list[Product])
def find_similar_products(product_id: str):
    """
    Finds visually similar products using the direct fetch method.
    """
    print(f"Finding similar products for ID: {product_id}")
    try:
        # 1. Use the direct fetch method to get the vector by its ID
        fetch_result = image_index.fetch(ids=[product_id])
        
        # 2. Robustly check if the fetch operation returned the vector
        if not fetch_result.vectors or product_id not in fetch_result.vectors:
            print(f"Fetch command failed to find the vector for ID {product_id}. The index may still be updating.")
            return []

        # 3. If found, get the vector and perform the similarity search
        source_vector = fetch_result.vectors[product_id].values
        
        similarity_results = image_index.query(
            vector=source_vector,
            top_k=7,
            include_metadata=True
        )

        # 4. Process results
        response_products = []
        for match in similarity_results.matches:
            if match.id == product_id: continue
            
            metadata = match.metadata
            creative_desc = generate_creative_description(
                title=metadata.get("title", ""),
                brand=metadata.get("brand", "")
            )
            product = Product(
                id=match.id,
                title=metadata.get("title", ""),
                brand=metadata.get("brand", ""),
                price=metadata.get("price", ""),
                image_url=metadata.get("image_url", ""),
                creative_description=creative_desc
            )
            response_products.append(product)

        return response_products[:6]

    except Exception as e:
        print(f"An unexpected error occurred in find_similar: {e}")
        return []

@app.get("/")
def read_root():
    return {"status": "API is running"}