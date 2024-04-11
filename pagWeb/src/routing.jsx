import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App'
import Navbar from './components/navbar';
import Glossary from './components/glossary';
import { HistoryProvider } from './components/historyContext';
import HistoryPage from './components/historyPage';


function Routing() {
    return (
        <HistoryProvider>
            <BrowserRouter>
                <div>
                    <Navbar />
                    <Routes>
                        <Route path={"/"} element={<App />} />
                        <Route path="/glossary" element={<Glossary />} />
                        <Route path="/history" element={<HistoryPage />} />
                    </Routes>
                </div>
            </BrowserRouter>
        </HistoryProvider>
    )
}
export default Routing; 