import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Paper,
  IconButton,
  Button,
  Box,
  Modal,
  TextField,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

const SearchBar = () => {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const [searchTerm, setSearchTerm] = useState("");
  const navigate = useNavigate();

  const onhandleSubmit = (e) => {
    e.preventDefault();

    if (searchTerm) {
      navigate(`/search/${searchTerm}`);

      setSearchTerm("");
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",

        justifyContent: "flex-end",
      }}
    >
      <Paper
        component="form"
        onSubmit={onhandleSubmit}
        sx={{
          borderRadius: 20,
          border: "1px solid #e3e3e3",
          pl: 2,
          boxShadow: "none",
          mr: { sm: 5 },
        }}
      >
        <input
          className="search-bar"
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <IconButton
          type="submit"
          sx={{ p: "10px", color: "red" }}
          aria-label="search"
        >
          <SearchIcon />
        </IconButton>
      </Paper>

      <Button
        variant="text"
        sx={{
          marginTop: "5px",
          marginBottom: "5px",
          marginLeft: 0,
          color: "#FC1503",
          marginRight: "20px",
        }}
      >
        Sign Up
      </Button>

      <Button
        variant="text"
        sx={{
          marginTop: "5px",
          marginBottom: "5px",
          marginLeft: 0,
          color: "#FC1503",
          marginRight: "20px",
        }}
      >
        Log In
      </Button>

      <Button
        onClick={handleOpen}
        variant="outlined"
        sx={{
          marginTop: "5px",
          marginBottom: "5px",
          marginLeft: 0,
          color: "#FC1503",
          borderColor: "#FC1503",
          marginRight: "20px",
        }}
      >
        Submit a webcam
      </Button>

      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Box sx={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <TextField
              color="secondary"
              id="outlined-basic"
              label="Webcam Name"
              variant="outlined"
            />
            <TextField
              color="secondary"
              id="outlined-basic"
              label="Webcam url"
              variant="outlined"
            />
            <Button
              variant="contained"
              sx={{ backgroundColor: "#FC1503", color: "white" }}
            >
              Submit webcam
            </Button>
          </Box>
        </Box>
      </Modal>
    </Box>
  );
};

export default SearchBar;
