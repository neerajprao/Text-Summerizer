async function summarizeText() {
    const inputText = document.getElementById('inputText').value;
    if (!inputText.trim()) {
        alert("Please enter a paragraph to summarize.");
        return;
    }
    
    const response = await fetch('/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: inputText })
    });
    
    const result = await response.json();
    document.getElementById('summaryText').innerText = result.summary;
    document.getElementById('summaryContainer').style.display = 'block';
}
