const fs = require("fs");
const path = require("path");
const Ward = require("../models/ward");

async function syncRankingToDB() {
  try {
    const rankingPath = path.join(__dirname, "../../ranking.json");

    if (!fs.existsSync(rankingPath)) return;

    const raw = fs.readFileSync(rankingPath, "utf-8");
    if (!raw) return;

    const lines = raw.trim().split("\n");

    const latestScores = {};

    // Get latest score per ward
    lines.forEach(line => {
      const r = JSON.parse(line);
      latestScores[r.wardNumber] = r.performanceScore;
    });

    for (const wardNumber in latestScores) {
      await Ward.updateOne(
        { wardNumber: parseInt(wardNumber) },
        { $set: { performanceScore: latestScores[wardNumber] } }
      );
    }

  } catch (err) {
    console.error("Ranking sync error:", err);
  }
}

module.exports = syncRankingToDB;