import { useState } from 'react';
import axios from 'axios';
import '../App.css';

function RecommenderPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResults([]);

    try {
      const response = await axios.post('http://127.0.0.1:8000/recommend', {
        query: query,
        top_k: 6
      });
      setResults(response.data);
    } catch (err) {
      console.error("Error fetching recommendations:", err);
      setError("Failed to get recommendations. Make sure the backend server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Furniture Recommender</h1>
        <p>Describe the furniture you're looking for</p>
      </header>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., a comfortable leather armchair for my study..."
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      <div className="results-grid">
        {results.map((product) => (
          <div key={product.id} className="product-card">
            <img src={product.image_url} alt={product.title} />
            <div className="product-info">
              <h3>{product.title}</h3>
              <p className="brand">{product.brand}</p>
              <p className="description">{product.creative_description}</p>
              <p className="price">{product.price}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommenderPage;