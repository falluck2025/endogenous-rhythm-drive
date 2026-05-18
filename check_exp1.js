const fs = require('fs');
const path = require('path');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'figures', 'experiment1.json'), 'utf8'));

console.log("Experiment 1 analysis:");
console.log(`Number of frames: ${data.length}`);

console.log("\nFirst 30 frames:");
for (let i = 0; i < 30; i++) {
  console.log(`Frame ${i}: V_curr=${data[i].V_curr.toFixed(2)}, K1=${data[i].K1.toFixed(2)}, K2=${data[i].K2.toFixed(2)}, a=${data[i].acceleration.toFixed(2)}`);
}

const maxV = Math.max(...data.map(d => d.V_curr));
const maxFrame = data.findIndex(d => d.V_curr === maxV);

console.log(`\nMax V_curr: ${maxV.toFixed(2)} at frame ${maxFrame}`);
console.log(`Final V_curr: ${data[data.length-1].V_curr.toFixed(2)}`);
