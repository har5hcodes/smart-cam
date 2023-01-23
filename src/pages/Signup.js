import * as React from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import "../index.css";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

export default function Signup() {
  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log({
      email: data.get("email"),
      password: data.get("password"),
    });
  };

  return (
    <Grid container component="main" sx={{ height: "100vh" }}>
      <CssBaseline />
      <Grid
        item
        xs={false}
        sm={4}
        md={7}
        sx={{
          backgroundImage: "url(https://source.unsplash.com/random)",
          backgroundRepeat: "no-repeat",
          backgroundColor: (t) =>
            t.palette.mode === "light"
              ? t.palette.grey[50]
              : t.palette.grey[900],
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />
      <Grid
        item
        xs={12}
        sm={8}
        md={5}
        component={Paper}
        elevation={6}
        square
        sx={{ backgroundColor: "#000" }}
      >
        <Box
          sx={{
            my: 8,
            mx: 4,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Typography
            component="h1"
            variant="h4"
            color="white"
            sx={{ fontWeight: "600", textTransform: "uppercase" }}
          >
            Sign up
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 1 }}
          >
            <TextField
              sx={{ input: { color: "white" } }}
              margin="normal"
              required
              color="error"
              fullWidth
              id="name"
              label="Name"
              type="text"
              name="name"
              autoComplete="name"
              autoFocus
              InputLabelProps={{
                style: { color: "#fff" },
              }}
            />
            <TextField
              sx={{ input: { color: "white" } }}
              margin="normal"
              color="error"
              required
              fullWidth
              id="email"
              type="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              autoFocus
              InputLabelProps={{
                style: { color: "#fff" },
              }}
            />
            <TextField
              sx={{ input: { color: "white" } }}
              color="error"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              InputLabelProps={{
                style: { color: "#fff" },
              }}
            />
            <TextField
              sx={{ input: { color: "white" } }}
              color="error"
              margin="normal"
              required
              fullWidth
              name="cnf-password"
              label="Confirm Password"
              type="password"
              id="cnf-password"
              InputLabelProps={{
                style: { color: "#fff" },
              }}
            />
            <Button
              variant="contained"
              type="submit"
              fullWidth
              sx={{ backgroundColor: "#FC1503", color: "white", mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
}
