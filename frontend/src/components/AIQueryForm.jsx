import React, { useState } from "react";
import logo from "../assets/scent-genie-logo.png";
// A simple component to accept AI text query
export default function AIQueryForm() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  //   Temp handle submit until backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(query);
    // try {
    //   // Replace this with your API endpoint
    //   const res = await fetch("/api/ai-query", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({ query }),
    //   });
    //   if (!res.ok) throw new Error("Failed to fetch AI response");
    //   const data = await res.json();
    //   setResponse(data.response);
    // } catch (err) {
    //   setError(err.message);
    // } finally {
    //   setLoading(false);
    // }
  };

  return (
    <div
      style={{
        maxWidth: "600px",
        marginBottom: "2rem",
        marginTop: "0px",
        marginLeft: "auto",
        marginRight: "auto",
        textAlign: "center",
      }}
    >
      <form onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Describe your fragrance..."
          rows={4}
          style={{
            width: "100%",
            padding: "0.5rem",
            fontSize: "1rem",
            resize: "none",
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{ marginTop: "1rem", padding: "0.5rem 1rem" }}
        >
          {loading ? "Loading..." : "Submit"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {response && (
        <div
          style={{
            marginTop: "2rem",
            padding: "1rem",
            border: "1px solid #ccc",
            borderRadius: "8px",
          }}
        >
          <strong>AI Response:</strong>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
