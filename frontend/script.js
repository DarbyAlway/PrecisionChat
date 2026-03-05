document.getElementById('compareBtn').addEventListener('click', async () => {
    const query = document.getElementById('queryInput').value;
    const sarResult = document.getElementById('sarResult');
    const ragResult = document.getElementById('ragResult');

    if (!query) return;

    sarResult.innerHTML = "<p class='loading'>Thinking (SAR)...</p>";
    ragResult.innerHTML = "<p class='loading'>Thinking (RAG)...</p>";

    // Function to convert text URLs into clickable HTML links
    const linkify = (text) => {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, (url) => {
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
        });
    };

    try {
        const response = await fetch('/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (data.status === "success") {
            // 1. Convert newlines to <br>
            // 2. Convert raw URLs to <a> tags using linkify
            sarResult.innerHTML = linkify(data.answer_SAR.replace(/\n/g, "<br>"));
            ragResult.innerHTML = linkify(data.answer_RAG.replace(/\n/g, "<br>"));
        } else {
            sarResult.innerHTML = "Error: " + data.message;
            ragResult.innerHTML = "Error: " + data.message;
        }

    } catch (error) {
        sarResult.innerHTML = "Connection failed.";
        ragResult.innerHTML = "Connection failed.";
        console.error(error);
    }
});