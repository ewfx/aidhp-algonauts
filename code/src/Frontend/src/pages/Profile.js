import { useEffect, useState } from "react";
import { Container, Typography, Box, CircularProgress } from "@mui/material";

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem("token"); // Get JWT token from local storage

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch("http://localhost:5000/customer/profile", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`, // Send token for authentication
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch profile");
        }

        const data = await response.json();
        setProfile(data);
      } catch (error) {
        console.error("Error fetching profile:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <Container sx={{ mt: 5, textAlign: "center" }}>
        <CircularProgress />
        <Typography sx={{ mt: 2 }}>Loading Profile...</Typography>
      </Container>
    );
  }

  return (
    <Container>
      <Box sx={{ mt: 5, p: 3, borderRadius: 2, boxShadow: 3, textAlign: "center", backgroundColor: "white" }}>
        <Typography variant="h4" sx={{ fontWeight: "bold", color: "#b31b1b" }}>
          Profile
        </Typography>
        
        {profile ? (
          <>
            <Typography variant="h6" sx={{ mt: 2 }}>Name: {profile.name}</Typography>
            <Typography variant="h6">Age: {profile.age}</Typography>
            <Typography variant="h6">Gender: {profile.gender}</Typography>
            <Typography variant="h6">Education: {profile.education}</Typography>
            <Typography variant="h6">Occupation: {profile.occupation}</Typography>
            <Typography variant="h6">Yearly Salary: Rs.{profile.yearly_salary}</Typography>
          </>
        ) : (
          <Typography variant="h6" sx={{ mt: 2, color: "red" }}>
            Profile data not found.
          </Typography>
        )}
      </Box>
    </Container>
  );
};

export default Profile;
