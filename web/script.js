async function fetchLatest() {
  const status = document.getElementById("status");
  const tableBody = document.getElementById("latest-table-body");

  try {
    const res = await fetch("/api/latest");
    if (!res.ok) throw new Error("API returned " + res.status);
    const data = await res.json();

    // Töm tabellen
    tableBody.innerHTML = "";

    if (!Array.isArray(data) || data.length === 0) {
      status.textContent = "No messages received yet.";
      return;
    }

    // Lägg till nya rader
    for (const d of data) {
      const row = document.createElement("tr");

      const topicCell = document.createElement("td");
      topicCell.textContent = d.topic || "–";

      const payloadCell = document.createElement("td");
      payloadCell.textContent = d.payload ?? "–";

      const timeCell = document.createElement("td");
      try {
        const time = new Date(d.timestamp).toLocaleTimeString();
        timeCell.textContent = time;
      } catch {
        timeCell.textContent = "Invalid timestamp";
      }

      row.appendChild(topicCell);
      row.appendChild(payloadCell);
      row.appendChild(timeCell);
      tableBody.appendChild(row);
    }

    status.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
  } catch (err) {
    tableBody.innerHTML = "";
    status.innerHTML = `<span style="color:red;">Failed to fetch data: ${err.message}</span>`;
    console.error("Fetch error:", err);
  }
}

setInterval(fetchLatest, 2000);
fetchLatest();
