import React, { useState } from "react";
import { Card, CardContent, Typography, Button, TextField, CircularProgress } from "@mui/material";
import { Box } from "@mui/system";
import axios from "axios";
import ReactMarkdown from "react-markdown";

export default function Insights() {
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [insights, setInsights] = useState("");
  const [recommendedProducts, setRecommendedProducts] = useState([]);

  const fetchInsights = async () => {
    if (!username) {
      alert("Please enter a username!");
      return;
    }

    setLoading(true);
    setInsights("");
    setRecommendedProducts([]);

    try {
      const response = await axios.get("http://localhost:5000/admin/insights", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        params: { username },
      });

      setInsights(response.data.insights);
      setRecommendedProducts(response.data.recommended_products);
    } catch (error) {
      setInsights("**Error fetching insights.** Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        backgroundColor: "#f3f4f6",
        padding: 3,
      }}
    >
      <Card
        sx={{
          width: "80vw", // Makes it responsive and takes 80% of the screen width
          maxWidth: "900px", // But keeps a reasonable max width
          padding: 3,
          boxShadow: 3,
        }}
      >
        <CardContent>
          <Typography variant="h5" textAlign="center" fontWeight="bold" gutterBottom>
            Risk Insights
          </Typography>

          <TextField
            fullWidth
            label="Enter Username"
            variant="outlined"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            sx={{ mb: 2 }}
          />

          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={fetchInsights}
            disabled={loading}
            sx={{ mb: 2 }}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : "Get Insights"}
          </Button>

          {loading && <Typography textAlign="center">Fetching insights...</Typography>}

          {insights && (
            <Box mt={3}>
              <Typography variant="subtitle1" fontWeight="bold">Insights:</Typography>
              <Box
                sx={{
                  backgroundColor: "#f9f9f9",
                  padding: "15px",
                  borderRadius: "8px",
                  border: "1px solid #ddd",
                  maxHeight: "400px", // Increased height
                  width: "100%", // Takes full width of parent
                  overflowY: "auto",
                }}
              >
                <ReactMarkdown>{insights}</ReactMarkdown>
              </Box>

              <Typography variant="subtitle1" fontWeight="bold" mt={2}>
                Recommended Products:
              </Typography>
              <Box component="ul" sx={{ pl: 2 }}>
                {recommendedProducts.map((product, index) => (
                  <Typography key={index} component="li" sx={{ fontSize: "14px", color: "#555" }}>
                    {product}
                  </Typography>
                ))}
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
