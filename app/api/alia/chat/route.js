import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req) {
  try {
    const body = await req.json();

    const {
      message,
      tickets = [],
      leads = [],
      invoices = [],
      calls = [],
      shipments = [],
    } = body;

    const systemPrompt = `
You are ALIA, a calm, professional operations assistant for Tritanium Command.

Your job:
- help employees understand what needs attention
- answer naturally, not robotically
- summarize leads, calls, invoices, tickets, and shipments
- give practical next-step suggestions
- stay concise but helpful
- do not invent records that are not present
- if data is missing, say so plainly

Tone:
- confident
- warm
- clear
- operational
- never overly casual
`;

    const contextBlock = `
CURRENT DATA

TICKETS:
${JSON.stringify(tickets)}

LEADS:
${JSON.stringify(leads)}

INVOICES:
${JSON.stringify(invoices)}

CALLS:
${JSON.stringify(calls)}

SHIPMENTS:
${JSON.stringify(shipments)}
`;

    const response = await client.responses.create({
      model: 'gpt-5.4',
      input: [
        {
          role: 'system',
          content: [
            { type: 'input_text', text: systemPrompt },
            { type: 'input_text', text: contextBlock },
          ],
        },
        {
          role: 'user',
          content: [{ type: 'input_text', text: message }],
        },
      ],
    });

    return Response.json({
      reply: response.output_text || 'I was not able to generate a reply.',
    });
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message || 'ALIA core request failed.' }),
      { status: 500 }
    );
  }
}
