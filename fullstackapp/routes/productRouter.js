// core modules
const path = require('path');
const rootdir = require('../utils/pathutil');

// external modules
const express = require('express');
const laptopRouter = express.Router();
const laptopController = require('../controllers/productController');
const productController = require('../controllers/product_details')

laptopRouter.get('/',laptopController.laptopRouter);

laptopRouter.post('/add_product',laptopController.postadd_product);


laptopRouter.get('/product/:product_name',productController.product);

module.exports = laptopRouter




