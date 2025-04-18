import { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const { question } = req.query;

    if (!question || typeof question !== "string") {
      return res.status(400).json({ error: "Question parameter required" });
    }

    const apiUrl = new URL("http://127.0.0.1:8000/ask");
    apiUrl.searchParams.set("question", question);

    const response = await fetch(apiUrl.toString(), {
      method: "POST",
      headers: { accept: "application/json" },
    });

    const data = await response.json();
    return res.status(response.status).json(data);
  } catch (error) {
    return res.status(500).json({ error: "Internal server error" });
  }
}
