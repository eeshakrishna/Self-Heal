import React, { useState } from 'react';
import axios from 'axios';
import './loginRegister.css'
import Navbar from './navbar'

function Sentimental() {
  const [text, setText] = useState('');
  const [positiveScore, setPositiveScore] = useState(null);
  const [email, setEmail] = useState('');
  const [sentiment, setSentiment] = useState('')

  const handleSubmit = async (e) => {
    const data = { text, email: sessionStorage.getItem('email') };
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/analyze_sentiment', data, {
            withCredentials:true,
      });
      

      if (response.status !== 200) {
        throw new Error('Network response was not ok');
      }

      const responseData = response.data;
      setPositiveScore(responseData.compound_score);
      setSentiment(responseData.sentiment);

    } catch (error) {
      console.error('Error:', error);
      // Handle error here, e.g., show error message to user
    }
  };

  return (
  <>
  <Navbar/>
    <div className=" bby">
    <div className="App container">
      <p><strong> Did you feel about today's therapy session?Did you leave today's session feeling hopeful or discouraged about your progress? Please describe your experience in your own words.</strong></p>
      <form onSubmit={handleSubmit}>
        {/* <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email..."
          className="input-field"
        /> */}
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter your text..."
          className="input-field"
        />
        <button type="submit" className="button1">Analyze</button>
      </form>
      
      {positiveScore !== null && (
        <div>
          Score: {positiveScore}
          <br/>
          {sentiment} {/* Display sentiment here */}
        </div>
      )}
    </div>
    </div>
    </>
  );
}

export default Sentimental;