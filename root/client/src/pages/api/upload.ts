import { NextApiRequest, NextApiResponse } from "next";
import { pipeline } from "node:stream/promises";
import { Writable } from "node:stream";

export const config = {
  api: {
    bodyParser: false, // Disable default body parsing
  },
};

class BufferWritable extends Writable {
  chunks: Buffer[] = [];

  _write(chunk: Buffer, encoding: string, callback: (error?: Error) => void) {
    this.chunks.push(chunk);
    callback();
  }

  getBuffer() {
    return Buffer.concat(this.chunks);
  }
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const writable = new BufferWritable();
    await pipeline(req, writable);

    const response = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      headers: {
        "Content-Type": req.headers["content-type"] || "multipart/form-data",
        "Content-Length": req.headers["content-length"] || "",
      },
      body: writable.getBuffer(),
    });

    // Forward FastAPI response headers
    response.headers.forEach((value, key) => {
      res.setHeader(key, value);
    });

    return res.status(response.status).send(response.body);
  } catch (error) {
    console.error("Proxy error:", error);
    return res.status(500).json({ error: "File upload failed" });
  }
}
