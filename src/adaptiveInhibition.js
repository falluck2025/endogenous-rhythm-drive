function calculateR(V_inhibited, V_inhibitor) {
  return Math.abs(V_inhibited - V_inhibitor) / V_inhibited;
}

function calculateInhibitionDamping(R, K2_inhibited) {
  return R * K2_inhibited;
}

function calculateNetDrive(K1_inhibited, inhibitionDamping) {
  return K1_inhibited - inhibitionDamping;
}

function calculateBreathBase(V_curr) {
  return 20 - (V_curr - 60) * 6 / 40;
}

function calculateBreathConstraint(breathBase, breathCurrent, K2_current) {
  return Math.abs(breathBase / breathCurrent - 1) * K2_current;
}

module.exports = {
  calculateR,
  calculateInhibitionDamping,
  calculateNetDrive,
  calculateBreathBase,
  calculateBreathConstraint
};
