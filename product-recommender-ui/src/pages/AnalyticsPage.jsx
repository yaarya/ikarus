import { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer} from 'recharts';
import './AnalyticsPage.css';

function StatCard({ title, value }) {
    return (
        <div className="stat-card">
            <h3>{title}</h3>
            <p>{value}</p>
        </div>
    );
}

function AnalyticsPage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/analytics-data');
                setData(response.data);
            } catch (err) {
                setError("Failed to fetch analytics data.");
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) return <p>Loading analytics...</p>;
    if (error) return <p className="error">{error}</p>;

    return (
        <div className="analytics-page">
            <h1>Dataset Analytics</h1>

            <div className="stats-grid">
                <StatCard title="Total Products" value={data.total_products} />
                <StatCard title="Products with Price" value={data.products_with_price} />
            </div>

            <div className="chart-container">
                <h2>Top 10 Brands by Product Count</h2>
                <ResponsiveContainer width="100%" height={400}>
                    <BarChart data={data.top_brands} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                        <XAxis dataKey="name" angle={-30} textAnchor="end" height={80} />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="products" fill="#8884d8" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default AnalyticsPage;