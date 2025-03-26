import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { 
  Container, Box, Typography, Button, MenuItem, Select, TextField 
} from "@mui/material";

const AddReview = () => {
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

  const [selectedProduct, setSelectedProduct] = useState("");
  const [reviewText, setReviewText] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedProduct || !reviewText.trim()) {
      alert("Please select a product and write a review.");
      return;
    }

    try {
      await axios.post("http://127.0.0.1:5000/customer/addreviews", {
        product_id: selectedProduct, // Sending only the product ID
        review: reviewText,
      },{
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json"
        }
      });

      alert("Review submitted successfully!");
      setSelectedProduct("");
      setReviewText("");
      navigate("/my-reviews"); // Redirect to MyReviews page
    } catch (error) {
      console.error("Error submitting review:", error);
      alert("Failed to submit review.");
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          mt: 5,
          p: 4,
          borderRadius: 2,
          boxShadow: 3,
          backgroundColor: "white",
          textAlign: "center",
        }}
      >
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#b31b1b", mb: 2 }}>
          Add a Review
        </Typography>
        <Typography variant="body1" sx={{ mb: 3 }}>
          Share your experience with one of our financial products.
        </Typography>

        <form onSubmit={handleSubmit}>
          {/* Product Selection */}
          <Select
            value={selectedProduct}
            onChange={(e) => setSelectedProduct(e.target.value)}
            fullWidth
            displayEmpty
            sx={{ mb: 3 }}
          >
            <MenuItem value="" disabled>Select a Product</MenuItem>
            {Object.entries(products).map(([id, name]) => (
              <MenuItem key={id} value={id}>{name}</MenuItem>
            ))}
          </Select>

          {/* Review TextField */}
          <TextField
            label="Write your review"
            multiline
            rows={4}
            fullWidth
            variant="outlined"
            value={reviewText}
            onChange={(e) => setReviewText(e.target.value)}
            sx={{ mb: 3 }}
          />

          {/* Submit Button */}
          <Button 
            type="submit" 
            variant="contained" 
            color="primary" 
            fullWidth
            disabled={!selectedProduct || !reviewText.trim()}
          >
            Submit Review
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default AddReview;
