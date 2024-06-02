var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Yun PDP' });
});

router.post('/login', function(req, res) {
  

  res.json({ status: 'success', message: 'Received username and password successfully.' });
});

module.exports = router;
