import React, { useState, useEffect } from "react";
import { Container, Typography, Box, Button, List, Card, CardContent, ListItem, ListItemText } from "@mui/material";

const MyReviews = () => {
  const [reviews, setReviews] = useState([]);
  const [showAll, setShowAll] = useState(false);
  const products = {
    1: "Home Loan",
    2: "Personal Loan",
    3: "Credit Card",
    4: "Fixed Deposit",
    5: "Recurring Deposit",
    6: "Mutual Fund",
    7: "Equity Shares",
    8: "Government Bonds",
    9: "Gold ETF",
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  const fetchReviews = async (fetchAll = false) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/customer/reviews`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json"
        }
      });

      if (!response.ok) {
        throw new Error("Failed to load reviews");
      }

      const data = await response.json();
      setReviews(data);
      setShowAll(fetchAll); // Update button state
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  return (
    <Container maxWidth="md">
      <Box 
        sx={{
          mt: 5,
          p: 4,
          borderRadius: 3,
          boxShadow: 4,
          textAlign: "center",
          backgroundColor: "#f8f9fa",
        }}
      >
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#b31b1b" }}>
          My Reviews
        </Typography>
        <Typography variant="h6" sx={{ mt: 1, color: "text.secondary" }}>
          See all your product reviews below.
        </Typography>

        <List sx={{ mt: 3 }}>
          {reviews.map((review, index) => (
            <Card key={index} variant="outlined" sx={{ mb: 2, borderRadius: 2, boxShadow: 1 }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: "bold", color: "#1a237e" }}>
                  {products[review.product_id]}
                </Typography>
                <Typography variant="body1" sx={{ mt: 1, color: "text.primary" }}>
                  "{review.review_text}"
                </Typography>
                <Typography variant="body2" sx={{ mt: 1, color: "text.secondary" }}>
                  Date: {review.review_date} | Sentiment: {review.is_positive ? "Positive 👍" : "Negative 👎"}
                </Typography>
              </CardContent>
            </Card>
          ))}
        </List>

        {!showAll && (
          <Button
            variant="contained"
            sx={{
              mt: 3,
              backgroundColor: "#b31b1b",
              "&:hover": { backgroundColor: "#8a1414" },
            }}
            onClick={() => fetchReviews(true)}
          >
            View All Reviews
          </Button>
        )}
      </Box>
    </Container>
  );
};

export default MyReviews;
