import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import RecommenderPage from './pages/RecommenderPage'; 
import AnalyticsPage from './pages/AnalyticsPage';
import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<RecommenderPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;