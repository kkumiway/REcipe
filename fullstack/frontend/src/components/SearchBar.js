import React, { useState } from "react";
import "../App.css"; // 스타일 적용

const SearchBar = ({ onSearch }) => {
    const [input, setInput] = useState("");

    const handleSearch = () => {
        onSearch(input);
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            handleSearch();
        }
    };

    return (
        <div className="search-container">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="재료 입력 (예: 계란)"
                className="search-input"
            />
            <button onClick={handleSearch} className="search-button">
                검색
            </button>
        </div>
    );
};

export default SearchBar;