// let windowWidth =  window.innerWidth - 20;
// let heigth = 500;
let vers = new Array();
let edges = new Array();
let VerR = 9;
let AbsVel = 0.1;
let maxVel = 0.5, stableVel = 0.08;
let NumVers = 80;
let minConnectDistance = 80;
let mouseNearA = 20;
let mouseNearK = 2;
let lineWidth = 0;
let cnv, bg;

let backgrounds_dark = ['2bg.jpg', '3bg.jpg', '5bg.jpg', '6bg.jpg']
let backgrounds_bright = ['1bg.jpg', '4bg.jpg']

let standartVertexColor;

function getRndInteger(min, max) {
    return Math.floor(random(min, max)) + min;
}

function getSuperfluousR(dx, dy, l) {
    let squareSide = VerR / 2;
    let rx = (dx * squareSide) / l;
    let ry = (dy * squareSide) / l;
    console.log(rx, ry);
    return {"x": rx, "y": ry};
}

// class Edge {
//     constructor(v1, v2, color) {
//         this.v1 = v1;
//         this.v2 = v2;
//         this.color = color;
//     }
// }

class Vertex {
    constructor(x, y, vx, vy, color) {
        this.color = color
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
    }
}

function getVerDistance(v1, v2) {
    return Math.sqrt((v1.x - v2.x) * (v1.x - v2.x) + (v1.y - v2.y) * (v1.y - v2.y));
}

function getDistanceToDot(v1, x, y) {
    return Math.sqrt( (v1.x - x) * (v1.x - x) + (v1.y - y) * (v1.y - y) );
}

function generateEllipses(n) {
    for (let i = 0; i < n; i++) {
        vers.push(new Vertex(random(VerR, windowWidth - VerR), random(VerR, windowHeight - VerR), random(-AbsVel, AbsVel), random(-AbsVel, AbsVel),
            standartVertexColor));
    }
}

function mousePressed() {
    vers.push(new Vertex(mouseX, mouseY, random(-AbsVel, AbsVel), 
        random(-AbsVel, AbsVel), standartVertexColor))
}

function setup() {
    let bgs = backgrounds_bright.concat(backgrounds_dark);
    let bg_name = bgs[getRndInteger(0, bgs.length)];
    bg = loadImage("/static/Authorize/img/" + bg_name);

    if (backgrounds_bright.includes(bg_name)) {
        standartVertexColor = {"r": 0, "g": 124, "b": 118};        
    } else {
        standartVertexColor = {"r": 0, "g": 255, "b": 234};
    }

    cnv = createCanvas(windowWidth, windowHeight);
    cnv.style('display', 'block');
    cnv.style('z-index', '900')
    centerCanvas();
    // cnv.parent('animation_holder');
    generateEllipses(NumVers);
    // generateEdges(10);
}

function centerCanvas() {
    var x = (windowWidth - width) / 2;
    var y = (windowHeight - height) / 2;
    cnv.position(x, y);
  }  

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}

function draw() {  
    background(bg);  
    for (let i = 0; i < vers.length; i++) {
        fill(vers[i].color.r, vers[i].color.g, vers[i].color.b);
        ellipse(vers[i].x, vers[i].y, VerR, VerR);

        if (getDistanceToDot(vers[i], mouseX, mouseY) <= mouseNearA) {
            if (Math.abs(vers[i].vx) < maxVel) vers[i].vx *= mouseNearK;
            if (Math.abs(vers[i].vy) < maxVel) vers[i].vy *= mouseNearK;
        } else {
            if (Math.abs(vers[i].vx) >= stableVel) {
                if (vers[i].vx > 0) vers[i].vx -= 0.05; 
                else vers[i].vx += 0.05;
            } 
            if (Math.abs(vers[i].vy) >= stableVel) {
                if (vers[i].vy > 0) vers[i].vy -= 0.05; 
                else vers[i].vy += 0.05;
            }  
        }

        if (vers[i].x - VerR <= 0 || vers[i].x + VerR >= windowWidth) {
            vers[i].vx = -vers[i].vx
        }
        if (vers[i].y - VerR <= 0 || vers[i].y + VerR >= windowHeight) {
            vers[i].vy = -vers[i].vy
        }

        vers[i].x += vers[i].vx;
        vers[i].y += vers[i].vy;
    }
    for (let i = 0; i < vers.length; i++) {
        for (let j = i + 1; j < vers.length; j++) {
            let verDis = getVerDistance(vers[i], vers[j]);
            if (verDis <= minConnectDistance) {
                if (lineWidth == 0) {
                    stroke(153);
                    let dr = getSuperfluousR(Math.abs(vers[i].x - vers[j].x),
                        Math.abs(vers[i].y - vers[j].y), verDis)
                    if (vers[i].x < vers[j].x) {
                        if (vers[i].y < vers[j].y) {
                            line(vers[i].x + dr.x, vers[i].y + dr.y, vers[j].x - dr.x, vers[j].y - dr.y);
                        } else {
                            line(vers[i].x + dr.x, vers[i].y - dr.y, vers[j].x - dr.x, vers[j].y + dr.y);
                        }
                    } else {
                        if (vers[i].y < vers[j].y) {
                            line(vers[i].x - dr.x, vers[i].y + dr.y, vers[j].x + dr.x, vers[j].y - dr.y);
                        } else {
                            line(vers[i].x - dr.x, vers[i].y - dr.y, vers[j].x + dr.x, vers[j].y + dr.y);                            
                        }
                    }
                } else {
                    fill(random(255), random(255), random(255));
                    quad(vers[i].x - lineWidth / 2, vers[i].y - lineWidth / 2,
                        vers[i].x + lineWidth / 2, vers[i].y + lineWidth / 2,
                        vers[j].x + lineWidth / 2, vers[j].y + lineWidth / 2,
                        vers[j].x - lineWidth / 2, vers[j].y - lineWidth / 2);
                }
            }
        }
    }
}