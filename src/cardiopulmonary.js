const rhythmDriver = require('./rhythmDriver');

function deriveBreathRate(V_curr) {
  return 20 - (V_curr - 60) * 6 / 40;
}

function calculateCouplingForce(breathRate, V_curr) {
  const K2_current = rhythmDriver.calculateK2(V_curr);
  return Math.abs(breathRate / Math.max(breathRate, 1) - 1) * K2_current;
}

module.exports = {
  deriveBreathRate,
  calculateCouplingForce
};
