import React, {useState} from "react";
import "./Post.css"
import ReactMarkdown from 'react-markdown';

const BASE_URL = "http://localhost:8000/"


function NewChat(){

    const [webUrl, setWebUrl] = useState('')
    const [companyName, setCompanyName] = useState('')
    const [brochure, setBrochure] = useState('')
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);


    const handleUrl = async (e) => {
        e.preventDefault();
        // console.log("URL submitted: ", webUrl);
        if (!webUrl || !companyName){
            setError("Please enter both a URL and a Company Name.");
            setBrochure('');
            return;
        }
        setIsLoading(true)
        setError(null)
        setBrochure('')

        const requestOptions = {
            method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    url: webUrl, 
                    company_name: companyName
                 }), // Sending URL in JSON format
            }
        
        try {
            // Assuming your FastAPI endpoint for summarization is '/summarize'
            // and it expects a JSON body like { "url": "..." }
            const response = await fetch(BASE_URL + "brochure", requestOptions);

            if (!response.ok) {
                // Handle HTTP errors (e.g., 404, 500)
                const errorData = await response.json();
                throw new Error(
                    errorData.detail || `HTTP error! status: ${response.status}`
                );
            }

            const data = await response.json();
            // Assuming your FastAPI returns a JSON like { "summary": "..." }
            setBrochure(data.result);

        } 
        catch (err) {
            console.error("Error fetching brochure:", err);
            setError(err.message);
            setBrochure(''); // Ensure summary is cleared on error
        } 
        finally {
            setIsLoading(false); // Reset loading state regardless of success or failure
        }
    }

    return(
        <div>
            <div className="input_group">
                <div className="company_name_input">
                    <input className="company_name_text" 
                        type="text" 
                        id="company_name_text" 
                        placeholder="Company Name"
                        onChange={(event)=> setCompanyName(event.target.value)}
                        value={companyName} />
                </div>

                <div className="web_url">
                    <input className="url_text" 
                        type="text" 
                        id="url_text" 
                        placeholder="URL"
                        onChange={(event)=> setWebUrl(event.target.value)}
                        value={webUrl} />
                </div>
            </div>
            
            <div>
                <button 
                className="create_button" 
                onClick={handleUrl}
                disabled={isLoading || !webUrl || !companyName}> {/* Disable button if loading or no URL or company_name entered */}
                    {isLoading ? 'Creating Brochure...' : 'Create Brochure'}
                </button>
            </div>

            {brochure && (
                <div className="brochure-box">
                <h3>Brochure Summary</h3>
                    <div className="brochure-content">
                        <ReactMarkdown>
                            {brochure.replace(/^, ```markdown\n/, '').replace(/\n```, $/, '').trim()}
                        </ReactMarkdown>
                    </div>
                </div>
            )}
            {error && (
                <div className="error-message" style={{ color: 'red', marginTop: '10px' }}>
                    {error}
                </div>
            )}
            
        </div>
        
    )}

export default NewChat