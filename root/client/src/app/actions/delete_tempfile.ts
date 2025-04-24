"use server"
import { NextApiRequest, NextApiResponse } from "next";
import { pipeline } from "node:stream/promises";
import { Writable } from "node:stream";

export async function delete_files(){
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/removetempfiles`, {
      method: 'POST',
    })
      .then(response => {
        if (!response.ok) throw new Error('Failed to clear temp files');
        console.log('Temp files cleanup triggered');
      })
      .catch(error => console.error('Cleanup error:', error));
}