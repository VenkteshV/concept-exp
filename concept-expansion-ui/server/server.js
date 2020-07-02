'use strict';
const express = require('express');
const app = express();
const bodyParser = require('body-parser');

const jvm_route = require('./routes/jvmtuning');
const path = require('path');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.use(express.static('dist'));
/* istanbul ignore next */
app.get('/', function (request, response) {
/* istanbul ignore next */
  response.redirect('index.html');
});
/* istanbul ignore next */
const port = process.env.PORT || 3200;
app.listen(port, function () {
  console.log(`Application listening on port ${port}`);
});

app.use('/concept', jvm_route);
module.exports = app;
