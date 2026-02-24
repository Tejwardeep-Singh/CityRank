require("dotenv").config();
const express = require("express");
const path = require("path");
const connectDB = require("./connection/mongoose");
const session = require("express-session");


const app = express();


connectDB();

require("./models/road");

const recalculateRanks = require("./utils/recalculateRanks");
// recalculateRanks();


app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.set("view engine", "ejs");

app.use(
  session({
    secret: process.env.SESSION_SECRET || "kjdbdskjcbjcvudbjchcihvcihsdiy",
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      maxAge: 1000 * 60 * 60
    }
  })
);


app.use(express.static(path.join(__dirname, "../adminPortal/public")));


app.set("views", path.join(__dirname, "../adminPortal/views"));


const adminPages = require("./routes/admin");

app.get("/", (req, res) => {
  res.redirect("/admin");
});

app.use("/admin", adminPages);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Admin Server running on port ${PORT}`);
});