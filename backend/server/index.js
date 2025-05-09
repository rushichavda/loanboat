const express = require('express');
const axios = require('axios');
const cors = require('cors');

require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

const PYTHON_API = 'http://localhost:5001';

app.get('/api/start', async (req, res) => {
  const response = await axios.get(`${PYTHON_API}/start`);
  res.json(response.data);
});

app.post('/api/respond', async (req, res) => {
  const response = await axios.post(`${PYTHON_API}/respond`, req.body);
  res.json(response.data);
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
