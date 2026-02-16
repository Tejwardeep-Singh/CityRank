const calculateRanks = require("./rankCalculator");

async function recalculateRanks() {
  await calculateRanks();
}

module.exports = recalculateRanks;
