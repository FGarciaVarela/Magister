import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App'
import Navbar from './components/navbar';
import Glossary from './components/glossary';


function Routing() {
    return (
        <BrowserRouter>
            <div>
                <Navbar />
                <Routes>
                    <Route path={"/"} element={<App />} />
                    <Route path="/" element={<div>Inicio</div>} />
                    <Route path="/glossary" element={<Glossary />} />
                </Routes>
            </div>
        </BrowserRouter>
    )
}
export default Routing; 