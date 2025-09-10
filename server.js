const express = require("express");
const multer = require("multer");
const axios = require("axios");
const cors = require("cors");
const { MongoClient } = require("mongodb");
const FormData = require("form-data");

require("dotenv").config();

const app = express();
app.use(cors());
const upload = multer({ storage: multer.memoryStorage() });

const mongo = new MongoClient(process.env.MONGO_URI);
const dbName = "career_db";
const collectionName = "resume_results";

let db, collection;

async function initMongo() {
  if (!db) {
    await mongo.connect();
    db = mongo.db(dbName);
    collection = db.collection(collectionName);
  }
}

app.post("/upload-resume", upload.single("file"), async (req, res) => {
  try {
    await initMongo();

    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded." });
    }

    const formData = new FormData();
    formData.append("file", req.file.buffer, req.file.originalname);
    formData.append("interest", req.body.interest);

    const response = await axios.post("http://localhost:8009/analyze/", formData, {
      headers: formData.getHeaders()
    });

    const result = response.data;

    const inserted = await collection.insertOne({
      file: req.file.originalname,
      interest: req.body.interest,
      result,
      createdAt: new Date()
    });

    res.json({ _id: inserted.insertedId, ...result });

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Failed to process resume." });
  }
});

app.listen(5000, () => {
  console.log("✅ Node server running at http://localhost:5000");
});
