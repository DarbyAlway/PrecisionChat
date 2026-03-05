
const queryInput = document.getElementById('queryInput');
const compareBtn = document.getElementById('compareBtn');

async function runSearch() {

    const query = queryInput.value;

    const sarResult = document.getElementById('sarResult');
    const ragResult = document.getElementById('ragResult');

    if (!query) return;

    sarResult.innerHTML = "<p>Thinking (SAR)...</p>";
    ragResult.innerHTML = "<p>Thinking (RAG)...</p>";

    const linkify = (text) => {
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        return text.replace(urlRegex, (url) => {
            return `<a href="${url}" target="_blank">${url}</a>`;
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
}

compareBtn.addEventListener('click', runSearch);

queryInput.addEventListener('keydown', (event) => {
    if (event.key === "Enter") {
        runSearch();
    }
});
