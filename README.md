# AI-Powered Furniture Recommender

This project is a full-stack, AI-driven web application designed to recommend furniture products based on natural language queries. It integrates multiple AI domains including Natural Language Processing, Computer Vision, and Generative AI. The application was developed to fulfill the requirements of a 2-day intern assignment, demonstrating rapid prototyping and end-to-end system design.

---

## Key Features

-   **Semantic Search:** Utilizes sentence-transformer models to understand the intent behind a user's natural language query and find the most relevant products.
-   **Generative Product Descriptions:** Employs the Google Gemini API to generate unique and creative descriptions for each recommended product in real-time.
-   **Visual Similarity Search (Simulated):** A feature to find visually similar items. Due to limitations discovered with the database service's free tier during development, this feature is simulated by performing a text-based search on the selected product's title.
-   **Data Analytics Dashboard:** A dedicated page that provides visualizations and insights from the product dataset, including breakdowns by brand and price.

---

## Tech Stack

| Category        | Technology                                                                |
| --------------- | ------------------------------------------------------------------------- |
| **Frontend** | React, Vite, Axios, Recharts, React Router                                |
| **Backend** | Python, FastAPI, Uvicorn                                                  |
| **Database** | Pinecone (Vector Database)                                                |
| **AI / ML** | `sentence-transformers`, PyTorch (`timm`), Google Gemini, Pandas, Jupyter |

---

## System Architecture

The application follows a decoupled frontend-backend architecture.

    [User] -> [React Frontend (Vercel)] -> [FastAPI Backend (Render)] -> [Pinecone (Embeddings)]
                                                      |
                                                      +-> [Google Gemini API (GenAI)]

-   The **React Frontend** provides the user interface.
-   The **FastAPI Backend** serves the recommendation logic and analytics data.
-   **Pinecone** stores and retrieves vector embeddings for similarity search.
-   **Google Gemini** generates creative text on demand.

---

## Setup and Running Locally

### Prerequisites
-   Python 3.9+
-   Node.js v18+ and npm
-   A Pinecone API Key
-   A Google AI (Gemini) API Key

### 1. Backend Setup

    # 1. Clone the repository
    git clone <your-repository-url>
    cd <repository-name>

    # 2. Install Python dependencies
    # It is recommended to use a virtual environment
    # python -m venv venv
    # source venv/bin/activate  (or venv\Scripts\activate on Windows)
    pip install -r requirements.txt

    # 3. Create a .env file in the root directory
    #    and add your secret API keys:
    #
    # PINECONE_API_KEY="YOUR_PINECONE_API_KEY"
    # GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"

    # 4. Generate embeddings and populate the database by running
    #    the Data_Pipeline.ipynb notebook from top to bottom.

    # 5. Start the backend server
    python -m uvicorn main:app --reload

The backend will be running at `http://127.0.0.1:8000`.

### 2. Frontend Setup

    # 1. Navigate to the frontend directory
    cd product-recommender-ui

    # 2. Install npm dependencies
    npm install

    # 3. Start the frontend development server
    npm run dev

The frontend will be running at `http://localhost:5173` by default.

---

## Project Deliverables

-   **`/main.py`**: The FastAPI backend server containing all API endpoints.
-   **`/product-recommender-ui`**: The complete React frontend application.
-   **`/Data_Pipeline.ipynb`**: The Jupyter notebook responsible for data cleaning, preprocessing, embedding generation, and uploading to Pinecone.
-   **`/Analytics_Notebook.ipynb`**: The Jupyter notebook used for exploratory data analysis and visualization.
-   **`/requirements.txt`**: A list of all Python dependencies for the backend.

---

## Future Improvements

While the current implementation fulfills the assignment requirements, the following professional-grade improvements could be made:

-   **Hybrid Search:** Implement a fused search score combining both text and image similarity to provide more nuanced recommendations. This would require using a multi-modal embedding model like CLIP.
-   **Metadata Filtering:** Enhance the `/recommend` endpoint to accept filters (e.g., price range, brand, category) and apply them during the Pinecone query for a more interactive user experience.
-   **Backend Caching:** Implement a caching layer (e.g., with Redis) for GenAI descriptions and embedding lookups to reduce latency and API costs.
-   **Custom Image Classifier:** Train a lightweight image classification model (e.g., using transfer learning on an EfficientNet) to clean and enrich the product category data.
