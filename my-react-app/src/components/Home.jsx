import React, { useState } from 'react'
import '../Styles/homeStyle.css'

function Home() {

    //Input and UI state variables
    const [url, setUrl] = useState("");
    const [isResultVisible, setIsResultVisible] = useState(false);
    const [averageStars, setAverageStars] = useState(null);
    const [topWords, setTopWords] = useState([]);
    const [summary, setSummary] = useState("")
    const [loading, setLoading] = useState(false)


    //Handles form submission
    const handleSubmit = ( async (e) => {
        //Prevent default form submission (page reload)
        e.preventDefault()
        setLoading(true)

        try{
            //Send user input to flask API via POST request
            const response = await fetch("http://127.0.0.1:5000/analyze", 
                {
                    method : "POST",
                    headers: {'Content-Type': 'application/json'},
                    body : JSON.stringify({url}),  
                }
            )
            const data = await response.json()
   
            //Update the state variables with response data
            if(response.ok){
            
                setAverageStars(data.average_stars)
                setTopWords(data.top_words)
                setSummary(data.summary)
                setIsResultVisible(true)

            }else{
                //if request doesn t succeed show alert
                alert("Something went wrong.")
            }
        }catch(error){
            alert("Error: "+error.message)
        }
        setLoading(false)
    });

  return (
    <div className='home'>
        <h1 className='header1'>Analyze The Reviews Of Your Favorite Amazon Product:</h1>
        <form onSubmit={handleSubmit} className='form'>
            <input 
                type="text" 
                value={url} 
                onChange={(e)=>setUrl(e.target.value)}
                placeholder = "Paste Amazon product URL..."
                className='urlInput'
            />
            <button type='submit' className='analyze-Button'>
                Analyze
            </button>

        </form>
        {/* Loading Spinner */}

        {loading && (
            <div className='loading'>⏳ Analyzing reviews, please wait...</div>
        )}
        
        {/* Display analysis result when backend has responded */}

        {isResultVisible && !loading && (
            <div className='result-box'>
                <h2>Analysis Result</h2>
                <p><strong>Average Stars:</strong>{averageStars}</p>
                <p><strong>Top Words:</strong></p>
                {Array.isArray(topWords) && (
                    <ul>
                        {topWords.map(([word, count], index) => (
                            <li key={index}>
                                {word}: {count}
                            </li>
                        ))}
                    </ul>
                )}
                <p><strong>Summary:</strong>{summary}</p> 
            </div>
        )}
      
    </div>
  )
}

export default Home

