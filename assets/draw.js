
console.log('we in!');

// NOTE that you must do a *hard* refresh (cmd+shift+R) to see these changes:
// On the bright side, you needn't restart the server.
var inputField;
var ctx;
var drawInterval;
var circ1, circ2;

window.onload = function() {
  console.log(document.getElementById('canv'));
  var canv = document.getElementById('canv');
  ctx = canv.getContext('2d');
  canv.height = 500;
  canv.width = 800;
  ctx.fillStyle = '#E6D5D5';
  ctx.fillRect(0, 0, 800, 500);

  var c1 = {
    x: 200,
    y: 250,
    r: 100,
    a: 0
  };
  var c2 = {
    x: 500,
    y: 250,
    r: 100,
    a: 0
  };
  circ1 = c1;
  circ2 = c2;
  drawCircles(c1, c2);


  inputField = document.getElementById('freq-in');
  console.log(inputField);

  // I mean this works....just takes a long time...but it shows up immediately in console if we click on console...
  inputField.addEventListener("change", function() {
    // console.log(ev);
    console.log('hi');
    console.log(inputField.value);

    c1 = {
      x: 200,
      y: 250,
      r: 100,
      a: 0
    };
    c2 = {
      x: 500,
      y: 250,
      r: 100,
      a: 0
    };
    circ1 = c1;
    circ2 = c2;
    drawCircles(c1, c2);

    drawInterval = setInterval(rotateLines, 50);

  });

};

function rotateLines() {
  circ1.a += 0.05;
  circ2.a += 0.1;
  drawCircles(circ1, circ2);
}


function drawCircles(c1, c2) {
  ctx.fillStyle = '#E6D5D5';
  ctx.fillRect(0, 0, 800, 500);

  ctx.beginPath();
  ctx.arc(c1.x, c1.y, c1.r, 0, 2*Math.PI);
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(c2.x, c2.y, c2.r, 0, 2*Math.PI);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(c1.x, c1.y);
  ctx.lineTo(c1.x + c1.r * Math.cos(c1.a), c1.y + c1.r * Math.sin(c1.a));
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(c2.x, c2.y);
  ctx.lineTo(c2.x + c2.r * Math.cos(c2.a), c2.y + c2.r * Math.sin(c2.a));
  ctx.stroke();


}
