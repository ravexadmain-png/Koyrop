async function copyCode(btn, filePath) {
    try {
        const response = await fetch(filePath);
        const text = await response.text();
        navigator.clipboard.writeText(text);
        let originalText = btn.innerText;
        btn.innerText = "✔ Copied!";
        btn.style.background = "#059669";
        setTimeout(() => {
            btn.innerText = originalText;
            btn.style.background = "#10b981";
        }, 2000);
    } catch (err) {
        alert("Failed to copy file content.");
    }
}
