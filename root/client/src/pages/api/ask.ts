import { NextApiRequest, NextApiResponse } from "next";
require("dotenv").config();

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const { question } = req.query;

    if (!question || typeof question !== "string") {
      return res.status(400).json({ error: "Question parameter required" });
    }

    const apiUrl = new URL(`${process.env.NEXT_PUBLIC_BACKEND_URL}/ask`);
    apiUrl.searchParams.set("question", question);

    const response = await fetch(apiUrl.toString(), {
      method: "POST",
      headers: { accept: "application/json" },
    });

    // Forward headers from the backend response
    response.headers.forEach((value, key) => {
      if (key.toLowerCase() !== "content-length") {
        res.setHeader(key, value);
      }
    });

    const data = await response.json();

    // Check if this is the specific error about no documents processed
    if (
      response.status === 400 &&
      data.detail === "No documents processed yet"
    ) {
      // You could redirect to file upload page or provide a more helpful message
      return res.status(400).json({
        error: "Please upload documents before asking questions",
        needsUpload: true,
      });
    }

    return res.status(response.status).json(data);
  } catch (error) {
    console.error("API handler error:", error);
    return res.status(500).json({ error: "Internal server error" });
  }
}
