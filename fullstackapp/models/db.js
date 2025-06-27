const {Pool} = require('pg')

exports.pgpool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'ajtracker',
  password: 'jay',
  port: 5432,
});
