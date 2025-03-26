import React, { useEffect, useState } from "react";
import axios from "axios";
import { Container, Box, Typography, Card, CardContent, Grid, CircularProgress, Alert } from "@mui/material";

const FinancialDetails = () => {
  const [financialData, setFinancialData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFinancialDetails = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/customer/finance", {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
          },
        });

        setFinancialData(response.data);
      } catch (err) {
        setError("Failed to fetch financial details.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFinancialDetails();
  }, []);

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          mt: 5,
          p: 4,
          borderRadius: 3,
          boxShadow: 4,
          backgroundColor: "#f8f9fa",
          textAlign: "center",
        }}
      >
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#1a237e" }}>
          My Financial Details
        </Typography>

        {loading ? (
          <CircularProgress sx={{ mt: 3 }} />
        ) : error ? (
          <Alert severity="error" sx={{ mt: 3 }}>{error}</Alert>
        ) : financialData.length === 0 ? (
          <Alert severity="info" sx={{ mt: 3 }}>No financial records found.</Alert>
        ) : (
          <Grid container spacing={3} sx={{ mt: 3 }}>
            {financialData.map((item, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card sx={{ borderRadius: 2, boxShadow: 2 }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ fontWeight: "bold", color: "#b31b1b" }}>
                      {item.product_name}
                    </Typography>
                    
                    {item.investment_amount && (
                      <Typography variant="body1">
                        💰 Investment Amount: ₹{item.investment_amount.toLocaleString()}
                      </Typography>
                    )}

                    {item.loan_amount && (
                      <Typography variant="body1">
                        🏦 Loan Amount: ₹{item.loan_amount.toLocaleString()}
                      </Typography>
                    )}

                    {item.credit_limit && (
                      <Typography variant="body1">
                        💳 Credit Limit: ₹{item.credit_limit.toLocaleString()}
                      </Typography>
                    )}

                    {item.credit_utilization && (
                      <Typography variant="body1">
                        📊 Credit Utilization: {item.credit_utilization}%
                      </Typography>
                    )}

                    {item.tenure_months && (
                      <Typography variant="body1">
                        📅 Tenure: {item.tenure_months} months
                      </Typography>
                    )}

                    {item.returns_percentage && (
                      <Typography variant="body1">
                        📈 Returns: {item.returns_percentage}%
                      </Typography>
                    )}

                    {item.emi_paid && (
                      <Typography variant="body1">
                        💵 EMIs Paid: {item.emi_paid}
                      </Typography>
                    )}

                    {item.max_dpd && (
                      <Typography variant="body1">
                        ⏳ Max DPD: {item.max_dpd} days
                      </Typography>
                    )}

                    <Typography
                      variant="body2"
                      sx={{ mt: 1, color: item.default_status ? "red" : "green", fontWeight: "bold" }}
                    >
                      {item.default_status ? "⚠️ Defaulted" : "✅ No Default"}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Container>
  );
};

export default FinancialDetails;

