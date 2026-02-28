import pathway as pw

class ComplaintSchema(pw.Schema):
    wardNumber: int
    status: str

score_map = {
    "completed": 10,
    "resolved": 5,
    "pending": -5,
    "in-progress": -2
}

table = pw.io.jsonlines.read(
    "events.jsonl",
    schema=ComplaintSchema,
    mode="streaming"
)

scored = table.select(
    wardNumber=pw.this.wardNumber,
    score=(
        pw.if_else(pw.this.status == "completed", 10,
        pw.if_else(pw.this.status == "resolved", 5,
        pw.if_else(pw.this.status == "pending", -5,
        pw.if_else(pw.this.status == "in-progress", -2, 0))))
    )
)

aggregated = scored.groupby(
    pw.this.wardNumber
).reduce(
    wardNumber=pw.this.wardNumber,
    performanceScore=pw.reducers.sum(pw.this.score)
)

pw.io.jsonlines.write(
    aggregated,
    "ranking.json"
)

pw.run()