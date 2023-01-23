import { removeStopwords, eng, fra } from "stopword";
import React from "react";
import { Link } from "react-router-dom";
import {
  Typography,
  Card,
  CardContent,
  CardMedia,
  Button,
  Container,
  Modal,
  Box,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CheckBoxSharpIcon from "@mui/icons-material/CheckBox";

import {
  demoThumbnailUrl,
  demoVideoUrl,
  demoVideoTitle,
  demoChannelUrl,
  demoChannelTitle,
} from "../utils/constants";

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

const VideoCard = ({
  video: {
    id: { videoId },
    snippet,
  },
}) => {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const description = snippet.description.slice(0, 45);
  console.log(description);
  const { removeStopwords } = require("stopword");
  const oldString = description.split(" ");
  const tagsList = removeStopwords(oldString);

  // putting tags by reversing every word in the videos description
  // let tag = "";
  // for (let i = 0; i < description.length; i++) {
  //   if (description[i] !== " ") {
  //     tag += description[i];
  //   } else {
  //     if (tag.length > 0) {
  //       tag = tag.split("").reverse().join("");
  //       tagsList.push(tag);
  //     }
  //     tag = "";
  //   }
  // }

  return (
    <Card
      sx={{
        width: { xs: "100%", sm: "358px", md: "320px" },
        boxShadow: "none",
        borderRadius: 0,
      }}
    >
      <Link to={videoId ? `/video/${videoId}` : `/video/cV2gBU6hKfY`}>
        <CardMedia
          image={snippet?.thumbnails?.high?.url || demoThumbnailUrl}
          alt={snippet?.title}
          sx={{ width: { xs: "100%", sm: "358px" }, height: 180 }}
        />
      </Link>
      <CardContent sx={{ backgroundColor: "#1E1E1E", height: "106px" }}>
        <Link to={videoId ? `/video/${videoId}` : demoVideoUrl}>
          <Box sx={{ display: "flex", flexDirection: "row" }}>
            {tagsList.map((tag) => (
              <Typography
                variant="subtitle1"
                fontSize="12px"
                color="#FFF"
                sx={{
                  marginRight: "4px",
                  padding: "2px 7px",
                  borderRadius: "50px",
                  backgroundColor: "#FF5C5C",
                }}
              >
                {/* {snippet?.title.slice(0, 60) || demoVideoTitle.slice(0, 60)} */}
                {tag}
              </Typography>
            ))}
          </Box>
        </Link>
        <Link
          to={
            snippet?.channelId
              ? `/channel/${snippet?.channelId}`
              : demoChannelUrl
          }
        >
          <Typography variant="subtitle2" color="gray">
            {snippet?.channelTitle || demoChannelTitle}
            <CheckCircleIcon
              sx={{ fontSize: "12px", color: "gray", ml: "5px" }}
            />
          </Typography>
        </Link>
        <Button
          onClick={handleOpen}
          variant="outlined"
          sx={{
            marginTop: "5px",
            marginBottom: "5px",
            marginLeft: 0,
            color: "#FC1503",
            borderColor: "#FC1503",
          }}
        >
          Analyse
        </Button>
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={style}>
            <Box
              sx={{
                display: "flex",
                flexDirection: "row-reverse",
                justifyContent: "start",
                alignItems: "center",
              }}
            >
              <Typography id="modal-modal-title" variant="h6" component="h2">
                Successfully sent to backend
              </Typography>
              <CheckBoxSharpIcon sx={{ color: "green", fontSize: "48px" }} />
            </Box>
            <Typography id="modal-modal-description" sx={{ mt: 2 }}>
              Our backend will start taking snapshots of the stream in
              intervals.
            </Typography>
          </Box>
        </Modal>
      </CardContent>
    </Card>
  );
};

export default VideoCard;
