const V_MIN = 60;
const V_MAX = 100;
const K1_SCALE = 40;
const K2_BASE = 60;

function calculateK1(V_target, V_curr) {
  const diff = V_target - V_curr;
  return Math.abs(diff) / K1_SCALE;
}

function calculateK2(V_curr) {
  return K2_BASE / V_curr;
}

function calculateAcceleration(V_target, V_curr) {
  const K1 = calculateK1(V_target, V_curr);
  const K2 = calculateK2(V_curr);
  const diff = V_target - V_curr;
  return diff * K1 - diff * K2;
}

function updateHeartRate(V_target, V_curr, dt) {
  const acceleration = calculateAcceleration(V_target, V_curr);
  let newV = V_curr + acceleration * dt;
  newV = Math.min(Math.max(newV, V_MIN), V_MAX);
  return newV;
}

module.exports = {
  V_MIN,
  V_MAX,
  K1_SCALE,
  K2_BASE,
  calculateK1,
  calculateK2,
  calculateAcceleration,
  updateHeartRate
};
