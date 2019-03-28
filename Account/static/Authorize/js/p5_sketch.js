let Width =  window.innerWidth - 20;
let heigth = 500;
let vers = new Array();
let edges = new Array();
let VerR = 15;
let AbsVel = 0.3;
let maxVel = 0.9, stableVel = 0.22;
let NumVers = 80;
let minConnectDistance = 80;
let mouseNearA = 20;
let mouseNearK = 2;
let lineWidth = 0;

function getRndInteger(min, max) {
    return Math.floor(random(min, max)) + min;
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
        vers.push(new Vertex(random(VerR, Width - VerR), random(VerR, height - VerR), random(-AbsVel, AbsVel), random(-AbsVel, AbsVel),
            {"r": random(255), "g": random(255), "b": random(255)}));
    }
}

function setup() {
    createCanvas(Width, 500);
    generateEllipses(NumVers);
    // generateEdges(10);
}

function mousePressed() {
    vers.push(new Vertex(mouseX, mouseY, random(-AbsVel, AbsVel), 
        random(-AbsVel, AbsVel), {"r": random(255), "g": random(255), "b": random(255)}))
}

function draw() {    
    background(255);
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

        if (vers[i].x - VerR <= 0 || vers[i].x + VerR >= Width) {
            vers[i].vx = -vers[i].vx
        }
        if (vers[i].y - VerR <= 0 || vers[i].y + VerR >= height) {
            vers[i].vy = -vers[i].vy
        }

        vers[i].x += vers[i].vx;
        vers[i].y += vers[i].vy;
    }
    for (let i = 0; i < vers.length; i++) {
        for (let j = i + 1; j < vers.length; j++) {
            if (getVerDistance(vers[i], vers[j]) <= minConnectDistance) {
                if (lineWidth == 0) {
                    line(vers[i].x, vers[i].y, vers[j].x, vers[j].y);
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