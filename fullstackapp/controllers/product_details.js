const path = require('path');
const db = require('../models/db').pgpool

exports.product = async (req, res, next) => {
  const product_name = req.params.product_name;

  try {
    const productResult = await db.query(
      'SELECT * FROM products WHERE product_name = $1 LIMIT 1',
      [product_name]
    );
    if (productResult.rows.length === 0) {
      return res.status(404).render('404', { pageTitle: 'Product Not Found' });
    }
    const product = productResult.rows[0];


    const todayResult = await db.query(
      `SELECT price FROM products 
       WHERE product_name = $1 AND date = CURRENT_DATE`,
      [product_name]
    );
    const todayPrice = todayResult.rows[0]?.price || null;

    const maxResult = await db.query(
      `SELECT MAX(price) AS max_price FROM products WHERE product_name = $1`,
      [product_name]
    );
    const maxPrice = maxResult.rows[0].max_price || todayPrice;

    const historyResult = await db.query(
      `SELECT date, price FROM products
       WHERE product_name = $1 ORDER BY date ASC`,
      [product_name]
    );

    const priceHistory = historyResult.rows;

    const discount = maxPrice && todayPrice
      ? Math.round(((maxPrice - todayPrice) / maxPrice) * 100)
      : 0;

    if (req.session.user?.name) {
      res.render('product', {
        pageTitle: 'Product Details',
        username: req.session.user.name,
        image_path: product.product_image_link,
        name: product.product_name,
        price: todayPrice,
        max_price: maxPrice,
        discount: discount,
        priceHistory: priceHistory
      });
    } else {
      res.render('home', { pageTitle: 'Home', username: null });
    }
  } catch (err) {
    console.error('Error fetching product:', err);
    res.status(500).render('500', { pageTitle: 'Error' });
  }
};
