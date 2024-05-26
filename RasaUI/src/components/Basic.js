import React, { useEffect, useState } from 'react';
import {IoMdSend} from 'react-icons/io';
import {BiBot, BiUser} from 'react-icons/bi';
import axios from 'axios';
import './chatBot.css';
// import Navbar from './navbar'
import {Link} from 'react-router-dom'

function Basic() {
    const [chat, setChat] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [botTyping, setBotTyping] = useState(false);
    const [recognition, setRecognition] = useState(null);
    const [isRecognizing, setIsRecognizing] = useState(false);
    const synth = window.speechSynthesis;

    useEffect(() => {
        let newRecognition = null;
        if (window.SpeechRecognition || window.webkitSpeechRecognition) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            newRecognition = new SpeechRecognition();
            newRecognition.continuous = false;

            newRecognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                setInputMessage(transcript);
            };

            newRecognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
            };

            setRecognition(newRecognition);
        } else {
            console.error('Speech recognition not supported by your browser.');
        }

        // Cleanup function to stop recognition when component unmounts
        return () => {
            if (newRecognition && isRecognizing) {
                newRecognition.stop();
            }
        };
    }, [isRecognizing]);

    const handleSpeechRecognition = () => {
        if (recognition) {
            if (isRecognizing) {
                recognition.stop();
                setIsRecognizing(false);
            } else {
                recognition.start();
                setIsRecognizing(true);
            }
        } else {
            console.error('Speech recognition not initialized.');
        }
    };

    const handleSubmit = (evt) => {
        evt.preventDefault();
        const name = "Self Heal";
        const request_temp = {sender: "user", sender_id: name, msg: inputMessage};
        
        if (inputMessage.trim() !== "") {
            setChat(chat => [...chat, request_temp]);
            setBotTyping(true);
            setInputMessage('');
            rasaAPI(name, inputMessage);
        } else {
            window.alert("Please enter a valid message");
        }
    };

    const emergencybutton = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/emergency', {
            email:sessionStorage.getItem('email')
            }, {
                headers: {
                    'Content-Type': 'application/json'
                },
                withCredentials: true
            });
    
            if (response.status === 200) {
                alert(response.data.message);
            } else {
                alert('Failed to send emergency alert');
            }
        } catch (error) {
            console.error('Error sending emergency message:', error);
            alert('An error occurred while sending the emergency message.');
        }
      };

    const rasaAPI = async function handleClick(name, msg) {
        try {
            const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'charset': 'UTF-8',
                },
                credentials: "same-origin",
                body: JSON.stringify({ "sender": name, "message": msg }),
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const responseData = await response.json();
            if (responseData && responseData.length > 0) {
                const temp = responseData[0];
                const recipient_id = temp["recipient_id"];
                const recipient_msg = temp["text"];
                
                const response_temp = { sender: "bot", recipient_id: recipient_id, msg: recipient_msg };
                setBotTyping(false);
                setChat(chat => [...chat, response_temp]);
                speak(recipient_msg); // Speak bot's response
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    };
    

    const speak = (text) => {
        const utterance = new SpeechSynthesisUtterance(text);
        synth.speak(utterance);
    };

    const stylecard = {
        maxWidth: '35rem',
        border: '1px solid black',
        paddingLeft: '0px',
        paddingRight: '0px',
        borderRadius: '30px',
        boxShadow: '0 16px 20px 0 rgba(0,0,0,0.4)'
    };

    const styleHeader = {
        height: '4.5rem',
        borderBottom: '1px solid black',
        borderRadius: '30px 30px 0px 0px',
        backgroundColor: '#8012c4'
    };

    const styleFooter = {
        borderTop: '1px solid black',
        borderRadius: '0px 0px 30px 30px',
        backgroundColor: '#8012c4'
    };

    const styleBody = {
        paddingTop: '10px',
        height: '28rem',
        overflowY: 'auto',
        overflowX: 'hidden'
    };

    return (
    <>
        <div>
            <div className="container">
                <div className="row justify-content-center">
                    <div className="card" style={stylecard}>
                        <div className="cardHeader text-white" style={styleHeader}>
                            <h1 style={{marginBottom:'0px'}}>AI Assistant</h1>
                            {botTyping ? <h6>Bot Typing....</h6> : null}
                        </div>
                        <div className="cardBody" id="messageArea" style={styleBody}>
                            <div className="row msgarea">
                                {chat.map((user, key) => (
                                    <div key={key}>
                                        {user.sender === 'bot' ? (
                                            <div className='msgalignstart'>
                                                <BiBot className="botIcon" />
                                                <h5 className="botmsg">{user.msg}</h5>
                                            </div>
                                        ) : (
                                            <div className='msgalignend'>
                                                <h5 className="usermsg">{user.msg}</h5>
                                                <BiUser className="userIcon" />
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="cardFooter text-white" style={styleFooter}>
                            <div className="row">
                                <form style={{display: 'flex'}} onSubmit={handleSubmit}>
                                    <div className="col-10" style={{paddingRight:'0px'}}>
                                        <input onChange={e => setInputMessage(e.target.value)} value={inputMessage} type="text" className="msginp" />
                                    </div>
                                    <div className="col-2 cola">
                                        <button type="button" onClick={handleSpeechRecognition} className="circleBtn">
                                            <IoMdSend className="sendBtn" />
                                        </button>
                                    </div>
                                </form>
                            </div>
                             <button id="emergencyButton"  onClick={emergencybutton} className="emergency" >Emergency</button>
                            <Link to="/analyze_sentiment"><button id="emergencyButton"   className="emergency" >Generate Report</button></Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    );
}

export default Basic;