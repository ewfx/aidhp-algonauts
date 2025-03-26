import React, { useState, useEffect } from "react";
import { Container, Typography, Box, Button, List, ListItem, ListItemText } from "@mui/material";

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [showAll, setShowAll] = useState(false);
  const [allTransactions, setAllTransactions] = useState([]);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async (fetchAll) => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/customer/transactions?all=${fetchAll}`, {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json"
          }
        });
  
        if (!response.ok) {
          throw new Error("Failed to load transactions");
        }
  
        const data = await response.json();
        setTransactions(data);
        setShowAll(fetchAll); // Update the button state
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };
  
    return (
      <Container>
        <Box sx={{ mt: 5, p: 3, borderRadius: 2, boxShadow: 3, textAlign: "center", backgroundColor: "white" }}>
          <Typography variant="h4" sx={{ fontWeight: "bold", color: "#b31b1b" }}>
            Transactions
          </Typography>
          <Typography variant="h6" sx={{ mt: 2 }}>
            View and manage your transactions here.
          </Typography>
  
          <List sx={{ mt: 2 }}>
            {transactions.map((txn, index) => (
              <ListItem key={index} sx={{ borderBottom: "1px solid #ddd" }}>
                <ListItemText
                  primary={`Amount: ₹${txn.amount}`}
                  secondary={`Date: ${txn.transaction_date} |  ${txn.transaction_type  ? "Credit" : "Debit"} `}
                />
              </ListItem>
            ))}
          </List>
  
          {!showAll && (
            <Button
              variant="contained"
              sx={{ mt: 2 }}
              onClick={() => fetchTransactions(true)}
            >
              View All Transactions
            </Button>
          )}
        </Box>
      </Container>
    );
  };
  
  export default Transactions;