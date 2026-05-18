const fs = require('fs');
const path = require('path');
const rhythmDriver = require('../src/rhythmDriver');
const adaptiveInhibition = require('../src/adaptiveInhibition');
const cardiopulmonary = require('../src/cardiopulmonary');

function calculateK1(V_target, V_curr) {
  return Math.abs(V_target - V_curr) / 40;
}

function calculateK2(V_curr) {
  return 60 / V_curr;
}

function calculateAcceleration(V_target, V_curr) {
  const K1 = calculateK1(V_target, V_curr);
  const K2 = calculateK2(V_curr);
  const diff = V_target - V_curr;
  return diff * K1 - (V_curr - V_target) * K2;
}

function calculateR(V_inhibited, V_inhibitor) {
  return Math.abs(V_inhibited - V_inhibitor) / V_inhibited;
}

function runExperiment1() {
  const data = [];
  let V_curr = 60;
  const dt = 0.7;

  for (let i = 0; i < 300; i++) {
    let V_target = i < 20 ? 60 : 100;
    
    const K1 = calculateK1(V_target, V_curr);
    const K2 = calculateK2(V_curr);
    const acceleration = calculateAcceleration(V_target, V_curr);
    
    data.push({
      frame: i,
      V_curr: V_curr,
      V_target: V_target,
      K1: K1,
      K2: K2,
      acceleration: acceleration
    });
    
    if (i >= 19) {
      const newV = V_curr + acceleration * dt;
      V_curr = Math.max(60, Math.min(120, newV));
    }
  }

  return data;
}

function runExperiment2() {
  const data = [];
  
  const inhibitionCases = [
    { label: 'strong', V_inhibited: 100, V_inhibitor: 60, expectedR: 0.40 },
    { label: 'medium', V_inhibited: 80, V_inhibitor: 100, expectedR: 0.25 },
    { label: 'weak', V_inhibited: 90, V_inhibitor: 80, expectedR: 0.11 }
  ];

  inhibitionCases.forEach(({ label, V_inhibited, V_inhibitor, expectedR }) => {
    const R = calculateR(V_inhibited, V_inhibitor);
    const K2_inhibited = calculateK2(V_inhibited);
    const K1_inhibited = calculateK1(V_inhibitor, V_inhibited);
    const damping = R * K2_inhibited;
    const netDrive = K1_inhibited - damping;
    
    data.push({
      label,
      V_inhibited,
      V_inhibitor,
      R,
      expectedR,
      K1_inhibited,
      K2_inhibited,
      damping,
      netDrive
    });
  });

  return data;
}

function runExperiment3() {
  const data = [];
  let V_curr = 60;
  let totalTasks = 0;
  const dt = 0.1;

  for (let i = 0; i < 150; i++) {
    let V_target, tasks, phase;
    
    if (i < 50) {
      phase = 'light';
      V_target = 60;
      tasks = 5 + Math.floor(Math.random() * 3);
    } else if (i < 100) {
      phase = 'heavy';
      V_target = 95;
      tasks = 15 + Math.floor(Math.random() * 5);
    } else {
      phase = 'recovery';
      V_target = 60;
      tasks = 5 + Math.floor(Math.random() * 3);
    }

    const breathBase = 20 - (V_curr - 60) * 6 / 40;
    const breathCurrent = 20 - (V_curr - 60) * 6 / 40;
    const K2_curr = calculateK2(V_curr);
    const constraintForce = Math.abs(breathBase / breathCurrent - 1) * K2_curr;
    
    data.push({
      frame: i,
      V_curr: V_curr,
      V_target: V_target,
      breathBase: breathBase,
      breathCurrent: breathCurrent,
      constraintForce: constraintForce,
      tasks: tasks,
      phase: phase
    });

    totalTasks += tasks;
    
    const acceleration = calculateAcceleration(V_target, V_curr);
    V_curr = V_curr + acceleration * dt;
    V_curr = Math.max(60, Math.min(120, V_curr));
  }

  return { heartRateData: data, totalTasks: totalTasks };
}

function saveJson(data, filename) {
  const figuresDir = path.join(__dirname, '..', 'figures');
  if (!fs.existsSync(figuresDir)) {
    fs.mkdirSync(figuresDir, { recursive: true });
  }
  const filepath = path.join(figuresDir, filename);
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
  console.log(`Saved: ${filepath}`);
}

function main() {
  console.log('Running Experiment 1: Heart Rate 60->100 Overshoot (300 frames)...');
  const exp1 = runExperiment1();
  saveJson(exp1, 'experiment1.json');
  console.log(`  - Frames: ${exp1.length}`);
  console.log(`  - Final V_curr: ${exp1[exp1.length - 1].V_curr.toFixed(2)}`);
  console.log(`  - Max V_curr: ${Math.max(...exp1.map(d => d.V_curr)).toFixed(2)}`);

  console.log('\nRunning Experiment 2: Three Inhibition Relationships...');
  const exp2 = runExperiment2();
  saveJson(exp2, 'experiment2.json');
  exp2.forEach(d => {
    console.log(`  - ${d.label}: R=${d.R.toFixed(2)} (expected ${d.expectedR.toFixed(2)})`);
  });

  console.log('\nRunning Experiment 3: Light/Heavy/Recovery Load...');
  const exp3 = runExperiment3();
  saveJson(exp3, 'experiment3.json');
  console.log(`  - Total tasks: ${exp3.totalTasks}`);
  console.log(`  - Frames: ${exp3.heartRateData.length}`);
  console.log(`  - Final V_curr: ${exp3.heartRateData[exp3.heartRateData.length - 1].V_curr.toFixed(2)}`);

  console.log('\nAll experiments completed successfully!');
}

main();
