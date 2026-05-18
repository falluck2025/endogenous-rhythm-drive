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

console.log("Test at V_curr = 60, V_target = 100:");
console.log("  K1 =", calculateK1(100, 60));
console.log("  K2 =", calculateK2(60));
console.log("  Acceleration =", calculateAcceleration(100, 60));
console.log("  V_next =", 60 + calculateAcceleration(100, 60) * 1);
console.log();

console.log("Test few steps:");
let V = 60;
for (let i = 0; i < 20; i++) {
  const a = calculateAcceleration(100, V);
  const newV = V + a * 1;
  console.log(`  Step ${i}: ${V.toFixed(2)} -> ${newV.toFixed(2)} (acceleration: ${a.toFixed(2)})`);
  V = Math.max(60, Math.min(120, newV));
}
