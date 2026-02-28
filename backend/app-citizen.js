require("dotenv").config();
const express = require("express");
const path = require("path");
const connectDB = require("./connection/mongoose");
const session = require("express-session");
const syncRankingToDB = require("./utils/syncRanking");

const app = express();


connectDB();

connectDB();
setInterval(() => {
  syncRankingToDB();
}, 3000);

require("./models/road");

const recalculateRanks = require("./utils/recalculateRanks");
// recalculateRanks();


app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.set("view engine", "ejs");

app.use(
  session({
    secret: process.env.SESSION_SECRET || "jbdshbbchbvefcvdsjbiidbdebfvubfv",
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      maxAge: 1000 * 60 * 60
    }
  })
);

app.use(express.static(path.join(__dirname, "../citizenPortal/public")));


app.set("views", path.join(__dirname, "../citizenPortal/views"));


const citizenPages = require("./routes/citizen");
const citizenMap = require("./routes/citizenMap");
const complaintRoutes = require("./routes/complaint");

app.use("/", citizenPages);
app.use("/map", citizenMap);
app.use("/", complaintRoutes);

const PORT = process.env.PORT|| 3000;
app.listen(PORT, () => {
  console.log(`Citizen Server running on port ${PORT}`);
});